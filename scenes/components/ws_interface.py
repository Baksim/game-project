import chess
import json
import pygame
import pygame_widgets
from pygame.locals import *
from websocket import *
from .chessboard import CBoard
from .chessboard_drawer import ChessboardDrawer
from ..VSAIGame import get_let, get_num


class WsInterface:
    def __init__(self, game, session_id):
        self.game = game
        self.board = chess.Board()
        self.cboard = CBoard()
        self.running = False
        self.player_color = None
        self.join_code = None
        self.turn = None
        self.player_move = ""
        self.fields = {
            "a": [None, None, None, None, None, None, None, None],
            "b": [None, None, None, None, None, None, None, None],
            "c": [None, None, None, None, None, None, None, None],
            "d": [None, None, None, None, None, None, None, None],
            "e": [None, None, None, None, None, None, None, None],
            "f": [None, None, None, None, None, None, None, None],
            "g": [None, None, None, None, None, None, None, None],
            "h": [None, None, None, None, None, None, None, None]
        }
        self.ws = WebSocketApp("wss://ws-chess-server.herokuapp.com/", on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, on_open=self.on_open)
        self.session_id = session_id

        size_x, size_y = self.game.screen.get_size()

        self.board_rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y * 0.1)), int(size_y * 0.1)),
                                 (int(size_y * 0.8), int(size_y * 0.8)))
        self.under_board_rect = pygame.Rect((self.board_rect.x - 20, self.board_rect.y - 20),
                                       (self.board_rect.width + 40, self.board_rect.height + 40))
        self.cd = ChessboardDrawer(self.game, self.board_rect, self.player_color)

    def mainloop(self):
        while self.running:
            for event in pygame.event.get():
                let = get_let(self.board_rect, self.player_color, pygame.mouse.get_pos()[0], list(self.fields.keys()))
                num = get_num(self.board_rect, self.player_color, pygame.mouse.get_pos()[1])
                self.game.event_handler(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if let and num and (let + str(num) != self.player_move) and self.turn:
                        self.player_move += let + str(num)
                if event.type == VIDEORESIZE or event.type == VIDEOEXPOSE:
                    size_x, size_y = self.game.screen.get_size()
                    self.board_rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y * 0.1)), int(size_y * 0.1)),
                                                (int(size_y * 0.8), int(size_y * 0.8)))
                    self.under_board_rect = pygame.Rect((self.board_rect.x - 20, self.board_rect.y - 20),
                                                      (self.board_rect.width + 40, self.board_rect.height + 40))
                    self.cd.set_rect(self.board_rect)

            self.game.screen.fill(self.game.colors["main"])
            pygame.draw.rect(self.game.screen, self.game.colors["gray"], self.under_board_rect)
            pygame_widgets.update(pygame.event.get())

            if self.turn:
                if len(self.player_move) == 4:
                    player_move = chess.Move.from_uci(self.player_move)
                    if player_move in self.board.legal_moves:
                        self.board.push(player_move)
                        self.cboard.push(str(player_move))
                        self.ws.turn = not self.turn
                    self.player_move = ""

            else:
                # result = engine.play(board, chess.engine.Limit(time=0))
                # board.push(result.move)
                # cboard.push(str(result.move))
                # player_turn = not player_turn
                pass

            self.cd.draw_board(self.fields)
            if len(self.player_move) == 2 and self.turn:
                pygame.draw.rect(self.game.screen, self.game.colors["accent"],
                                 self.fields[self.player_move[0]][int(self.player_move[1]) - 1])
            self.cd.draw_pices(self.cboard, self.fields)

            self.game.coursor()
            pygame.display.update()

    def create(self):
        self.cd.draw_board(self.fields)
        self.cd.draw_pices(self.cboard, self.fields)
        self.running = True
        self.mainloop()

    def init_game(self):
        self.player_color = chess.WHITE
        event = {"type": "init", "session_id": self.session_id}
        self.ws.send(json.dumps(event))

    def join_game(self, join):
        self.player_color = chess.BLACK
        event = {"type": "init", "join": join, "session_id": self.session_id}
        self.ws.send(json.dumps(event))

    def match(self):
        event = {"type": "init", "match": "true", "session_id": self.session_id}
        print("hello???", event)
        self.ws.send(json.dumps(event))

    def on_click_join(self):
        join = None
        self.join_game(join)

    def send_move(self, move):
        event = {"type": "play", "code": move}
        self.ws.send(json.dumps(event))

    def on_click_send(self, ws):
        # move = p_txt.get()
        # if chess.Move.from_uci(move) in board.generate_legal_moves():
        #     send_move(ws, move)
        #     p_btn.configure(state="disabled")
        # else:
        #     print('Illegal move you dumdumb')
        pass

    def on_message(self, ws, message):
        msg = json.loads(message)
        if msg.get('join') is not None:
            self.join_code = msg['join']
            print(self.join_code)
        elif msg['type'] == "assign_color":
            print("Assigned a color")
            self.player_color = msg['color']
            self.turn = self.player_color
        elif msg['type'] == "announcement":
            self.create()
        elif msg['type'] == "play":
            move = chess.Move.from_uci(msg['code'])
            self.board.push(move)
            # brd.configure(text=board)
            # if msg['color'] == player_color:
            #     p_btn.configure(state="active")
        elif msg['type'] == "win":
            if msg['color'] == chess.WHITE:
                print("White won")
            else:
                print("Black won")
            self.ws.close()
        elif msg['type'] == "draw":
            print("Lol draw")
            self.ws.close()
        print("Received:" + message)
        pygame.display.update()

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")