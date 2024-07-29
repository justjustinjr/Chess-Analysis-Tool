from functools import lru_cache
import io
from time import time

import chess
import chess.engine
import chess.pgn
import numpy as np
from scipy.interpolate import interp1d


# Path to the Stockfish engine executable
STOCKFISH_PATH = r'C:\Users\trept\OneDrive\Desktop\Chesstin\stockfish_14_x64_avx2.exe'
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)


def board_to_pgn_stringio(board):
    """
    Convert a chess board to a PGN string in a StringIO object.

    :param board: The chess board to convert.
    :return: The PGN representation of the board in a StringIO object.
    """
    game = chess.pgn.Game()  # Create a new PGN game
    node = game

    # Add moves to the PGN game
    for move in board.move_stack:
        node = node.add_variation(move)

    pgn_str = str(game)  # Convert game to PGN string
    pgn_io = io.StringIO(pgn_str)  # Convert PGN string to StringIO
    return pgn_io


def merge_pgn_variations(*pgn_ios):
    """
    Merge multiple PGN variations into a single PGN.

    :param pgn_ios: PGN StringIO objects to merge.
    :return: The merged PGN in a StringIO object.
    """
    games = []

    # Read all PGN games from the provided StringIO objects
    for pgn_io in pgn_ios:
        game = chess.pgn.read_game(pgn_io)
        while game is not None:
            games.append(game)
            game = chess.pgn.read_game(pgn_io)

    master_node = chess.pgn.Game()  # Create a master PGN node
    move_variations = []

    # Collect all variations from the games
    for game in games:
        move_variations.extend(game.variations)

    variations = [(master_node, move_variations)]
    done = False

    # Merge variations into the master node
    while not done:
        new_variations = []
        done = True
        for vnode, nodes in variations:
            move_dict = {}
            for node in nodes:
                if node.move is None:
                    continue
                if node.move not in move_dict:
                    new_vnode = vnode.add_variation(node.move)
                    if len(node.variations) > 0:
                        done = False
                    new_variations.append((new_vnode, node.variations))
                    move_dict[node.move] = len(new_variations) - 1
                else:
                    new_vnode, node_list = new_variations[move_dict[node.move]]
                    if len(node.variations) > 0:
                        done = False
                    node_list.extend(node.variations)
                    new_variations[move_dict[node.move]] = (new_vnode, node_list)
        variations = new_variations

    # Export the merged PGN
    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
    merged_pgn = master_node.accept(exporter)

    return io.StringIO(merged_pgn)


@lru_cache(maxsize=None)
def memoized_get_top_moves(board_fen, num_moves, time_limit):
    """
    Memoized function to get the top moves from a given board position.

    :param board_fen: The FEN string of the board position.
    :param num_moves: The number of top moves to retrieve.
    :param time_limit: The time limit for the analysis.
    :return: A list of the top moves.
    """
    return _get_top_moves(chess.Board(fen=board_fen), num_moves, time_limit)


def _get_top_moves(board: chess.Board, num_moves: int, time_limit: float) -> list:
    """
    Get the top moves from a given board position using Stockfish.

    :param board: The chess board to analyze.
    :param num_moves: The number of top moves to retrieve.
    :param time_limit: The time limit for the analysis.
    :return: A list of the top moves.
    """
    analysis = engine.analyse(board=board, limit=chess.engine.Limit(time=time_limit), multipv=num_moves)
    return [info['pv'][0] for info in analysis]  # Extract the top moves


def get_top_moves(board: chess.Board = None, num_moves: int = 5, time_limit: float = 0.5) -> list:
    """
    Wrapper function to get the top moves with memoization.

    :param board: The chess board to analyze.
    :param num_moves: The number of top moves to retrieve.
    :param time_limit: The time limit for the analysis.
    :return: A list of the top moves.
    """
    return memoized_get_top_moves(board.fen(), num_moves, time_limit)


def simulate_moves(board: chess.Board = None, num_moves: int = 8, time_limit: float = 2.5):
    """
    Simulate a series of moves on the board using Stockfish.

    :param board: The chess board to simulate moves on.
    :param num_moves: The number of moves to simulate.
    :param time_limit: The time limit for each move.
    :return: The resulting board after the simulated moves.
    """
    board = board.copy()  # Create a copy of the board
    
    # Simulate moves on the board
    for _ in range(num_moves):
        result = engine.play(board, limit=chess.engine.Limit(time=time_limit))
        board.push(result.move)
        
    return board


def recursive_variations(board: chess.Board, original_side, max_depth: int, num_simulated_moves: int, num_top_moves: int, time_limit: float, current_depth: int = 0):
    """
    Generate recursive variations of the board up to a given depth.

    :param board: The chess board to analyze.
    :param original_side: The original side to move.
    :param max_depth: The maximum depth of analysis.
    :param num_simulated_moves: The number of moves to simulate in each variation.
    :param num_top_moves: The number of top moves to consider at each step.
    :param time_limit: The time limit for each move analysis.
    :param current_depth: The current depth of the recursive analysis.
    :return: A list of PGN StringIO objects representing the variations.
    """
    if current_depth >= max_depth:
        return [board_to_pgn_stringio(simulate_moves(board, num_simulated_moves, time_limit))]

    boards = []

    # Generate variations based on the side to move
    if board.turn == original_side:
        top_moves = get_top_moves(board=board, num_moves=num_top_moves if current_depth > 0 else 4, time_limit=time_limit)
        for move in top_moves:
            board.push(move)
            boards.extend(recursive_variations(board, original_side, max_depth, num_simulated_moves, num_top_moves, time_limit, current_depth + 1))
            board.pop()
    else:
        result = engine.play(board, limit=chess.engine.Limit(time=time_limit))
        board.push(result.move)
        boards.extend(recursive_variations(board, original_side, max_depth, num_simulated_moves, num_top_moves, time_limit, current_depth + 1))
        board.pop()

    return boards


