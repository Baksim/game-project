import pygame

class ChessboardDrawer:
    def __init__(self, game, is_white):
        self.game = game
        size_x, size_y = self.game.screen.get_size() 
        self.rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
        self.under_rect = pygame.Rect((self.rect.x - 20, self.rect.y - 20), (self.rect.width + 45, self.rect.height + 45))
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
                    
    def draw_symb(self, rects):
        for i, let in enumerate(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']):
            let = self.game.fonts["small_text"].render(let, True, (0, 0, 0))
            num = self.game.fonts["small_text"].render(str(i + 1), True, (0, 0, 0)) if self.is_white else self.game.fonts["small_text"].render(str(8 - i), True, (0, 0, 0))
            self.game.screen.blit(let, let.get_rect(center=(self.rect.left + self.rect.width //16 + self.rect.width //8 * i, self.rect.bottom + 11)))
            self.game.screen.blit(num, let.get_rect(center=(self.rect.left - 12, self.rect.bottom - self.rect.width //16 - self.rect.width //8 * i)))
                 
    def resize(self):
        size_x, size_y = self.game.screen.get_size() 
        self.rect = pygame.Rect((size_x // 2 - (size_y // 2 - int(size_y*0.1)), int(size_y*0.1)), (int(size_y*0.8), int(size_y*0.8)))
        self.under_rect = pygame.Rect((self.rect.x - 20, self.rect.y - 20), (self.rect.width + 45, self.rect.height + 45))
        self.reload_imgs()
        
    def draw(self, cboard, rects, picked=None):
        pygame.draw.rect(self.game.screen, self.game.colors["gray"], self.under_rect)
        self.draw_board(rects)
        self.draw_symb(rects)
        if picked:
            pygame.draw.rect(self.game.screen, self.game.colors["accent"], rects[picked[0]][int(picked[1]) - 1])
        self.draw_pices(cboard, rects)
        
    def get_promotion(self, cboard, rects):
        while True:
            self.game.screen.fill(self.game.colors["main"])
            size_x, size_y = self.game.screen.get_size() 
            picks = {
            "q": pygame.Rect((self.under_rect.x - self.rect.width // 8 - 20, self.rect.top), (int(size_y*0.8), int(size_y*0.8))),
            "r": pygame.Rect((self.under_rect.x - self.rect.width // 8 - 20, self.rect.top + (self.rect.width // 8)*2), (int(size_y*0.8), int(size_y*0.8))),
            "b": pygame.Rect((self.under_rect.x - self.rect.width // 8 - 20, self.rect.top + (self.rect.width // 8)*3), (int(size_y*0.8), int(size_y*0.8))),
            "n": pygame.Rect((self.under_rect.x - self.rect.width // 8 - 20, self.rect.top + (self.rect.width // 8)*4), (int(size_y*0.8), int(size_y*0.8)))
            }
            
            for key in picks:
                self.game.screen.blit(self.imgs["w" if self.is_white else "b"][key], picks[key].topleft)
            for event in pygame.event.get():
                self.game.event_handler(event)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for key in picks:
                        if picks[key].collidepoint(pygame.mouse.get_pos()):
                            print(key)
                            return key
                
            self.draw_board(rects)
            self.draw_symb(rects)
            self.draw_pices(cboard, rects)
            
            self.game.coursor()