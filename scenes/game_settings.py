import pygame
import pygame_widgets as pw
from pygame_widgets.toggle import Toggle
from pygame_widgets.dropdown import Dropdown
import easygui
from . import menu, sound_settings
from pygame.locals import *


def set_value(param, value, sett):
    sett[param] = value

def run(game, new_settings=None, exit_sett=False):
    title = game.fonts["header"].render("Settings", True, (0, 0, 0))
    new_settings = game.settings.copy() if not new_settings else new_settings
    running = True if not exit_sett else False
    fs_dropdown = Dropdown(
        game.screen, 120, 10, 200, 80, name=new_settings["fullscreen"],
        choices=[
            'True',
            'False'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['True', 'False'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
        )
    resolution_dropdown = Dropdown(
        game.screen, 120, 10, 200, 80, name=new_settings["resolution"],
        choices=[
            '1920x1080',
            '1280x720',
            '854x480',
            '640x360'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['1920', '1280x720', '854x480', '640x360'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
    )
    style_dropdown = Dropdown(
        game.screen, 120, 10, 200, 80, name=new_settings["piece_style"],
        choices=[
            'Classic',
            'Africa',
            'Fairytale',
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['Classic', 'Africa', 'Fairytale'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
    )
    
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        title_rect = pygame.Rect((0, size_y // 60), (size_x, size_y // 10))
        pygame.draw.rect(game.screen, game.colors["tertiary"], title_rect)
        game.screen.blit(title, title.get_rect(center=(title_rect.center)))
        
        game_settings_rect = pygame.Rect((0, 7 * size_y // 60), (size_x // 4, 100))
        sound_settings_rect = pygame.Rect((0, 7 * size_y // 60 + 100), (size_x // 4, 100))
        pygame.draw.rect(game.screen, game.colors["secondary"], game_settings_rect)
        pygame.draw.rect(game.screen, game.colors["secondary"], sound_settings_rect)
        line_points = [(0, 7 * size_y // 60),
                       (size_x // 4, 7 * size_y // 60),
                       (size_x // 4, 7 * size_y // 60 + 100),
                       (0, 7 * size_y // 60 + 100),
                       (size_x // 4, 7 * size_y // 60 + 100),
                       (size_x // 4, 7 * size_y // 60 + 200),
                       (0, 7 * size_y // 60 + 200),
                       (size_x // 4, 7 * size_y // 60 + 200),
                       (size_x // 4, size_y),
                       (0, size_y)]
        pygame.draw.lines(game.screen, game.colors["gray"], True, line_points, 4)
        
        events = pygame.event.get()
        
        rects = [
        pygame.Rect((size_x // 4, size_y // 10), (size_x * 3 // 4, 100)),
        pygame.Rect((size_x // 4, size_y // 10 + 100), (size_x * 3 // 4, 100)),
        pygame.Rect((size_x // 4, size_y // 10 + 200), (size_x * 3 // 4, 100)),
        pygame.Rect((size_x // 4, size_y // 10 + 300), (size_x * 3 // 4, 100)),
        pygame.Rect((size_x // 4, size_y // 10 + 400), (size_x * 3 // 4, 100)),
        pygame.Rect((size_x // 4, size_y // 10 + 500), (size_x * 3 // 4, 100)),
    ]
        
        dropdowns = [fs_dropdown, resolution_dropdown, style_dropdown]
        dropdown_names = ["fullscreen", "resolution", "piece_style"]
        for i, dropdown in enumerate(dropdowns):
            dropdown._x, dropdown._y = rects[i].midright[0] - 250, rects[i].midright[1] + 10
            if dropdown.getSelected():
                set_value(dropdown_names[i], dropdown.getSelected(), new_settings)
        
        text_game = game.fonts["btn"].render("Game", True, game.colors["strong_accent"])
        game.screen.blit(text_game, text_game.get_rect(center=(game_settings_rect.center)))
        if sound_settings_rect.collidepoint(pygame.mouse.get_pos()):
            text_sound = game.fonts["btn"].render("Sound", True, game.colors["accent"])
        else:
            text_sound = game.fonts["btn"].render("Sound", True, (0, 0, 0))
        game.screen.blit(text_sound, text_sound.get_rect(center=(sound_settings_rect.center)))
        
        options = ["Fullscreen", "Resolution", "Piece style"]
        for i, text in enumerate(options):
            text = game.fonts["text"].render(text, True, (0, 0, 0))
            game.screen.blit(text, (rects[i].midleft[0] + 50, rects[i].midleft[1]))
        for event in events:
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game.rest_settings()
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and sound_settings_rect.collidepoint(pygame.mouse.get_pos()):
                new_settings, running = sound_settings.run(game, new_settings)
                
        pw.update(events)
        
        game.coursor()
        pygame.display.update() 
            
    
"""
def run(game):
    import easygui
    d = easygui.diropenbox("Hello!", "Music path")
    print(d)
    title = game.fonts["title"].render("Settings", True, (0, 0, 0))
    running = True
    root = tk.Tk()
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    folder_path = filedialog.askdirectory()
    print(folder_path)
    frame = HtmlFrame(root)
    frame.load_website("https://flask-chess-server.herokuapp.com/")
    frame.pack(fill="both", expand=True)
    root.iconphoto(False, tk.PhotoImage(file="resources\images\icon.png"))
    root.mainloop()
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        game.screen.blit(title, title.get_rect(center=(size_x/2, size_y/2)))
        game.coursor()
        
        pygame.display.update()   
    menu.run(game)
"""