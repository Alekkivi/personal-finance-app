from login import *
import tkinter as tk
from datetime import date

class MainMenuWindow:
    def __init__(self, username):

        # Initialize window
        self.root = tk.Tk()
        self.root.resizable(False,False)
        self.screen_height_middle = self.root.winfo_screenheight() / 3.5
        self.screen_width_middle = self.root.winfo_screenwidth() / 2.33
        self.root.geometry('%dx%d+%d+%d' % (900, 450, self.screen_width_middle, self.screen_height_middle))

        # Start to form user data
        self.username = username
        self.current_date = date.today().strftime("%d/%m/%Y")
        self.expenses = [] 
        self.incomes = []
        self.current_balance = 0

        # Welcome text
        self.welcome_frame = tk.Frame(self.root)

        date_text = "Todays date: " + self.current_date
        welcome_text = "Welcome " + self.username

        tk.Label(self.welcome_frame, text=welcome_text)
        tk.Label(self.welcome_frame, text=date_text)
        self.welcome_frame.pack()


        # TODO If first time in the month --> force to update wage
        # Kela automaattisesti, laina kans, SQL


         

        def show_home_page():
            home_frame = tk.Frame(main_frame)
            lb = tk.Label(home_frame, text="Home Frame\n\n page1", font=('bold',30))
            lb.pack()
            home_frame.pack(pady=20)

        
        def show_transaction_page():
            home_frame = tk.Frame(main_frame)
            lb = tk.Label(home_frame, text="transaction Frame\n\n page1", font=('bold',30))
            lb.pack()
            home_frame.pack(pady=20)

        
        
        def show_yearly_page():
            home_frame = tk.Frame(main_frame)
            lb = tk.Label(home_frame, text="yearly Frame\n\n page1", font=('bold',30))
            lb.pack()
            home_frame.pack(pady=20)

        def clear_main_frame():
            for frame in main_frame.winfo_children():
                frame.destroy()

        def clear_menu_indicators():
            home_indicator.config(bg='#c3c3c3')
            yearly_indicator.config(bg='#c3c3c3')
            transaction_indicator.config(bg='#c3c3c3')

        def indicate_menu_status(label, page):

            # Clear the main_frame
            clear_menu_indicators()
            clear_main_frame()

            # Pack the new page to main_frame
            label.config(bg="#158aff")
            page()

        options_frame = create_frame(self.root,'#c3c3c3', 125, 450)
        main_frame = create_frame(self.root, "#158aff", 900, 450)

        # Home button and indicator
        home_btn = tk.Button(options_frame, text='Home', font=('Bold', 15), fg='#c3c3c3', bd=0, 
                             command=lambda: indicate_menu_status(home_indicator, show_home_page))
        
        home_btn.place(x=10, y=50)
        home_indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
        home_indicator.place(x=3, y=50, width=5, height=40)

        # transactions button and indicator
        transaction_btn = tk.Button(options_frame, text='Transaction', font=('Bold', 15), fg='#c3c3c3', bd=0, 
                                    command=lambda: indicate_menu_status(transaction_indicator, show_transaction_page))
        
        transaction_btn.place(x=10, y=100)
        transaction_indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
        transaction_indicator.place(x=3, y=100, width=5, height=40)

         # yearly button and indicator
        yearly_btn = tk.Button(options_frame, text='Yearly', font=('Bold', 15), fg='#c3c3c3', bd=0, 
                               command=lambda: indicate_menu_status(yearly_indicator, show_yearly_page))
        
        yearly_btn.place(x=10, y=150)
        yearly_indicator = tk.Label(options_frame, text="", bg='#c3c3c3')
        yearly_indicator.place(x=3, y=150, width=5, height=40)


 
        self.root.mainloop()




def create_frame(window, bg, width, height):
    frame = tk.Frame(window, bg=bg)
    frame.pack(side=tk.LEFT)
    frame.pack_propagate(False)
    frame.configure(width=width, height=height)
    return frame
