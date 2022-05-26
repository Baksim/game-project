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
    ws.match()
    
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
    
    while not ws.is_connected:
        game.screen.fill(game.colors["main"])
        events = pygame.event.get()
        for event in events:
            game.event_handler(event)
            
        game.coursor()
        pygame.display.update()   
        
    running = True
    while running:
        game.screen.fill(game.colors["main"])
        cd.draw(cboard, fields)
        events = pygame.event.get()
        for event in events:
            game.event_handler(event)
            if event.type == VIDEORESIZE or event.type == VIDEOEXPOSE:
                cd.resize()
        game.coursor()
        pygame.display.update()   
    

    print("Matchmaking is loading...")


