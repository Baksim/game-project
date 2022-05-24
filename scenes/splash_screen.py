import pygame
import time
from . import menu
from pygame.locals import *


def run(game):
    title = game.fonts["title"].render("(Not) Friends Inc.", True, (0, 0, 0))
    start = time.time()
    while time.time() - start < 4:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            elif event.type == pygame.USEREVENT:
                game.reload_music()
            elif event.type == VIDEORESIZE and game.settings["fullscreen"] != "True":
                pygame.display.set_mode((max(event.dict['size'][0], 1300), max(event.dict['size'][1], 850)), RESIZABLE)
                pygame.display.update()
            elif event.type == VIDEOEXPOSE and game.settings["fullscreen"] != "True":
                pygame.display.set_mode((max(game.screen.get_size()[0], 1300), max(game.screen.get_size()[1], 850)), RESIZABLE)
                pygame.display.update()
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        game.screen.blit(title, title.get_rect(center=(size_x/2, size_y/2)))
        pygame.display.update()   
    if game.settings["bgm"] == "True":
        game.play_music(game.settings)
    menu.run(game)