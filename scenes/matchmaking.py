import time
import chess
import json
from pygame.locals import *
import pygame_widgets
from websocket import *
from threading import *
from multiprocessing import Process
import pygame.time

from .VSAIGame import get_num, get_let
from .components.chessboard import CBoard
from .components.chessboard_drawer import ChessboardDrawer
from .components.ws_interface import WsInterface

# def connection(game, session_id):
#     enableTrace(True)
#     ws.on_open = on_open
#     print("starting ws???")
#     ws.run_forever()
#     print("are you not running forever, son?")

def run(game):
    session_id = game.session_id
    enableTrace(True)
    # t = Thread(target=connection, args=(game, session_id))
    # t.start()
    ws = WsInterface(game, session_id)
    wst = Thread(target=ws.ws.run_forever)
    wst.daemon = True
    wst.start()
    pygame.time.delay(1000)
    while not ws.is_connected:
        events = pygame.event.get()
        for event in events:
            game.event_handler(event)
        game.screen.fill(game.colors["main"])
        print("LOADING!!!!!!!!!!!")
        
    ws.match()
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            game.event_handler(event)
        game.screen.fill(game.colors["strong_accent"])
    

    print("Matchmaking is loading...")


