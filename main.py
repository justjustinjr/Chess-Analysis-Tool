import chess
import chess.engine
from time import time
from engine_utils import play_board, recursive_variations, get_top_moves
from pgn_utils import merge_pgns_to_variations, board_to_pgn_stringio
from estimate_time import estimate_time, approximate_table

PATH = 'stockfish_14_x64_avx2.exe'

def master_func(board: chess.Board = None, n_top_moves: int = 4, k_moves_played: int = 8, time_limit: float = 0.5, depth: int = 1, path: str = 'merged.pgn'):
    depth *= 2
    boards = recursive_variations(board, board.turn, depth, k_moves_played, n_top_moves, time_limit)
    merged = merge_pgns_to_variations(*boards)
    with open(path, 'w') as f:
        f.write(merged.getvalue())

def main():
    try:
        params = {
            'depth': 5,
            'n_top_moves': 3,
            'k_moves_played': 7,
            'time_limit': 0.2
        }
        
        moves = ['d2d4', 'f7f5']
        board = chess.Board()
        for move in moves:
            board.push(chess.Move.from_uci(move))
        
        global engine
        engine = chess.engine.SimpleEngine.popen_uci(PATH)
        
        estimate = estimate_time(
            params.get('depth', 2) * 2,
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
        elapsed_time = abs(start - end)
        print(f"Actual: {elapsed_time:.2f}")
        
    except Exception as e:
        print(e)
        engine.quit()
        print("An error occurred during the process.")
        
    finally:    
        engine.quit()
        print("Program completed successfully.")

if __name__ == '__main__':
    main()

