import pygame
from pygame.locals import *
from .components.button import Button
from .components.chessboard import CBoard
from .components.chessboard_drawer import ChessboardDrawer
import pygame_widgets
from pygame_widgets.textbox import TextBox
import chess

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

def promote_loop(cboard):
    while True:
        print("pls choose a promotion piece")
        p = None
        cboard.promote(p)

def outcome_loop(outcome):
    while True:
        print(f"The outcome is {outcome}")

def run(game):
    player_move = ""
    running = True
    cboard = CBoard()
    board = chess.Board()
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
    player_turn = True
    is_white = True
    cd = ChessboardDrawer(game, is_white)
    cd.draw(cboard, fields)
    winner = None
    outcome = None

    while running:
        game.screen.fill(game.colors["main"])
        events = pygame.event.get()
        pygame_widgets.update(events)
        for event in events:
            let = get_let(cd.rect, is_white, pygame.mouse.get_pos()[0], list(fields.keys()))
            num = get_num(cd.rect, is_white, pygame.mouse.get_pos()[1])
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if let and num and (let + str(num) != player_move):
                    player_move += let + str(num)
            if event.type == VIDEORESIZE or event.type == VIDEOEXPOSE:
                cd.resize()
                size_x, size_y = game.screen.get_size()

        if len(player_move) >= 4:
            if cboard.is_promotion():
                promote_loop(cboard)
            player_move = chess.Move.from_uci(player_move)
            if player_move in board.legal_moves:
                board.push(player_move)
                cboard.push(str(player_move))
                player_turn = not player_turn
            player_move = ""
            is_white = not is_white
            cd.is_white = is_white

        cd.draw(cboard, fields, (player_move if len(player_move) == 2 else False))
        game.coursor()
        pygame.display.update()

        if board.outcome() is not None:
            if board.outcome().winner is not None:
                winner = board.outcome().winner
                if (is_white and winner) or (not is_white and not winner):
                    outcome = "win"
                else:
                    outcome = "lose"
            else:
                outcome = "draw"
            running = False
            outcome_loop(outcome)
