import pygame
from pygame.locals import *
from .components.button import Button
from . import game_mode, VSAIGame
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.textbox import TextBox
import random

def run(game):
    title = game.fonts["header"].render("VS AI Game", True, (0, 0, 0))
    running = True
    slider = Slider(game.screen, 100, 100, 800, 20, min=1, max=20, step=1, handleRadius=12, initial=10)
    output = TextBox(game.screen, 475, 300, 50, 50, font=game.fonts["small_text"])
    clr_text = TextBox(game.screen, 475, 300, 300, 50, font=game.fonts["small_text"])
    clr = Dropdown(
        game.screen, 120, 10, 300, 50, name="Random",
        choices=[
            'Random',
            'Black',
            'White'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['Random', 'Black', 'White'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
        )
    output.disable()
    clr_text.disable()
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        
        play_btn = Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 300 + size_y // (50 / 3)), (400, 75), "Play ", VSAIGame)
        back_btn = Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 400 + size_y // (50 / 3)), (400, 75), "Back ", game_mode)
        title_rect = pygame.Rect((0, size_y // 60), (size_x, size_y // 10))
        
        slider.setWidth(int(size_x // 3))
        slider.setX(int(size_x // 2 - slider.getWidth() // 2))
        slider.setY(int(size_y // 2.5))
        output.setWidth(int(size_x // 3))
        output.setX(int(size_x // 2 - output.getWidth() // 2))
        output.setY(int(size_y // 2.5 - (output.getHeight() + 30)))
        clr_text.setX(int(size_x // 2 - clr_text.getWidth() - 30))
        clr_text.setY(int(slider.getY() + (slider.getHeight() + 30)))
        clr.setX(int(size_x // 2 + 30))
        clr.setY(clr_text.getY())
        
        pygame.draw.rect(game.screen, game.colors["tertiary"], title_rect)
        pygame.draw.rect(game.screen, game.colors["secondary"], pygame.Rect(0, size_y // 30 + size_y // 10, size_x, size_y // 10))
        game.screen.blit(title, title.get_rect(center=(title_rect.center)))
        back_btn.draw()
        play_btn.draw()
        
        for event in pygame.event.get():
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                elif play_btn.rect.collidepoint(pygame.mouse.get_pos()):
                    slider.hide()
                    output.hide()
                    clr_text.hide()
                    clr.hide()
                    slider.disable()
                    clr.disable()
                    if not clr.getSelected() or clr.getSelected() == "Random":
                        is_white = random.choice([True, False])
                    else:
                        is_white = True if clr.getSelected() == "White" else False
                    VSAIGame.run(game, slider.getValue(), is_white)
                    slider.show()
                    output.show()
                    clr_text.show()
                    clr.show()
                    slider.enable()
                    clr.enable()
                    
        pygame_widgets.update(pygame.event.get())
        output.setText("Difficulty level: " + str(slider.getValue()))
        clr_text.setText("Your color: " + (clr.getSelected() if clr.getSelected() else "Random"))
        game.coursor()
        pygame.display.update()    
        
    slider.hide()
    output.hide()
    clr_text.hide()
    clr.hide()
    slider.disable()
    clr.disable()