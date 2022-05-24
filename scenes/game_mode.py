import pygame
from pygame.locals import *
from .components.button import Button
from . import settings, menu, VSAIOptions

      
def run(game):
    title = game.fonts["header"].render("Chess Multiplayer", True, (0, 0, 0))
    running = True
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        btns = [Button(game, (size_x // 2 - 200, size_y // 2.5 - 50), (400, 100), "Multiplayer", settings),
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 100 + size_y // 50), (400, 100), "Hotseat", settings),
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 200 + size_y // 25), (400, 100), "VS AI ", VSAIOptions),
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 300 + size_y // (50 / 3)), (400, 100), "Back ", menu)
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
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    btn.redirect(pos)
        pygame.display.update()    