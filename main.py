from scenes import game
import ctypes
import json
import tkinter
import tkinter.font as tkFont
import customtkinter


def main():
    myappid = '300icq'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    
    with open('settings\settings.json') as json_file:
        settings = json.load(json_file)
    g = game.Game(settings)
    g.run()  
    
if __name__ == "__main__":
    main()