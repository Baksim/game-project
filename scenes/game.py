import pygame
from pygame.locals import *
import sys
from . import splash_screen
import json

class Game:
    def __init__(self, settings):
        pygame.init()
        pygame.display.set_caption('Chess Multiplayer')
        pygame_icon = pygame.image.load('resources\images\icon.png')
        pygame.display.set_icon(pygame_icon)
        pygame.mouse.set_visible(False)
        
        self.settings = settings
        if settings["fullscreen"] == "True":
            self.screen = pygame.display.set_mode(tuple(map(int, settings["resolution"].split(', '))), pygame.FULLSCREEN)
        else:
            self.screen = pygame.display.set_mode((1000, 850), pygame.RESIZABLE)
        
        self.fonts = { "title": pygame.font.Font("./resources/fonts/title.ttf", 60),
                       "header": pygame.font.Font("./resources/fonts/title.ttf", 50),
                       "btn": pygame.font.Font("./resources/fonts/btn.ttf", 40),
                       "text":pygame.font.Font("./resources/fonts/text.ttf", 40),
                       "small_text":pygame.font.Font("./resources/fonts/text.ttf", 25)
                      }
        
        
        self.colors = {
            "main":             (234, 231, 220),
            "secondary":        (216, 195, 165),
            "tertiary":         (142, 141, 138),
            "accent":           (233, 128, 116),
            "strong_accent":    (232, 90, 79),
            "red":              (139, 0, 0),
            "gray":             (169, 169, 169)
        }
        
        self.music_list = []
        
    def run(self):
        if self.settings["sound"]["bgm"] == "True":
            self.play_music(self.settings["sound"])
        splash_screen.run(self)
        
    def event_handler(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == VIDEORESIZE:
            pygame.display.set_mode((max(event.dict['size'][0], 800), max(event.dict['size'][1], 700)), RESIZABLE)
            pygame.display.update()
        elif event.type == VIDEOEXPOSE:
            pygame.display.set_mode((max(self.screen.get_size()[0], 800), max(self.screen.get_size()[1], 700)), RESIZABLE)
            pygame.display.update()
        if event.type == pygame.USEREVENT:
            self.reload_music()
            
    def play_music(self, sound):
        from os import listdir, path
        from os.path import isfile, join
        import random
        if sound["bgm"] == "True":
            music_path = None
            if sound["custom_path"] != "False":
                music_path = sound["custom_path"] + "\\"
                if not path.exists(music_path):
                    with open("settings\settings.json", 'w') as f:
                        sound["custom_path"] = "False"
                        wrong = None
                        for i in sound["user_music"]:
                            if sound["user_music"][i] + "\\" == music_path:
                                wrong = i
                                break
                        del sound["user_music"][wrong]
                        music_path == None
                        json.dump(self.settings, f, indent=4)
            if sound["custom_path"] == "False":
                music_path = "resources\sound\music\\" + sound["music_style"] + "\\"
            
            if music_path and path.exists(music_path):
                self.music_list = []
                for f in listdir(music_path):
                    if isfile(join(music_path, f)):
                        if f.lower().endswith(('.mp3', '.wav', '.ogg')):
                            self.music_list.append(music_path + f)
                
                if self.music_list:
                    random.shuffle(self.music_list)
                    pygame.mixer.music.load(self.music_list[0])
                    self.music_list.append(self.music_list.pop(0))
                    pygame.mixer.music.queue (self.music_list[0])
                    self.music_list.append(self.music_list.pop(0))
                    pygame.mixer.music.set_endevent (pygame.USEREVENT)
                    pygame.mixer.music.set_volume(float(sound["bgm_volume"]))
                    pygame.mixer.music.play()
            
    def reload_music(self):
        pygame.mixer.music.queue (self.music_list[0])
        self.music_list.append(self.music_list.pop(0))
        
        
    def apply_settings(self, new_settings):
        pass
    
    def rest_settings(self):
        pass
        
    def coursor(self):
        CURSOR = pygame.image.load('resources\images\cursor.png').convert_alpha()
        if pygame.mouse.get_focused() != 0:
            self.screen.blit( CURSOR, ( pygame.mouse.get_pos() ) ) 