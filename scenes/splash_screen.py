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
            if event.type == pygame.USEREVENT:
                game.reload_music()
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        game.screen.blit(title, title.get_rect(center=(size_x/2, size_y/2)))
        pygame.display.update()   
    menu.run(game)