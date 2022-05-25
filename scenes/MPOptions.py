import pygame
from pygame.locals import *
from .components.button import Button
from . import game_mode, VSAIGame, matchmaking, room_game
import pygame_widgets
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.textbox import TextBox
from pygame_widgets.button import Button as pwb
import random

def start_room(game, key=None):
    print("Room is loading...")
    
def start_matchmaking(game, what):
    print("Matcmking is loading...")

def run(game):
    title = game.fonts["header"].render("Multiplayer", True, (0, 0, 0))
    create_room_btn = pwb(game.screen, 100, 100, 400, 50,  
        text='Create a room',
        font=game.fonts["small_text"],
        radius=20,
        onClick=start_room,
        onClickParams=(game, True)
)
    join_room_filed = TextBox(game.screen, 500, 100, 800, 50, font=game.fonts["small_text"], fontSize=50, textColour=(0, 0, 0),
                  onSubmit=start_room, onSubmitParams=(game, True), radius=20, borderThickness=5)
    matchmaking_btn = pwb(game.screen, 100, 100, 400, 50,  
        text='Start matchmaking',
        font=game.fonts["small_text"],
        radius=20,
        onClick=start_matchmaking,
        onClickParams=(game, True))
    running = True
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        back_btn = Button(game, (size_x // 2 - 200, (size_y // 2.5 - 50) + 400 + size_y // (50 / 3)), (400, 75), "Back ", game_mode)
        title_rect = pygame.Rect((0, size_y // 60), (size_x, size_y // 10))
        
        join_room_filed.setWidth(int(size_x // 3))
        join_room_filed.setX(int(size_x // 2 - join_room_filed.getWidth() // 2))
        join_room_filed.setY(int(size_y // 2.5))
        create_room_btn.setWidth(int(size_x // 3))
        create_room_btn.setX(int(size_x // 2 - create_room_btn.getWidth() // 2))
        create_room_btn.setY(int(size_y // 2.5 - (create_room_btn.getHeight() + 30)))
        matchmaking_btn.setX(int(size_x // 2 - matchmaking_btn.getWidth() // 2))
        matchmaking_btn.setY(int(join_room_filed.getY() + (join_room_filed.getHeight() + 30)))
        
        pygame.draw.rect(game.screen, game.colors["tertiary"], title_rect)
        pygame.draw.rect(game.screen, game.colors["secondary"], pygame.Rect(0, size_y // 30 + size_y // 10, size_x, size_y // 10))
        game.screen.blit(title, title.get_rect(center=(title_rect.center)))
        back_btn.draw()
        
        for event in pygame.event.get():
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_btn.rect.collidepoint(pygame.mouse.get_pos()):
                    running = False
                    
        pygame_widgets.update(pygame.event.get())
        game.coursor()
        pygame.display.update()    
        
    create_room_btn.hide()
    join_room_filed.hide()
    matchmaking_btn.hide()
    create_room_btn.disable()
    join_room_filed.disable()
    matchmaking_btn.disable()