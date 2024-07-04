import chess
import chess.engine
from functools import lru_cache

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

