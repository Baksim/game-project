import pygame


def show(game, outcome, nicks, rating):
    running = True
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        display = pygame.Rect((size_x // 4, size_y // 4), (size_x // 2, size_y // 4))
        pygame.draw.rect(game.screen, game.colors["gray"], display)
        outcome = game.fonts["text"].render(str(outcome), True, (0, 0, 0))
        player_1 = game.fonts["small_text"].render(str(nicks[0]) + ": " + str(rating[0]), True, (0, 0, 0))
        player_2 = game.fonts["small_text"].render(str(nicks[1]) + ": " + str(rating[1]), True, (0, 0, 0))
        hint = game.fonts["small_text"].render(("Click to proceed"), True, game.colors["secondary"])
        game.screen.blit(outcome, outcome.get_rect(center=(display.left + display.width/2, display.top + display.height/4)))
        game.screen.blit(player_1, (display.left + display.width // 3, display.top + display.height*2 // 4))
        game.screen.blit(player_2, (display.left + display.width // 3, display.top + display.height*2.5 // 4))
        game.screen.blit(hint, hint.get_rect(center=(display.left + display.width/2, display.top + display.height*3.5/4)))
        
        for event in pygame.event.get():
            game.event_handler(event)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                running = False
                
        game.coursor()
        pygame.display.update()