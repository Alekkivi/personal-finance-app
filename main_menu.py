from login import *
import tkinter as tk
from datetime import date

class MainMenuWindow:
    def __init__(self, username):

        # Initialize window
        self.menu = tk.Tk()
        self.menu.resizable(False,False)
        self.screen_height_middle = self.menu.winfo_screenheight() / 3.5
        self.screen_width_middle = self.menu.winfo_screenwidth() / 2.33
        self.menu.geometry('%dx%d+%d+%d' % (500, 450, self.screen_width_middle, self.screen_height_middle))

        # Start to form user data
        self.username = username
        self.current_date = date.today().strftime("%d/%m/%Y")
        self.expenses = [] 
        self.incomes = []
        self.current_balance = 0

        # Welcome text
        self.welcome_frame = tk.Frame(self.menu)
        self.welcome_frame.pack()

        date_text = "Todays date: " + self.current_date
        welcome_text = "Welcome " + self.username

        self.welcome_label = tk.Label(self.welcome_frame, text=welcome_text)
        self.welcome_label.pack()


        # TODO If first time in the month --> force to update wage
        # Kela automaattisesti, laina kans, SQL



 


        self.menu.mainloop()

