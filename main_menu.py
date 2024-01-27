from login import *
from datetime import date

class MainMenu:
    def __init__(self):
        self.login_window = LoginWindow()
        self.username = self.login_window.username
        self.current_date = date.today().strftime("%d/%m/%Y")