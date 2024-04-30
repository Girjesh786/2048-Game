# login.py

from customtkinter import *
from PIL import Image
import mysql.connector
from tkinter import simpledialog, messagebox
import subprocess

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="color"
)

cursor = db.cursor()

def login(username, password, login_window):
    if not username.isalnum():
        messagebox.showerror("Invalid Username", "Username must contain only alphabets and numbers.")
        return

    if not password.isdigit():
        messagebox.showerror("Invalid Password", "Password must contain only numbers.")
        return

    try:
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        result = cursor.fetchone()
        if result:
            print("Login successful!")
            login_window.destroy()
            subprocess.run(["python", "start.py"])  # Adjust the command based on your environment
        else:
            messagebox.showerror("Login Error", "Invalid username or password. Please try again.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def register_redirect(login_window):
    login_window.destroy()
    import register
    register.register_main()

def login_main():
    login_window = CTk()
    login_window.title("Login Page")
    login_window.config(bg="white")
    login_window.resizable(False, False)

    bg_img = CTkImage(dark_image=Image.open("bg1.jpg"), size=(500, 500))

    bg_lab = CTkLabel(login_window, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    frame1 = CTkFrame(login_window, fg_color="#D9D9D9", bg_color="white", height=350, width=300, corner_radius=20)
    frame1.grid(row=0, column=1, padx=40)

    title = CTkLabel(frame1, text="Login to Your Account", text_color="black", font=("", 35, "bold"))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    usrname_entry = CTkEntry(frame1, text_color="white", placeholder_text="Username", fg_color="black",
                             placeholder_text_color="white",
                             font=("", 16, "bold"), width=200, corner_radius=15, height=45)
    usrname_entry.grid(row=1, column=0, sticky="nwe", padx=30)

    passwd_entry = CTkEntry(frame1, text_color="white", placeholder_text="Password", fg_color="black",
                             placeholder_text_color="white",
                             font=("", 16, "bold"), width=200, corner_radius=15, height=45, show="*")
    passwd_entry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

    l_btn = CTkButton(frame1, text="Login", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                      corner_radius=15, command=lambda: login(usrname_entry.get(), passwd_entry.get(), login_window))
    l_btn.grid(row=3, column=0, sticky="ne", pady=20, padx=35)

    r_btn = CTkButton(frame1, text="Back To Register", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                      corner_radius=15, command=lambda: register_redirect(login_window))
    r_btn.grid(row=4, column=0, sticky="ne", pady=10, padx=35)

    login_window.mainloop()

if __name__ == "__main__":
    login_main()
