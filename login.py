import tkinter as tk
import os
import hashlib
from tkinter import messagebox
from db import *
from PIL import ImageTk, Image  

class LoginWindow:
    def __init__(self):
        # 'Login' Window
        self.login_window = create_window(False, None, 450, 330, "PFA", 4, 1.5)
        add_image_to_window("img/login.png", self.login_window)
        
        # Prompts for user
        self.uname_entry = text_and_entry_frame('uname', self.login_window, 12, 0, "Username", "", 35)
        self.psword_entry = text_and_entry_frame('psword',self.login_window, 13, 15, "password", "*", 35)

        # Buttons
        self.login_button = tk.Button(self.login_window, text="Log In", width=8, command=self.test_login).pack()
        self.create_button = tk.Button(self.login_window, text="Create a new account", width=30, command=self.new_account).pack(pady=40)

        # Window Loop
        self.login_window.mainloop()


    # Event Handeler - Log in to a existing account
    def test_login(self):
        try:
            input_ok = entry_validation(self.uname_entry.get(), self.psword_entry.get(), False, None)

            if input_ok:
                # Check if there is a existing user in the db that matches the entries
                new_pword_hash = Sha512Hash(self.psword_entry.get())
                cursor = db.cursor()
                sql = "SELECT username FROM user_credentials WHERE username LIKE %s AND password_hash LIKE %s;"
                values = (self.uname_entry.get(), new_pword_hash)
                cursor.execute(sql, values)
                result = cursor.fetchall()
                
                if result:
                    # Credentials were correct
                    self.username = self.uname_entry.get()
                    print('Log In successful')
                    self.login_window.destroy()
                else:
                    # Credentials were incorrect
                    messagebox.showwarning("Error", "Invalid password or username")

        except Exception as e:
            print("Error:", e)
            messagebox.showerror("Error", "An unexpected error occurred. Please try again.")


    # Event Handeler - Pop up a new window from new account button
    def new_account(self):

        # 'New account' window
        new_acc_window = create_window(True, self.login_window, 450, 330, "PFA", 4, 1.5)
        add_image_to_window("img/new-user.png", new_acc_window)
        
        # Prompts for user
        new_uname_entry = text_and_entry_frame('uname', new_acc_window, 10, 0, "               Username", "", 28)
        new_psword_entry = text_and_entry_frame('pword', new_acc_window, 10, 15,"                Password","*",28)
        new_conf_entry = text_and_entry_frame('conf', new_acc_window, 10, 0,"Confirm password", "*", 28  )

        # Try to create a new account
        def handle_new_user_creation():
            input_ok = entry_validation(new_uname_entry.get(), new_psword_entry.get(), True, new_conf_entry.get())
            if input_ok:
                # Check if there is an existing user
                result = check_db_existing_user(new_uname_entry.get())

                if not result:
                    # Case: No matching user --> Create new user
                    try:
                        cursor = db.cursor()
                        pword_hash = Sha512Hash(new_psword_entry.get())
                        sql = "INSERT INTO user_credentials (username, password_hash) VALUES (%s, %s);"
                        cursor.execute(sql, (new_uname_entry.get(), pword_hash,))
                        db.commit()
                        print(cursor.rowcount, f"record(s) affected, User: {new_uname_entry.get()} created")
                        messagebox.showinfo("PFA", "Account created - Please log in")

                    # There was a error in db connection   
                    except Exception as e:
                        print("MySQL Error:", e)
                        print("Failed to create user.")
                        messagebox.showerror("Error", "Failed to create user. Please try again.")
                else:
                    # Case: Username taken
                    messagebox.showinfo("PFA", "There is an existing account")

        btn = tk.Button(new_acc_window, text="Create new account", width=20, command=handle_new_user_creation)
        btn.pack(pady=40)


# Make sure that entry boxes are not empty and if needed, password and confirm password match
def entry_validation(uname, pword, need_for_conf, conf):
    if need_for_conf:
        # invalid input and need for password confirmation
        if pword != conf or not uname or not pword or not conf:
            return False
        else:
            # Input OK
            return True
    # No need for password confirmation
    else:
        if uname and pword:
            return True
        else:
            messagebox.showinfo("PFA", "Invalid input")
            return False


# Is the uname unique when compaired to db
def check_db_existing_user(uname):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM user_credentials WHERE username LIKE %s;"
    cursor.execute(query, (uname,))
    result = cursor.fetchall()
    return result


# Turn a string to a hashed string
def Sha512Hash(password):
    HashedPassword=hashlib.sha512(password.encode('utf-8')).hexdigest()
    return HashedPassword


# Create a text - input frame
def text_and_entry_frame(frame_name, window, xpad, ypad, label_text, show_symbol, entry_width):
    frame_name = tk.Frame(window)
    frame_name.pack(fill=tk.X, padx=xpad, pady=ypad)
    label = tk.Label(frame_name, text=label_text, padx=xpad)
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame_name, width=entry_width, show=show_symbol)
    entry.pack(side=tk.LEFT)
    return entry


# Create a whole new window
def create_window(new_top_window, root_window, window_height, window_width, title, height_pos, width_pos):
    # Is the window to be created supposed to be a pop up
    if not new_top_window:
        window = tk.Tk()
    else:
        window = tk.Toplevel(root_window)

    screen_height_middle = window.winfo_screenheight() / height_pos
    screen_width_middle = window.winfo_screenheight() / width_pos
    window.geometry('%dx%d+%d+%d' % (window_width, window_height, screen_width_middle, screen_height_middle))
    window.title(title)
    return window


# Add a square image to the window
def add_image_to_window(image_path, window):
    if os.path.exists(image_path):
        image = Image.open(image_path)
        image = image.resize((200, 200))
        photo = ImageTk.PhotoImage(image)
        image_label = tk.Label(window, image=photo)
        image_label.image = photo  # prevent garbage collection
        image_label.pack(pady=20)
    else:
        print("Image file not found")