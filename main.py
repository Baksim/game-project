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
    
    
    """
    root = customtkinter.CTk()
    w = 800
    h = 650
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.iconphoto(False, tkinter.PhotoImage(file="resources\images\icon.png"))
    customtkinter.set_appearance_mode("light")
    customtkinter.set_default_color_theme("settings\launcher_style.json")
    button = customtkinter.CTkButton(master=root, text="CTkButton")
    button.place(relx=0.5, rely=0.5, anchor=tkinter.CENTER)
    root['background'] = "#EAE7DC"
    root.mainloop()
    """
    
    g = game.Game(settings)
    g.run()  
    
if __name__ == "__main__":
    main()