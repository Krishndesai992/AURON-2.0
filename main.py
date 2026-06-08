from gui.login_window import LoginWindow
from gui.main_window import AURONApp


if __name__ == "__main__":

    login_window = LoginWindow()

    login_window.mainloop()

    if login_window.authenticated:

        app = AURONApp()

        app.mainloop()