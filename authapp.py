from tkinter import *
import customtkinter as ctk
from email_validator import validate_email, EmailNotValidError
import requests
import json
from scenes import game

def go_to_game(controller, session):
    with open('settings\\settings.json') as json_file:
        settings = json.load(json_file)
    g = game.Game(settings, session)
    controller.destroy()
    g.run()

class AuthApp(ctk.CTk):
    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        self.title("User Manager")
        ctk.set_default_color_theme("settings\\launcher_style.json")
        self.iconbitmap("resources\\images\\ctkicon.ico")
        ctk.set_appearance_mode("light")
        w = 400
        h = 350
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.resizable(False, False)
        self.update()

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (StartPage, LoginPage, RegisterPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky='nsew', padx=80, pady=50)

        self.show_frame("StartPage")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class StartPage(ctk.CTkFrame):

    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        ctk.CTkLabel(self, text="User Manager").grid(row=0, column=0, sticky='ew', pady=7)
        logbtn = ctk.CTkButton(self, text="Log in", command=lambda: controller.show_frame("LoginPage"))
        regbtn = ctk.CTkButton(self, text="Register", command=lambda: controller.show_frame("RegisterPage"))
        gstbtn = ctk.CTkButton(self, text="Continue as guest", command=lambda: go_to_game(controller, "Guest"))
        logbtn.grid(row=1, column=0, pady=3)
        regbtn.grid(row=2, column=0, pady=3)
        gstbtn.grid(row=3, column=0, pady=3)
        self.columnconfigure(0, weight=1)


class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        ctk.CTkLabel(self, text="Login").grid(row=0, column=0, columnspan=2, sticky='ew')
        self.warning = ctk.CTkLabel(self, text="")
        self.warning.grid(row=1, column=0, columnspan=2, sticky='ew')
        ctk.CTkLabel(self, text="Email: ").grid(row=2, column=0)
        self.email = ctk.CTkEntry(self, placeholder_text="Email")
        self.email.grid(row=2, column=1)
        ctk.CTkLabel(self, text="Password: ").grid(row=3, column=0)
        self.pswd = ctk.CTkEntry(self, placeholder_text="Password")
        self.pswd.grid(row=3, column=1, sticky='e')
        submit = ctk.CTkButton(self, text="Submit", command=lambda: self.login(controller), width=50)
        submit.grid(row=4, column=0, columnspan=2, pady=10, sticky='ew')
        remember_me = StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(self, text="Remember me", variable=remember_me, onvalue="on", offvalue="off")
        self.checkbox.grid(row=5, column=0, sticky='n')
        goback = ctk.CTkButton(self, text="Go back", command=lambda: controller.show_frame("StartPage"), width=10)
        goback.grid(row=5, column=1, sticky='e')

    def login(self, controller):
        data = {'email': self.email.get(),
                'password': self.pswd.get()}
        if data.get('email') != '' and data.get('password') != '':
            try:
                data['email'] = validate_email(data['email']).email
                response = requests.get('https://flask-chess-server.herokuapp.com/login_api', data=data).json()
                session = response['session_id']
                if self.checkbox.get() == "on":
                    with open('settings\\session.json', 'w') as outfile:
                        json.dump(response, outfile, indent=4)
                go_to_game(controller, session)
            except EmailNotValidError as e:
                self.warning.config(text="Invalid email address.")
        else:
            self.warning.config(text="Please fill out the fields.")


class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)
        self.controller = controller
        ctk.CTkLabel(self, text="Register").grid(row=0, column=0, columnspan=2, sticky='ew')
        self.warning = ctk.CTkLabel(self, text="")
        self.warning.grid(row=1, column=0, columnspan=2, sticky='ew')
        ctk.CTkLabel(self, text="Username: ").grid(row=2, column=0)
        self.usrn = ctk.CTkEntry(self, placeholder_text="Username")
        self.usrn.grid(row=2, column=1)
        ctk.CTkLabel(self, text="Email: ").grid(row=3, column=0)
        self.email = ctk.CTkEntry(self, placeholder_text="Email")
        self.email.grid(row=3, column=1)
        ctk.CTkLabel(self, text="Password: ").grid(row=4, column=0)
        self.pswd = ctk.CTkEntry(self, placeholder_text="Password")
        self.pswd.grid(row=4, column=1, sticky='e')
        ctk.CTkLabel(self, text="Confirm password: ").grid(row=5, column=0)
        self.cnpswd = ctk.CTkEntry(self, placeholder_text="Confirm password")
        self.cnpswd.grid(row=5, column=1, sticky='e')
        self.submit = ctk.CTkButton(self, text="Submit", command=lambda: self.register())
        self.submit.grid(row=6, column=0, columnspan=2, sticky='ew', padx=50, pady=7)
        goback = ctk.CTkButton(self, text="Go back", command=lambda: controller.show_frame("StartPage"), width=10)
        goback.grid(row=7, column=1, sticky='en')

    def register(self):
        data = {'username': self.usrn.get(),
                'email': self.email.get(),
                'password': self.pswd.get(),
                'confirm_password': self.cnpswd.get()}
        if data.get('username') != '' and data.get('email') != '' and data.get('password') != '' and data.get('confirm_password') != '':
            if data.get('confirm_password') == data.get('password'):
                try:
                    data['email'] = validate_email(data['email']).email
                    requests.post('https://flask-chess-server.herokuapp.com/register_api', data=data)
                    self.warning.config(text="Success! Please log in now.")
                    self.submit.config(state="disabled")
                except EmailNotValidError as e:
                    self.warning.config(text="Invalid email address.")
            else:
                self.warning.config(text="Passwords don't match.")
        else:
            self.warning.config(text="Please fill out the fields.")

# if __name__ == "__main__":
#     app = AuthApp()
#     app.mainloop()
