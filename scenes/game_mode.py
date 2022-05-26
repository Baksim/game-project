import pygame
from pygame.locals import *
from .components.button import Button
from . import settings, menu, VSAIOptions, MPOptions, hotseat

      
def run(game):
    title = game.fonts["header"].render("Chess Multiplayer", True, (71, 32, 24))
    running = True
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        multiplayer_btn = Button(game, (size_x // 2 - 200, size_y // 2.5 - 50), (400, 100), "Multiplayer", MPOptions)
        btns = [
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 100 + size_y // 25), (400, 100), "VS AI ", VSAIOptions),
                Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 200 + size_y // (50 / 3)), (400, 100), "Back ", menu)
                ]
        title_rect = pygame.Rect((0, size_y // 60), (size_x, size_y // 10))
        pygame.draw.rect(game.screen, game.colors["tertiary"], title_rect)
        pygame.draw.rect(game.screen, game.colors["secondary"], pygame.Rect(0, size_y // 30 + size_y // 10, size_x, size_y // 10))
        game.screen.blit(title, title.get_rect(center=(title_rect.center)))
        for btn in btns:
            btn.draw()
        if game.session_id != "Guest":
            multiplayer_btn.draw()
        
        for event in pygame.event.get():
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    btn.redirect(pos)
                if game.session_id != "Guest":
                    multiplayer_btn.redirect(pos)
                    
        if game.session_id == "Guest":
            size_x, size_y = game.screen.get_size()
            pos = pygame.mouse.get_pos()
            pygame.draw.rect(game.screen, game.colors["button_border"], multiplayer_btn.second_rect, 0, 10)
            pygame.draw.rect(game.screen, game.colors["button_bg"], multiplayer_btn.rect, 0, 10)
            text = game.fonts["btn"].render(multiplayer_btn.text, True, game.colors["gray"])
            game.screen.blit(text, text.get_rect(center=(multiplayer_btn.rect.center)))
        game.coursor()
        pygame.display.update()    