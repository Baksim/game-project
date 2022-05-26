import os
from authapp import *
import ctypes
import json
from threading import *


def main():
    myappid = '300icq'
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    if not os.path.isfile("settings\\session.json"):
        with open('settings\\session.json', "w") as f:
            session = {"session_id": ""}
            json.dump(session, f)
        f.close()
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
        f.close()
    
if __name__ == "__main__":
    t = Thread(target=main)
    t.start()
