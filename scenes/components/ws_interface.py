import chess
import json
import pygame
from websocket import *


class WsInterface:
    def __init__(self, game, session_id):
        self.game = game
        self.board = chess.Board()
        self.is_connected = False
        self.player_color = None
        self.join_code = None
        self.turn = None
        self.received_moves = []
        self.outcome = None
        self.last_error = None
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
        self.ws.send(json.dumps(event))

    def on_click_join(self):
        join = None
        self.join_game(join)

    def send_move(self, move):
        event = {"type": "play", "code": move}
        self.ws.send(json.dumps(event))

    def on_message(self, ws, message):
        msg = json.loads(message)
        if msg.get('join') is not None:
            self.join_code = msg['join']
            print(self.join_code)
        elif msg.get('status') is not None:
            print("poka")
        elif msg['type'] == 'error':
            self.last_error = msg['message']
        elif msg['type'] == "assign_color":
            print("Assigned a color")
            self.player_color = msg['color']
            self.turn = self.player_color
        elif msg['type'] == "announcement":
            self.is_connected = True
        elif msg['type'] == "play":
            self.received_moves.append([msg['code'], msg['color']])
        elif msg['type'] == "win":
            self.outcome = ["win", msg["color"]]
            self.ws.close()
        elif msg['type'] == "draw":
            self.outcome = ["draw"]
            self.ws.close()
        print("Received:" + message)

    def on_error(self, ws, error):
        print(error)

    def on_close(self, ws):
        print("### closed ###")

    def on_open(self, ws):
        print("Opened connection")