import chess
import chess.engine


board=chess.Board()
engine = chess.engine.SimpleEngine.popen_uci("resources\engine\stockfish_15_win_x64_popcnt\stockfish_15_x64_popcnt.exe")
lm = board.legal_moves
print(board)
player_turn = True


while not board.is_checkmate() or not board.is_stalemate():
    if player_turn:
        move = chess.Move.from_uci(input())
        if move in board.legal_moves:
            board.push(move)
            player_turn = False
    else:
        result = engine.play(board, chess.engine.Limit(time=1))
        board.push(result.move)
        player_turn = True
    
        print(board)
    
print("checkmate" if board.is_checkmate() else "stalemate")