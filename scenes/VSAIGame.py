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
                rects[let][j] = pygame.Rect(rec.x + size * i, rec.bottom - size * (j + 1), size, size)
            else:
                rects[let][j] = pygame.Rect(rec.right - size * (i + 1), rec.top + size * j, size, size)
    for let in rects:
        for i in range(8):
            if color:
                pygame.draw.rect(game.screen, "#6D2900", rects[let][i])
            else:
                pygame.draw.rect(game.screen, "#E1B494", rects[let][i])
            color = not color
        color = not color
    
def draw_pices(g, cboard, rects, imgs):
    board_fields = cboard.get_board()
    for let in board_fields:
        for i in range(1, 9):
            if board_fields[let][i][1] == "w":
                g.screen.blit(imgs["w"][board_fields[let][i][0]], rects[let][i - 1].topleft)
            elif board_fields[let][i][1] == "b":
                g.screen.blit(imgs["b"][board_fields[let][i][0]], rects[let][i - 1].topleft)
                

def get_let(board, is_white, x, b_keys):    
    if pygame.mouse.get_focused() != 0:
        index = (x - board.x) // (board.width // 8)
        if -1 < index < len(b_keys):
            if is_white:
                return b_keys[index]
            else:
                b_keys.reverse()
                return b_keys[index]
        return None

def get_num(board, is_white, y): 
    if pygame.mouse.get_focused() != 0:  
        if board.top <= y <= board.bottom:
            if is_white:
                return 8 - (y - board.top) // (board.width // 8)
            else:
                return (y - board.top) // (board.width // 8) + 1
        return None
        

def run(game, difficulty, is_white):
    running = True
    engine = game.get_engine()
    cboard = CBoard()
    board = chess.Board()
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
    let  = get_let(board_rect, is_white, pygame.mouse.get_pos()[0], list(fields.keys()))
    imgs = game.load_images_vsbot(board_rect.width // 8)
    draw_board(game, board_rect, fields, is_white)
    draw_pices(game, cboard, fields, imgs)
    player_move = ""
    
    while running:
        for event in pygame.event.get():
            let  = get_let(board_rect, is_white, pygame.mouse.get_pos()[0], list(fields.keys()))
            num = get_num(board_rect, is_white, pygame.mouse.get_pos()[1])
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = pygame.mouse.get_pos()
                if let and num and (let + str(num) != player_move) and player_turn:
                    player_move += let + str(num)
            if event.type == VIDEORESIZE or event.type == VIDEOEXPOSE:
                imgs = game.load_images_vsbot(board_rect.width // 8)
                    
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size() 
        under_board_rect = pygame.Rect((board_rect.x - 20, board_rect.y - 20), (board_rect.width + 40, board_rect.height + 40))
        board_rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
        pygame.draw.rect(game.screen, game.colors["gray"], under_board_rect)
        pygame_widgets.update(pygame.event.get())
        
        if player_turn:
            if len(player_move) == 2:
                fields[player_move[0]][int(player_move[1]) - 1]
            if len(player_move) == 4:
                player_move = chess.Move.from_uci(player_move)
                if player_move in board.legal_moves:
                    board.push(player_move)
                    cboard.push(str(player_move))
                    player_turn = not player_turn
                player_move = ""
                
        else:
            result = engine.play(board, chess.engine.Limit(time=0))
            board.push(result.move)
            cboard.push(str(result.move))
            player_turn = not player_turn
        draw_board(game, board_rect, fields, is_white)
        if len(player_move) == 2 and player_turn:
            pygame.draw.rect(game.screen, game.colors["accent"], fields[player_move[0]][int(player_move[1]) - 1])
        draw_pices(game, cboard, fields, imgs)
        game.coursor()
        pygame.display.update()