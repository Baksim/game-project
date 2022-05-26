import pygame

class ChessboardDrawer:
    def __init__(self, game, is_white):
        self.game = game
        size_x, size_y = self.game.screen.get_size() 
        self.rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
        self.under_rect = pygame.Rect((self.rect.x - 20, self.rect.y - 20), (self.rect.width + 40, self.rect.height + 40))
        self.is_white = is_white
        self.imgs = game.load_images(self.rect.width // 8)
        
    def set_is_white(self, is_white):
        self.is_white = is_white
        
    def reload_imgs(self):
        self.imgs = self.game.load_images(self.rect.width // 8)
        
    def draw_board(self, rects):
        size = self.rect.width // 8
        color = self.is_white
        for i, let in enumerate(rects):
            for j in range(8):
                if self.is_white:
                    rects[let][j] = pygame.Rect(self.rect.x + size * i, self.rect.bottom - size * (j + 1), size, size)
                else:
                    rects[let][j] = pygame.Rect(self.rect.right - size * (i + 1), self.rect.top + size * j, size, size)
        for let in rects:
            for i in range(8):
                if color:
                    pygame.draw.rect(self.game.screen, "#6D2900", rects[let][i])
                else:
                    pygame.draw.rect(self.game.screen, "#E1B494", rects[let][i])
                color = not color
            color = not color
        
    def draw_pices(self, cboard, rects):
        board_fields = cboard.get_board()
        for let in board_fields:
            for i in range(1, 9):
                if board_fields[let][i][1] == "w":
                    self.game.screen.blit(self.imgs["w"][board_fields[let][i][0]], rects[let][i - 1].topleft)
                elif board_fields[let][i][1] == "b":
                    self.game.screen.blit(self.imgs["b"][board_fields[let][i][0]], rects[let][i - 1].topleft)
    
    def resize(self):
        size_x, size_y = self.game.screen.get_size() 
        self.rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
        self.under_rect = pygame.Rect((self.rect.x - 20, self.rect.y - 20), (self.rect.width + 40, self.rect.height + 40))
        self.reload_imgs()
        
    def draw(self, cboard, rects, picked=None):
        pygame.draw.rect(self.game.screen, self.game.colors["gray"], self.under_rect)
        self.draw_board(rects)
        if picked:
            pygame.draw.rect(self.game.screen, self.game.colors["accent"], rects[picked[0]][int(picked[1]) - 1])
        self.draw_pices(cboard, rects)