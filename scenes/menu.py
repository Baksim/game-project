import pygame
from pygame.locals import *
from .components.button import Button
from . import exit, settings, game_mode

      
def run(game):
    title = game.fonts["header"].render("Chess Multiplayer", True, (71, 32, 24))
    while True:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        btns = [Button(game, (size_x // 2 - 200, size_y // 2.5 - 50), (400, 100), "Play", game_mode),
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 100 + size_y // 50), (400, 100), "Settings", settings),
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 200 + size_y // 25), (400, 100), "Exit", exit)
                ]
        title_rect = pygame.Rect((0, size_y // 60), (size_x, size_y // 10))
        pygame.draw.rect(game.screen, game.colors["tertiary"], title_rect)
        pygame.draw.rect(game.screen, game.colors["secondary"], pygame.Rect(0, size_y // 30 + size_y // 10, size_x, size_y // 10))
        game.screen.blit(title, title.get_rect(center=(title_rect.center)))
        for btn in btns:
            btn.draw()
        game.coursor()
        for event in pygame.event.get():
            game.event_handler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    btn.redirect(pos)
        pygame.display.update()    