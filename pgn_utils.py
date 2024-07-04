import chess.pgn
import io

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

