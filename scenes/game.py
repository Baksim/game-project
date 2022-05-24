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
            self.screen = pygame.display.set_mode((1300, 950), pygame.RESIZABLE)
        
        self.fonts = { "title": pygame.font.Font("./resources/fonts/title.ttf", 60),
                       "header": pygame.font.Font("./resources/fonts/title.ttf", 50),
                       "btn": pygame.font.Font("./resources/fonts/btn.ttf", 40),
                       "text":pygame.font.Font("./resources/fonts/text.ttf", 30),
                       "small_text":pygame.font.Font("./resources/fonts/text.ttf", 25)
                      }
        
        
        self.colors = {
            "main":             (234, 231, 220),
            "secondary":        (216, 195, 165),
            "tertiary":         (142, 141, 138),
            "accent":           (233, 128, 116),
            "strong_accent":    (232, 90, 79),
            "red":              (139, 0, 0),
            "gray":             (169, 169, 169),
            "green":            (39, 174, 96)
        }
        
        self.music_list = []
        
    def run(self):
        splash_screen.run(self)
        
    def event_handler(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            quit()
            
        elif event.type == VIDEORESIZE and self.settings["fullscreen"] != "True":
            pygame.display.set_mode((max(event.dict['size'][0], 1300), max(event.dict['size'][1], 850)), RESIZABLE)
            pygame.display.update()
        elif event.type == VIDEOEXPOSE and self.settings["fullscreen"] != "True":
            pygame.display.set_mode((max(self.screen.get_size()[0], 1300), max(self.screen.get_size()[1], 850)), RESIZABLE)
            pygame.display.update()
        if event.type == pygame.USEREVENT:
            self.reload_music()
            
    def play_music(self, sound):
        from os import listdir, path
        from os.path import isfile, join
        import random
        if sound["bgm"] == "True":
            music_path = None
            if sound["custom_path"][0] != "False" and sound["custom_path"][1] == "True":
                music_path = sound["custom_path"][0] + "\\"
                if not path.exists(music_path):
                    with open("settings\settings.json", 'w') as f:
                        sound["custom_path"][0] = "False"
                        sound["custom_path"][1] = "False"
                        music_path == None
                        json.dump(self.settings, f, indent=4)
            if sound["custom_path"][1] == "False":
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
        else:
            pygame.mixer.music.stop()
            
    def reload_music(self):
        pygame.mixer.music.queue (self.music_list[0])
        self.music_list.append(self.music_list.pop(0))
        
        
    def apply_settings(self, new_settings, music=None, save=False):
        if new_settings["fullscreen"] != self.settings["fullscreen"] or (self.settings["fullscreen"] == "True" and self.settings["resolution"] != new_settings["resolution"]):
            if new_settings["fullscreen"] == "True": 
                self.screen = pygame.display.set_mode(tuple(map(int, new_settings["resolution"].split(', '))), pygame.FULLSCREEN)
            else:
                self.screen = pygame.display.set_mode((1400, 950), pygame.RESIZABLE)
                
        if new_settings["bgm_volume"] != self.settings["bgm_volume"]:
            pygame.mixer.music.set_volume(float(new_settings["bgm_volume"]))
        if music:
            self.play_music(new_settings)
        self.settings = new_settings.copy()
        if save:
            with open("settings\settings.json", 'w') as f:
                json.dump(self.settings, f, indent=4)
                
    def get_engine(self):
        import chess.engine
        return chess.engine.SimpleEngine.popen_uci("resources\engine\stockfish_15_win_x64_popcnt\stockfish_15_x64_popcnt.exe")

    def load_svg(self, filename, size):
        import cairosvg
        import io
        new_bites = cairosvg.svg2png(url = filename, scale=(size/45))
        byte_io = io.BytesIO(new_bites)
        return pygame.image.load(byte_io)
        
    def coursor(self):
        CURSOR = pygame.image.load('resources\images\cursor.png').convert_alpha()
        if pygame.mouse.get_focused() != 0:
            self.screen.blit(CURSOR, (pygame.mouse.get_pos())) 