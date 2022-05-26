import pygame
from pygame.locals import *
from .components.ws_interface import WsInterface
import time
from websocket import WebSocketConnectionClosedException, enableTrace
from threading import *

def run(game, key):
    game.screen.fill(game.colors["main"])
    pygame.display.update()
    enableTrace(True)
    ws = WsInterface(game, game.session_id)
    wst = Thread(target=ws.ws.run_forever)
    wst.daemon = True
    wst.start()
    pygame.time.delay(2000)
    if key:
        try:
            response = ws.join_game(key)
        except WebSocketConnectionClosedException:
            pygame.time.delay(2000)
            response = ws.join_game(key)
        pygame.time.delay(1000)
        if response["status"] == "ERROR":
            start = time.time()
            title = game.fonts["text"].render("Incorrect room key!!!", True, game.colors["accent"])
            while time.time() - start < 2:
                for event in pygame.event.get():
                    game.event_handler(event)
                game.screen.fill(game.colors["main"])
                size_x, size_y = game.screen.get_size()
                game.screen.blit(title, title.get_rect(center=(size_x/2, size_y/2)))
                pygame.display.update()
                return
    else:
        try:
            ws.init_game()
        except WebSocketConnectionClosedException:
            pygame.time.delay(2000)
            response = ws.init_game()
        while ws.join_code is None:
            game.screen.fill(game.colors["main"])
            events = pygame.event.get()
            for event in events:
                game.event_handler(event)
            pygame.display.update()
        title = game.fonts["text"].render("Waiting for opponent.", True, (0, 0, 0))
        code = game.fonts["title"].render(f"{ws.join_code}", True, (0, 0, 0))
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
