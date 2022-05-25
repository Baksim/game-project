import pygame

class Button:
    def __init__(self, game, coords, size, text, scene):
        self.text = text
        self.rect =  pygame.Rect(coords, size)
        self.second_rect = pygame.Rect((coords[0] - 5, coords[1] - 5), (size[0] + 10, size[1] + 10))
        self.game = game
        self.scene = scene
        
    def draw(self):
        size_x, size_y = self.game.screen.get_size()
        pos = pygame.mouse.get_pos()
        pygame.draw.rect(self.game.screen, self.game.colors["button_border"], self.second_rect, 0, 10)
        pygame.draw.rect(self.game.screen, self.game.colors["button_bg"], self.rect, 0, 10)
        if self.rect.collidepoint(pos[0], pos[1]):
            text = self.game.fonts["btn"].render(self.text, True, self.game.colors["red"])
        else:
            text = self.game.fonts["btn"].render(self.text, True, self.game.colors["button_text"])
        self.game.screen.blit(text, text.get_rect(center=(self.rect.center)))
    def redirect(self, pos):
        if self.rect.collidepoint(pos):
            self.scene.run(self.game)