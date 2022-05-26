import pygame
from pygame.locals import *
from .components.ws_interface import WsInterface
import time

def run(game, key):
    game.screen.fill(game.colors["main"])
    pygame.display.update()
    ws = WsInterface(game, game.session_id)
    pygame.time.delay(2000)
    if key:
        response = ws.join_game(key)
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
        ws.init_game()
        game.screen.fill(game.colors["main"])
        start = time.time()
        title = game.fonts["text"].render("Waiting for oponent.", True, (0, 0, 0))
        while not ws.is_connected:
            if (time.time() - start) // 2 == (time.time() - start) / 2:
                title = game.fonts["text"].render("Waiting for opponent.", True, (0, 0, 0))
            if (time.time() - start) // 4 == (time.time() - start) / 4:
                title = game.fonts["text"].render("Waiting for opponent...", True, (0, 0, 0))
            if (time.time() - start) // 6 == (time.time() - start) / 6:
                title = game.fonts["text"].render("Waiting for opponent.....", True, (0, 0, 0))
            game.screen.blit(title, title.get_rect(center=(size_x/2, size_y/2)))
            pygame.display.update()