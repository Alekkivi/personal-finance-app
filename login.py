import tkinter as tk
import os
import hashlib
from tkinter import messagebox
from db import *
from PIL import ImageTk, Image  

class LoginWindow:
    def __init__(self):
        self.login_window = tk.Tk()
        self.login_window.resizable(False,False)
        self.screen_height_middle = self.login_window.winfo_screenheight() / 3.5
        self.screen_width_middle = self.login_window.winfo_screenwidth() / 2.33
        self.login_window.geometry('%dx%d+%d+%d' % (330, 450, self.screen_width_middle, self.screen_height_middle))
        self.login_window.title('Log in')
        
        # Image
        self.display_image("img/login.png", self.login_window)

        # Username
        self.uname_frame = tk.Frame(self.login_window)
        self.uname_frame.pack(fill=tk.X, padx=10)

        self.uname_label = tk.Label(self.uname_frame, padx=10, text="Username")
        self.uname_label.pack(side=tk.LEFT)

        self.uname_entry = tk.Entry(self.uname_frame, width=35)
        self.uname_entry.pack(side=tk.LEFT)

        # Password
        self.psword_frame = tk.Frame(self.login_window)
        self.psword_frame.pack(fill=tk.X, padx=13, pady=15)

        self.psword_label = tk.Label(self.psword_frame, padx=10, text="Password")
        self.psword_label.pack(side=tk.LEFT)

        self.psword_entry = tk.Entry(self.psword_frame, width=35, show="*")
        self.psword_entry.pack(side=tk.LEFT)

        # 'Log In' Button
        self.login_button = tk.Button(self.login_window, text="Log In", width=8, command=self.test_login)
        self.login_button.pack()

        # 'Create a new account' Button
        self.create_button = tk.Button(self.login_window, text="Create a new account", width=30, command=self.new_account)
        self.create_button.pack(pady=40)

        self.login_window.mainloop()

    def new_account(self):
        print("'Create a new account' -button clicked")
        new_acc_window = tk.Toplevel(self.login_window)
        new_acc_window.resizable(False,False)
        new_acc_window.title("Create an account")
        new_acc_window.geometry('%dx%d+%d+%d' % (330, 450, self.screen_width_middle, self.screen_height_middle))

        # Image
        self.display_image("img/new-user.png", new_acc_window)

        # Username
        new_uname_frame = tk.Frame(new_acc_window)
        new_uname_frame.pack(fill=tk.X, padx=10)

        new_uname_label = tk.Label(new_uname_frame, text="               Username", padx=10)
        new_uname_label.pack(side=tk.LEFT)

        new_uname_entry = tk.Entry(new_uname_frame, width=28)
        new_uname_entry.pack(side=tk.LEFT)

        # Password
        new_psword_frame = tk.Frame(new_acc_window)
        new_psword_frame.pack(fill=tk.X, padx=10, pady=15)

        new_psword_label = tk.Label(new_psword_frame, text="                Password", padx=10)
        new_psword_label.pack(side=tk.LEFT)

        new_psword_entry = tk.Entry(new_psword_frame, width=28, show="*")
        new_psword_entry.pack(side=tk.LEFT)

        # Confirm Password
        new_conf_frame = tk.Frame(new_acc_window)
        new_conf_frame.pack(fill=tk.X, padx=10)

        new_conf_label = tk.Label(new_conf_frame, text="Confirm password", padx=10)
        new_conf_label.pack(side=tk.LEFT)

        new_conf_entry = tk.Entry(new_conf_frame, width=28, show="*")
        new_conf_entry.pack(side=tk.LEFT)


        # Check the input
        def validate_input():
            username = new_uname_entry.get()
            password = new_psword_entry.get()
            confirm_password = new_conf_entry.get()

            # Case: Bad request
            if password != confirm_password or not username or not password or not confirm_password:
                print("Passwords do not match or fields are empty.")
                messagebox.showwarning("Error", "Passwords do not match or fields are empty.")
            else:           
                # Input OK - Check if there is a existing user
                result = check_db_existing_user(username)

                if not result:
                    # There is not a existing user
                    print('There was no matching username in the database')
                    cursor = db.cursor()
                    pword_hash = Sha512Hash(password)
                    sql = "insert into user_credentials( username, password_hash) values (%s,%s);"
                    cursor.execute(sql,(username, pword_hash,))
                    db.commit()
                    print(cursor.rowcount, f"record(s) affected, User: {username} created")
                    messagebox.showinfo("Account created", "Account created - Please log in")
                else:
                    # There was a existing user
                    messagebox.showinfo("Error", "There is a existing account")

        create_button = tk.Button(new_acc_window, text="Create new account", width=20, command=validate_input)
        create_button.pack(pady=40)
    

    def display_image(self, image_path, window):
        print(image_path)
        if os.path.exists(image_path):
            image = Image.open(image_path)
            image = image.resize((200, 200))
            photo = ImageTk.PhotoImage(image)
            image_label = tk.Label(window, image=photo)
            image_label.image = photo  # Retain a reference to the image to prevent it from being garbage collected
            image_label.pack(pady=20)  # Add the label to the window
            return image_label  # Return the label widget
        else:
            print("Image file not found")
            return None


    def test_login(self):
        # Placeholder function for login validation
        print("'Login' -button clicked")
        uname_input = self.uname_entry.get()
        pword_input = self.psword_entry.get()

        if uname_input and pword_input:
            print('Checking login credentials')
            new_pword_hash = Sha512Hash(pword_input)
            cursor = db.cursor()
            sql = "SELECT username FROM user_credentials WHERE username LIKE %s AND password_hash LIKE %s;"
            values = (uname_input, new_pword_hash)
            cursor.execute(sql, values)
            result = cursor.fetchall()
            if result:
                self.username = uname_input
                print('Legit credentials')
            else:
                messagebox.showwarning("Error", "Invalid password")
        else:
            messagebox.showwarning("Error", "Enter credentials")


    


def check_db_existing_user(uname):
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM user_credentials WHERE username LIKE %s;"
    cursor.execute(query, (uname,))
    result = cursor.fetchall()
    return result


def Sha512Hash(password):
    HashedPassword=hashlib.sha512(password.encode('utf-8')).hexdigest()
    return HashedPassword

