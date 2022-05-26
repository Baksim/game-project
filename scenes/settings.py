import pygame
import pygame_widgets as pw
from pygame_widgets.slider import Slider
from pygame_widgets.dropdown import Dropdown
from pygame_widgets.button import Button
import easygui
from pygame.locals import *


def set_value(param, value, sett, game, music=None):
    sett[param] = value
    game.apply_settings(sett, music)
    


def run(game):
    
    def pick_playlist(game, new_settings):
        global custom_music_path, music_name, music_values
        new_path = easygui.diropenbox("Hello!", "Music path")
        if new_path:
            new_settings["custom_path"] = new_path
            set_value("custom_path", [new_path, "True"], new_settings, game, True)
            custom_music_path = [new_settings["custom_path"][0].split("\\")[-1], new_settings["custom_path"][0]]
            music_name = custom_music_path[0]
            music_choices = [
                'Classical',
                'J-Pop',
                'Pop',
                custom_music_path[0]
            ]
            music_values = ['Classical', 'J-Pop', 'Pop', custom_music_path[1]]
            setters[8].hide()
            setters[8].disable()
            setters[8] = Dropdown(
                game.screen, 120, 10, 170, 80, name=music_name,
                choices=music_choices,
                borderRadius=3, colour=game.colors["gray"], 
                values=music_values, 
                direction='down', textHAlign='centre',
                font=game.fonts["small_text"]
            )
        
    running = True
    title = game.fonts["header"].render("Settings", True, (71, 32, 24))
    new_settings = game.settings.copy()
    old_settings = game.settings.copy()
    custom_music_path = [new_settings["custom_path"][0].split("\\")[-1], new_settings["custom_path"][0]] if new_settings["custom_path"][0] != "False" else None
    if custom_music_path:
        if eval(new_settings["custom_path"][1]):
            music_name = custom_music_path[0]
        else:
            music_name = new_settings["music_style"]
        music_choices = [
                'Classical',
                'J-Pop',
                'Pop',
                custom_music_path[0]
            ]
        music_values = ['Classical', 'J-Pop', 'Pop', custom_music_path[1]]
    else:
        music_name = new_settings["music_style"]
        music_choices = [
                'Classical',
                'J-Pop',
                'Pop'
            ]
        music_values = ['Classical', 'J-Pop', 'Pop']
    setters = [
         Dropdown(
        game.screen, 120, 10, 170, 80, name=new_settings["fullscreen"],
        choices=[
            'True',
            'False'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['True', 'False'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
        ),
    Dropdown(
        game.screen, 120, 10, 170, 80, name=new_settings["resolution"],
        choices=[
            "2560x1440",
            '1920x1080',
            '1280x720'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['2560, 1440', '1920, 1080', '1280, 720'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
    ),
    Dropdown(
        game.screen, 120, 10, 170, 80, name=new_settings["piece_style"],
        choices=[
            'Classic',
            'Africa',
            'Fairytale',
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['Classic', 'Africa', 'Fairytale'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
    ),
    Dropdown(
        game.screen, 120, 10, 170, 80, name=new_settings["bgm"],
        choices=[
            'True',
            'False'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['True', 'False'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
        ),
    Dropdown(
        game.screen, 120, 10, 170, 80, name=new_settings["sfx"],
        choices=[
            'True',
            'False'
        ],
        borderRadius=3, colour=game.colors["gray"], 
        values=['True', 'False'], 
        direction='down', textHAlign='centre',
        font=game.fonts["small_text"]
        ),
    Slider(game.screen, 100, 100, 800, 20,
           min=0.01, max=1, step=0.01, 
           initial=float(new_settings["bgm_volume"]), handleRadius=13
           ),
    Slider(game.screen, 100, 100, 800, 20,
           min=0.01, max=1, step=0.01, 
           initial=float(new_settings["sfx_volume"]), handleRadius=13
           ),
    Dropdown(
            game.screen, 120, 10, 170, 80, name=music_name,
            choices=music_choices,
            borderRadius=3, colour=game.colors["gray"], 
            values=music_values, 
            direction='down', textHAlign='centre',
            font=game.fonts["small_text"]
            ),
    Button(
        game.screen, 100, 100, 170,  80, 
        text='Add',
        font= game.fonts["small_text"],
        radius=20,
        onClick=pick_playlist,
        onClickParams=(game, new_settings)
        )
    ]
    
    
    while running:
        game.screen.fill(game.colors["main"])
        size_x, size_y = game.screen.get_size()
        title_rect = pygame.Rect((0, size_y // 60), (size_x, size_y // 10))
        pygame.draw.rect(game.screen, game.colors["tertiary"], title_rect)
        game.screen.blit(title, title.get_rect(center=(title_rect.center)))
        
        save_rect = pygame.Rect((0, 7 * size_y // 60), (size_x // 4, 100))
        cancel_rect = pygame.Rect((0, 7 * size_y // 60 + 100), (size_x // 4, 100))
        pygame.draw.rect(game.screen, game.colors["button_bg"], save_rect)
        pygame.draw.rect(game.screen, game.colors["button_bg"], cancel_rect)
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
         
        setter_names = ["fullscreen", "resolution", "piece_style",
                        "bgm", "sfx", "bgm_volume", "sfx_volume", "music_style",
                        "custom_path"
                        ]
        options = ["Fullscreen", "Resolution", "Piece style",
                   "Music", "Sounds", "Music Volume", "SFX Volume", "Music Style",
                   "Add music"
                   ]
        for i, setter in enumerate(setters):
            text = game.fonts["text"].render(options[i], True, (0, 0, 0))
            if i + 1 <= len(setters) / 2:
                if isinstance(setter, Dropdown):
                    setter.setX(rects[i].midtop[0] - 180)
                    setter.setY(rects[i].centery - 20)
                    
                elif isinstance(setter, Slider):
                    setter.setWidth(rects[i].width // 4 - 30)
                    setter.setX(rects[i].centerx - setter.getWidth() - 10)
                    setter.setY(rects[i].centery + 10)
                elif isinstance(setter, Button):
                    setter.setX(rects[i].midtop[0] - 180)
                    setter.setY(rects[i].centery - 20)
                    
                game.screen.blit(text, (rects[i].midleft[0] + 50, rects[i].midleft[1]))
                
            else:
                if isinstance(setter, Dropdown):
                    setter.setX(rects[i - round(len(setters) / 2)].right - 180)
                    setter.setY(rects[i - round(len(setters) / 2)].centery - 20)
                
                elif isinstance(setter, Slider):
                    setter.setWidth(rects[i - round(len(setters) / 2)].width // 4 - 30)
                    setter.setX(rects[i - round(len(setters) / 2)].right - setter.getWidth() - 20)
                    setter.setY(rects[i - round(len(setters) / 2)].centery + 10)
                elif isinstance(setter, Button):
                    setter.setX(rects[i - round(len(setters) / 2)].right - 180)
                    setter.setY(rects[i - round(len(setters) / 2)].centery - 20)
                    
                game.screen.blit(text, (rects[i - round(len(setters) / 2)].centerx + 50, rects[i - round(len(setters) / 2)].midleft[1]))
            
            if isinstance(setter, Dropdown):    
                if setter_names[i] == "music_style" and setter.getSelected():
                    if eval(new_settings["custom_path"][1]) and setter.getSelected() != custom_music_path[1]:
                        new_settings["custom_path"][1] = "False"
                        set_value(setter_names[i], setter.getSelected(), new_settings, game, True)
                    elif not eval(new_settings["custom_path"][1]):
                        if setter.getSelected() == custom_music_path[1]:
                            new_settings["custom_path"][1] = "True"
                            set_value(setter_names[i], setter.getSelected(), new_settings, game, True)
                        elif setter.getSelected() != new_settings["music_style"]:
                            set_value(setter_names[i], setter.getSelected(), new_settings, game, True)
                elif setter_names[i] == "bgm":
                    if setter.getSelected():
                        if setter.getSelected() != new_settings[setter_names[i]]:
                            set_value(setter_names[i], setter.getSelected(), new_settings, game, True)
                elif setter.getSelected() and setter.getSelected() != new_settings[setter_names[i]]:
                    set_value(setter_names[i], setter.getSelected(), new_settings, game)
            elif isinstance(setter, Slider) and setter.getValue() != new_settings[setter_names[i]]:
                set_value(setter_names[i], setter.getValue(), new_settings, game)
            
        
        if save_rect.collidepoint(pygame.mouse.get_pos()):
            text_save = game.fonts["btn"].render("Save", True, game.colors["red"])
        else:
            text_save = game.fonts["btn"].render("Save", True, game.colors["button_text"])
        game.screen.blit(text_save, text_save.get_rect(center=(save_rect.center)))
        if cancel_rect.collidepoint(pygame.mouse.get_pos()):
            text_cancel = game.fonts["btn"].render("Cancel", True, game.colors["red"])
        else:
            text_cancel = game.fonts["btn"].render("Cancel", True, game.colors["button_text"])
        game.screen.blit(text_cancel, text_cancel.get_rect(center=(cancel_rect.center)))
        
        for event in events:
            game.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    for i in setters:
                        i.disable()
                        i.hide()
                    game.apply_settings(old_settings, True)
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if cancel_rect.collidepoint(pygame.mouse.get_pos()):
                    for i in setters:
                            i.disable()
                            i.hide()
                    game.apply_settings(old_settings, True)
                    running = False
                if save_rect.collidepoint(pygame.mouse.get_pos()):
                    for i in setters:
                            i.disable()
                            i.hide()
                    game.settings = new_settings
                    game.apply_settings(new_settings, False, True)
                    running = False
        
        pw.update(events)
        
        game.coursor()
        pygame.display.update() 
            