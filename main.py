import chess
import chess.engine
import io
import chess.pgn
from functools import lru_cache
from time import time
import numpy as np
from scipy.interpolate import interp1d
 
 
PATH = r'C:\Users\trept\OneDrive\Desktop\Chesstin\stockfish_14_x64_avx2.exe'
engine = chess.engine.SimpleEngine.popen_uci(PATH)
 
 
def approximate_table(x):
    # Given data points
    x_points = np.array([1, 2, 3, 4])
    y_points = np.array([0.714, 0.703, 0.704, 0.701])
    
    # Create an interpolation function with extrapolation
    interpolating_function = interp1d(x_points, y_points, kind='linear', fill_value="extrapolate")
    
    # Return the interpolated or extrapolated value for x
    return float(interpolating_function(x))
 
def board_to_pgn_stringio(board):
    game = chess.pgn.Game()
    node = game
 
    for move in board.move_stack:
        node = node.add_variation(move)
 
    pgn_str = str(game)
    pgn_io = io.StringIO(pgn_str)
    
    return pgn_io
 
 
def merge_pgns_to_variations(*pgn_ios):
    games = []
 
    for pgn_io in pgn_ios:
        game = chess.pgn.read_game(pgn_io)
        while game is not None:
            games.append(game)
            game = chess.pgn.read_game(pgn_io)
 
    master_node = chess.pgn.Game()
 
    mlist = []
    for game in games:
        mlist.extend(game.variations)
 
    variations = [(master_node, mlist)]
    done = False
 
    while not done:
        newvars = []
        done = True
        for vnode, nodes in variations:
            newmoves = {}
            for node in nodes:
                if node.move is None:
                    continue
                elif node.move not in list(newmoves):
                    nvnode = vnode.add_variation(node.move)
                    if len(node.variations) > 0:
                        done = False
                    newvars.append((nvnode, node.variations))
                    newmoves[node.move] = len(newvars) - 1
                else:
                    nvnode, nlist = newvars[newmoves[node.move]]
                    if len(node.variations) > 0:
                        done = False
                    nlist.extend(node.variations)
                    newvars[newmoves[node.move]] = (nvnode, nlist)
        variations = newvars
 
    exporter = chess.pgn.StringExporter(headers=True, variations=True, comments=True)
    merged_pgn = master_node.accept(exporter)
 
    return io.StringIO(merged_pgn)
 
 
# Wrapper function for memoization
@lru_cache(maxsize=None)
def memoized_get_top_moves(board_fen, n, limit):
    return _get_top_moves(chess.Board(fen=board_fen), n, limit)
 
# The core function
def _get_top_moves(board: chess.Board, n: int, limit: float) -> list:
    analysis = engine.analyse(board=board, limit=chess.engine.Limit(time=limit), multipv=n)
    return [info['pv'][0] for info in analysis]
 
# Entry point function
def get_top_moves(board: chess.Board = None, n: int = 5, limit: float = 0.5) -> list:
    return memoized_get_top_moves(board.fen(), n, limit)
 
 
 
def play_board(board: chess.Board = None, k: int = 8, limit: float = 2.5):
    board = board.copy()
    
    for _ in range(k):
        result = engine.play(board, limit=chess.engine.Limit(time=limit))
        board.push(result.move)
        
    return board
 
 
def recursive_variations(board: chess.Board, original_side, d: int, k: int, b: int, limit: float, depth: int = 0):
    if depth >= d:
        return [board_to_pgn_stringio(play_board(board, k, limit))]
 
    boards = []
 
    if board.turn == original_side:
        top_moves = get_top_moves(board=board, n=b if depth > 0 else 4, limit=limit)
        for move in top_moves:
            board.push(move)
            boards.extend(recursive_variations(board, original_side, d, k, b, limit, depth + 1))
            board.pop()
    else:
        result = engine.play(board, limit=chess.engine.Limit(time=limit))
        board.push(result.move)
        boards.extend(recursive_variations(board, original_side, d, k, b, limit, depth + 1))
        board.pop()
 
    return boards
 
 
def master_func(board: chess.Board = None, n_top_moves: int = 4, k_moves_played: int = 8, time_limit: float = 0.5, depth: int = 1, path: str = 'merged.pgn'):
    depth *= 2
    
    boards = recursive_variations(board, board.turn, depth, k_moves_played, n_top_moves, time_limit)
    merged = merge_pgns_to_variations(*boards)
    
    with open(path, 'w') as f:
        f.write(merged.getvalue())
 
def estimate_time(d, k, b, limit, original_side, depth=0, is_original_side_turn=True):
    # Base case: If the depth is greater than or equal to the maximum depth
    if depth >= d:
        return k * limit
 
    # Time to analyze moves at the current depth
    if is_original_side_turn:
        current_level_time = b * limit
        next_level_time = b * estimate_time(d, k, b, limit, original_side, depth + 1, not is_original_side_turn)
    else:
        current_level_time = limit
        next_level_time = estimate_time(d, k, b, limit, original_side, depth + 1, not is_original_side_turn)
 
    
    return (current_level_time + next_level_time)
 
 
def main():
    try:
        params = {'depth': 5,
                  'n_top_moves': 4,
                  'k_moves_played': 5,
                  'time_limit': 0.2
                  }
        
        moves = ['d2d4', 'f7f5']
        board = chess.Board()
    
        for move in moves:
            board.push(chess.Move.from_uci(move))
        
        
        estimate = estimate_time(
            params.get('depth',2) * 2,
            params.get('k_moves_played', 5),
            params.get('n_top_moves', 5),
            params.get('time_limit', 0.5),
            board.turn
            
         ) * approximate_table(params.get('depth', 2))
        
        
        
        print(f"Estimate: {estimate:.2f}")
        
        start = time()
        
        master_func(
            board=board, 
            depth=params.get('depth', 2),
            n_top_moves=params.get('n_top_moves', 5), 
            k_moves_played=params.get('k_moves_played', 5), 
            time_limit=params.get('time_limit', 0.5)
            )
        
        end = time()
        elapsed_time = abs(start-end)
        
        print(f"Actual: {elapsed_time:.2f}")
        
    except Exception as e:
        print(e)
        engine.quit()
                
    finally:    
        
        engine.quit()
 
 
if __name__ == '__main__':
    main()
