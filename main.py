# main.py

from customtkinter import *
from PIL import Image
import mysql.connector
from tkinter import simpledialog

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
    database="color"
)

cursor = db.cursor()

def create_account():
    username = simpledialog.askstring("Create Account", "Enter your username:")
    password = simpledialog.askstring("Create Account", "Enter your password:")
    high_score = 0  # Set initial high score to 0 for new accounts

    # Insert user data into the database
    try:
        cursor.execute("INSERT INTO users (username, password, high_score) VALUES (%s, %s, %s)", (username, password, high_score))
        db.commit()
        print("Account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def login():
    # Add your login functionality here
    pass

def switch_to_register():
    main_window.destroy()
    import register
    register.register_main()  # Call the register_main function from register.py

def switch_to_login():
    main_window.destroy()
    import login
    login.login_main()  # Call the login_main function from login.py

def main():
    global main_window

    main_window = CTk()
    main_window.title("Main Page")
    main_window.config(bg="white")
    main_window.resizable(False, False)

    bg_img = CTkImage(dark_image=Image.open("bg1.jpg"), size=(500, 500))

    bg_lab = CTkLabel(main_window, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    frame1 = CTkFrame(main_window, fg_color="#D9D9D9", bg_color="white", height=350, width=300, corner_radius=20)
    frame1.grid(row=0, column=1, padx=40)

    title = CTkLabel(frame1, text="2048 Game", text_color="black", font=("", 35, "bold"))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    register_btn = CTkButton(frame1, text="Create Account", font=("", 15, "bold"), height=40, width=120,
                             fg_color="#0085FF", cursor="hand2", corner_radius=15, command=switch_to_register)
    register_btn.grid(row=1, column=0, pady=20, padx=20)

    login_btn = CTkButton(frame1, text="Login", font=("", 15, "bold"), height=40, width=120, fg_color="#0085FF",
                          cursor="hand2", corner_radius=15, command=switch_to_login)
    login_btn.grid(row=2, column=0, pady=20, padx=20)

    main_window.mainloop()

if __name__ == "__main__":
    main()
