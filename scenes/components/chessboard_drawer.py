import pygame

class ChessboardDrawer:
    def __init__(self, game, rect, is_white):
        self.game = game
        self.rect = rect
        self.is_white = is_white
        self.imgs = game.load_images_vsbot(self.rect.width // 8)
        
    def set_is_white(self, is_white):
        self.is_white = is_white
        
    def set_rect(self, rect):
        self.rect = rect
        self.reload_imgs()
        
    def reload_imgs(self):
        self.imgs = self.game.load_images_vsbot(self.rect.width // 8)
        
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