def analyze_board(board: chess.Board = None, num_top_moves: int = 4, num_simulated_moves: int = 8, time_limit: float = 0.5, depth: int = 1, output_path: str = 'merged.pgn'):
    """
    Analyze the given chess board and generate a merged PGN file of variations.

    :param board: The chess board to analyze.
    :param num_top_moves: The number of top moves to consider.
    :param num_simulated_moves: The number of moves to simulate in each variation.
    :param time_limit: The time limit for each move analysis.
    :param depth: The depth of analysis.
    :param output_path: The file path to save the merged PGN.
    """
    depth *= 2  # Double the depth for complete analysis
    boards = recursive_variations(board, board.turn, depth, num_simulated_moves, num_top_moves, time_limit)
    merged_pgn = merge_pgn_variations(*boards)
    
    # Save the merged PGN to the specified file
    with open(output_path, 'w') as file:
        file.write(merged_pgn.getvalue())


def estimate_analysis_time(max_depth, num_simulated_moves, num_top_moves, time_limit, original_side, current_depth=0, is_original_side_turn=True):
    """
    Estimate the time required for the analysis.

    :param max_depth: The maximum depth of analysis.
    :param num_simulated_moves: The number of moves to simulate in each variation.
    :param num_top_moves: The number of top moves to consider at each step.
    :param time_limit: The time limit for each move analysis.
    :param original_side: The original side to move.
    :param current_depth: The current depth of the analysis.
    :param is_original_side_turn: Boolean indicating if it's the original side's turn.
    :return: The estimated time for the analysis.
    """
    if current_depth >= max_depth:
        return num_simulated_moves * time_limit

    if is_original_side_turn:
        current_level_time = num_top_moves * time_limit
        next_level_time = num_top_moves * estimate_analysis_time(max_depth, num_simulated_moves, num_top_moves, time_limit, original_side, current_depth + 1, not is_original_side_turn)
    else:
        current_level_time = time_limit
        next_level_time = estimate_analysis_time(max_depth, num_simulated_moves, num_top_moves, time_limit, original_side, current_depth + 1, not is_original_side_turn)

    return current_level_time + next_level_time


def get_params():
    """
    Prompt the user to input parameters for the analysis.

    :return: A dictionary of input parameters and the initial board setup.
    """
    params = {}
    
    # Prompt for depth of analysis
    params['depth'] = int(input("Enter the depth of analysis (e.g., 3). Note: The program time grows exponentially with the depth: "))
    
    # Prompt for number of top moves to consider
    params['num_top_moves'] = int(input("Enter the number of top moves to consider (e.g., 4): "))
    
    # Prompt for number of moves to simulate in each variation
    params['num_simulated_moves'] = int(input("Enter the number of moves to simulate in each variation (e.g., 8): "))
    
    # Prompt for time limit for each move analysis
    params['time_limit'] = float(input("Enter the time limit for each move analysis in seconds (e.g., 0.5): "))
    
    # Prompt for output file path
    params['output_path'] = input("Enter the output file path for the merged PGN (e.g., 'merged.pgn'): ")
    
    # Prompt for initial board setup
    print("Enter the initial moves in UCI format separated by spaces (e.g., 'e2e4 e7e5').")
    moves_input = input("Initial moves: ")
    moves = moves_input.split()
    
    # Create a board and push the initial moves
    board = chess.Board()
    for move in moves:
        board.push(chess.Move.from_uci(move))
    
    params['initial_board'] = board
    
    return params


def main():
    """
    Main function to run the analysis.
    """
    try:
        print("Chess Analysis Tool (CAT) created by J₂ + US₆ → 3 Ti + N₅")
        print("Add suggestoins at the github: https://github.com/Treptune/Chess-Analysis-Tool/tree/main")
        print()
        print()
        
        params = get_params()  # Get parameters from the user
        
        print()
        print()
        
        # Estimate the time required for the analysis
        estimate = estimate_analysis_time(
            params['depth'] * 2,
            params['num_simulated_moves'],
            params['num_top_moves'],
            params['time_limit'],
            params['initial_board'].turn
        )
        
        print(f"Estimated Time: {estimate:.2f} seconds")
        
        start_time = time()
        
        # Perform the board analysis and save the results
        analyze_board(
            board=params['initial_board'], 
            num_top_moves=params['num_top_moves'], 
            num_simulated_moves=params['num_simulated_moves'], 
            time_limit=params['time_limit'], 
            depth=params['depth'], 
            output_path=params['output_path']
        )
        
        end_time = time()
        elapsed_time = end_time - start_time
        
        print(f"Actual Time: {elapsed_time:.2f} seconds")
        
    except Exception as e:
        print(f"Error: {e}")
        engine.quit()
    finally:    
        engine.quit()


if __name__ == '__main__':
    main()
