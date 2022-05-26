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
        self.is_connectd = False
        self.player_color = None
        self.join_code = None
        self.turn = None
        self.ws = WebSocketApp("wss://ws-chess-server.herokuapp.com/", on_message=self.on_message, on_error=self.on_error, on_close=self.on_close, on_open=self.on_open)
        self.session_id = session_id

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
            self.is_connected = True
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