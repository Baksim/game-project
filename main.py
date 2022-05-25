from authapp import *
import ctypes
import json
import tkinter
import tkinter.font as tkFont
import customtkinter


def main():
    myappid = '300icq'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    with open('settings\\session.json') as f:
        session = json.load(f)['session_id']
        if session == "":
            authapp = AuthApp()
            authapp.mainloop()
        else:
            with open('settings\settings.json') as json_file:
                settings = json.load(json_file)
            g = game.Game(settings, session)
            g.run()
    
if __name__ == "__main__":
    main()
