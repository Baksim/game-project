import chess
import pygame
from pygame.locals import *
from .components.chessboard import CBoard
from .components.chessboard_drawer import ChessboardDrawer
from .components.ws_interface import WsInterface
import time
from websocket import WebSocketConnectionClosedException, enableTrace
from threading import *
from .components.result_log import show
from . import menu, MPOptions

def get_let(board, is_white, x, b_keys):
    if pygame.mouse.get_focused() != 0:
        index = (x - board.x) // (board.width // 8)
        if -1 < index < len(b_keys):
            if is_white:
                return b_keys[index]
            else:
                b_keys.reverse()
                return b_keys[index]
        return None

def get_num(board, is_white, y):
    if pygame.mouse.get_focused() != 0:
        if board.top <= y <= board.bottom:
            if is_white:
                return 8 - (y - board.top) // (board.width // 8)
            else:
                return (y - board.top) // (board.width // 8) + 1
        return None

def run(game, key):
    game.screen.fill(game.colors["main"])
    pygame.display.update()
    enableTrace(True)
    ws = WsInterface(game, game.session_id)
    wst = Thread(target=ws.ws.run_forever)
    wst.daemon = True
    wst.start()
    pygame.time.delay(2000)
    print(key)
    if key:
        try:
            ws.join_game(key)
        except WebSocketConnectionClosedException:
            pygame.time.delay(2000)
            ws.join_game(key)
        pygame.time.delay(1000)
        response = ws.last_error
        while not ws.is_connected:
            if response is not None:
                response = None
                ws.last_error = None
                start = time.time()
                title = game.fonts["text"].render("Incorrect room key!!!", True, game.colors["accent"])
                while time.time() - start < 2:
                    for event in pygame.event.get():
                        game.event_handler(event)
                    game.screen.fill(game.colors["main"])
                    size_x, size_y = game.screen.get_size()
                    game.screen.blit(title, title.get_rect(center=(size_x/2, size_y/2)))
                    pygame.display.update()
                menu.run(game)
            return
    else:
        try:
            ws.init_game()
        except WebSocketConnectionClosedException:
            pygame.time.delay(2000)
            ws.init_game()
        while ws.join_code is None:
            game.screen.fill(game.colors["main"])
            events = pygame.event.get()
            for event in events:
                game.event_handler(event)
            pygame.display.update()
        title = game.fonts["text"].render("Waiting for opponent.", True, (0, 0, 0))
        code = game.fonts["readable"].render(f"{ws.join_code}", True, (0, 0, 0))
        counter = 0
        while not ws.is_connected:
            game.screen.fill(game.colors["main"])
            events = pygame.event.get()
            for event in events:
                game.event_handler(event)
            if counter // 1000 == counter / 1000:
                title = game.fonts["text"].render("Waiting for opponent.", True, (0, 0, 0))
            if counter // 2000 == counter / 2000:
                title = game.fonts["text"].render("Waiting for opponent...", True, (0, 0, 0))
            if counter // 3000 == counter / 3000:
                title = game.fonts["text"].render("Waiting for opponent.....", True, (0, 0, 0))
            size_x, size_y = game.screen.get_size()
            game.screen.blit(title, (size_x/3, size_y/3))
            game.screen.blit(code, code.get_rect(center=(size_x/2, size_y/2)))
            game.coursor()
            pygame.display.update()
            counter += 1
    ws.last_error = None
    player_move = ""
    fields = {
        "a": [None, None, None, None, None, None, None, None],
        "b": [None, None, None, None, None, None, None, None],
        "c": [None, None, None, None, None, None, None, None],
        "d": [None, None, None, None, None, None, None, None],
        "e": [None, None, None, None, None, None, None, None],
        "f": [None, None, None, None, None, None, None, None],
        "g": [None, None, None, None, None, None, None, None],
        "h": [None, None, None, None, None, None, None, None]
    }
    cboard = CBoard()
    cd = ChessboardDrawer(game, ws.player_color)
    running = True
    while running:
        game.screen.fill(game.colors["main"])
        events = pygame.event.get()
        for event in events:
            let = get_let(cd.rect, ws.player_color, pygame.mouse.get_pos()[0], list(fields.keys()))
            num = get_num(cd.rect, ws.player_color, pygame.mouse.get_pos()[1])
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if let and num and (let + str(num) != player_move) and ws.turn:
                    player_move += let + str(num)
            if event.type == VIDEORESIZE or event.type == VIDEOEXPOSE:
                cd.resize()

        if ws.turn:
            if len(player_move) >= 4:
                player_move_new = chess.Move.from_uci(player_move)
                if player_move_new in ws.board.legal_moves or chess.Move.from_uci(player_move + "q") in ws.board.legal_moves:
                    cboard.push(player_move)
                    if cboard.is_promotion():
                        player_move_new = chess.Move.from_uci(player_move + "q")
                    ws.board.push(player_move_new)
                    cboard.promote("q")
                    ws.send_move(player_move_new)
                    ws.turn = not ws.turn
                    pygame.mixer.Sound.play(game.sound)
                player_move = ""
        if len(ws.received_moves) > 0:
            for i in range(len(ws.received_moves)):
                ws.board.push(chess.Move.from_uci(ws.received_moves[i][0]))
                cboard.push(str(chess.Move.from_uci(ws.received_moves[i][0])))
                if ws.received_moves[i][1] == ws.player_color:
                    ws.turn = True
                del ws.received_moves[i]
                pygame.mixer.Sound.play(game.sound)
                cboard.promote("q")
        cd.draw(cboard, fields, (player_move if len(player_move) == 2 and ws.turn else False))
        game.coursor()
        pygame.display.update()
        if ws.outcome is not None:
            outcome = None
            print("Hello??")
            if ws.outcome[0] == "win":
                winner = ws.outcome[1]
                if (ws.player_color and winner) or (not ws.player_color and not winner):
                    outcome = "Victory"
                else:
                    outcome = "Defeat"
            else:
                outcome = "Draw"
            running = False
            print(ws.outcome)
            print(outcome, type(outcome))
            show(game, str(outcome), [game.user["username"], game.opponent["username"]],
                 [game.user["score"], game.opponent["score"]])

