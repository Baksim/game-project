import pygame
from pygame.locals import *
from .components.button import Button
from .components.chessboard import CBoard
import pygame_widgets
from pygame_widgets.textbox import TextBox
import chess
import chess.engine


def draw_board(game, rec, rects, is_white):
    size = rec.width // 8
    color = is_white
    for i, let in enumerate(rects):
        for j in range(8):
            if is_white:
                rects[let][j] = pygame.Rect(rec.x + size * i, rec.y + rec.height - size * j, size, size)
            else:
                rects[let][j] = pygame.Rect(rec.x + size * i, rec.y + size * j, size, size)
    for let in rects:
        for i in range(8):
            if color:
                pygame.draw.rect(game.screen, (255, 255, 255), rects[let][i])
            else:
                pygame.draw.rect(game.screen, (0, 0, 0), rects[let][i])
            color = not color
        color = not color
    
def draw_pices(g, cboard, rects, is_white):
    pass

def run(game, difficulty, is_white):
    running = True
    engine = game.get_engine()
    cboard = CBoard()
    size_x, size_y = game.screen.get_size()
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
    engine.configure({"Skill Level": difficulty})
    player_turn = is_white
    board_rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
    under_board_rect = pygame.Rect((board_rect.x - 20, board_rect.y - 20), (board_rect.width + 40, board_rect.height + 40))
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size() 
        for event in pygame.event.get():
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                
        under_board_rect = pygame.Rect((board_rect.x - 20, board_rect.y - 20), (board_rect.width + 40, board_rect.height + 40))
        board_rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
        pygame.draw.rect(game.screen, game.colors["gray"], under_board_rect)
        draw_board(game, board_rect, fields, is_white)
        pygame_widgets.update(pygame.event.get())
        game.coursor()
        pygame.display.update()