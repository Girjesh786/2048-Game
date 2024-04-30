# register.py

from customtkinter import *
from PIL import Image
import mysql.connector
from tkinter import simpledialog, messagebox

# Establish MySQL connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123456",
)

cursor = db.cursor()

# Create color database if not present
# Create color database if not present
try:
    cursor.execute("CREATE DATABASE IF NOT EXISTS color")
    cursor.execute("USE color")
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(255), password VARCHAR(255), high_score INT DEFAULT 0)")
    db.commit()
except mysql.connector.Error as err:
    print(f"Error: {err}")


def create_account(username, password):
    # Check if the entered username and password meet specific criteria
    if not username.isalnum():
        messagebox.showerror("Invalid Username", "Username must contain only alphabets and numbers.")
        return

    if not password.isdigit():
        messagebox.showerror("Invalid Password", "Password must contain only numbers.")
        return

    # Insert user data into the color database
    try:
        cursor.execute("INSERT INTO users (username, password, high_score) VALUES (%s, %s, %s)", (username, password, 0))
        db.commit()
        messagebox.showinfo("Success", "Account created successfully!")
        switch_to_login()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        messagebox.showerror("Error", "Account creation failed.")


def switch_to_login():
    register_window.destroy()
    import login
    login.login_main()

def register_main():
    global register_window

    register_window = CTk()
    register_window.title("Register Page")
    register_window.config(bg="white")
    register_window.resizable(False, False)

    bg_img = CTkImage(dark_image=Image.open("bg1.jpg"), size=(500, 500))

    bg_lab = CTkLabel(register_window, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    frame1 = CTkFrame(register_window, fg_color="#D9D9D9", bg_color="white", height=350, width=300, corner_radius=20)
    frame1.grid(row=0, column=1, padx=40)

    title = CTkLabel(frame1, text="Create Account", text_color="black", font=("", 35, "bold"))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    usrname_entry = CTkEntry(frame1, text_color="white", placeholder_text="Username", fg_color="black",
                             placeholder_text_color="white",
                             font=("", 16, "bold"), width=200, corner_radius=15, height=45)
    usrname_entry.grid(row=1, column=0, sticky="nwe", padx=30)

    passwd_entry = CTkEntry(frame1, text_color="white", placeholder_text="Password", fg_color="black",
                             placeholder_text_color="white",
                             font=("", 16, "bold"), width=200, corner_radius=15, height=45, show="*")
    passwd_entry.grid(row=2, column=0, sticky="nwe", padx=30, pady=20)

    cr_acc = CTkButton(frame1, text="Create Account!!", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                      corner_radius=15, command=lambda: create_account(usrname_entry.get(), passwd_entry.get()))
    cr_acc.grid(row=3, column=0, sticky="w", pady=20, padx=40)
    
    back_to_login = CTkButton(frame1, text="Back to Login!!", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                      corner_radius=15, command=switch_to_login)
    back_to_login.grid(row=4, column=0, sticky="w", pady=10, padx=40)

    register_window.mainloop()

if __name__ == "__main__":
    register_main()
