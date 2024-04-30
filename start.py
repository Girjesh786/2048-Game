# start.py
from customtkinter import *
from PIL import Image
import subprocess

def start_color(start_window):
    # Destroy the current window
    start_window.destroy()

    # Use subprocess to start color.py
    subprocess.run(["python", "game.py"])

def back_to_login(start_window):
    # Destroy the current window
    start_window.destroy()

    # Use subprocess to start login.py
    subprocess.run(["python", "login.py"])

def start_main():
    start_window = CTk()
    start_window.title("Start Page")
    start_window.config(bg="white")
    start_window.resizable(False, False)

    bg_img = CTkImage(dark_image=Image.open("bg1.jpg"), size=(500, 500))

    bg_lab = CTkLabel(start_window, image=bg_img, text="")
    bg_lab.grid(row=0, column=0)

    frame1 = CTkFrame(start_window, fg_color="#D9D9D9", bg_color="white", height=350, width=300, corner_radius=20)
    frame1.grid(row=0, column=1, padx=40)

    title = CTkLabel(frame1, text="Start Page", text_color="black", font=("", 35, "bold"))
    title.grid(row=0, column=0, sticky="nw", pady=30, padx=10)

    start_btn = CTkButton(frame1, text="Start", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                          corner_radius=15, command=lambda: start_color(start_window))
    start_btn.grid(row=1, column=0, sticky="w", pady=20, padx=40)

    back_to_login_btn = CTkButton(frame1, text="Back To Login", font=("", 15, "bold"), height=40, width=60, fg_color="#0085FF", cursor="hand2",
                                  corner_radius=15, command=lambda: back_to_login(start_window))
    back_to_login_btn.grid(row=2, column=0, sticky="w", pady=10, padx=40)

    start_window.mainloop()

if __name__ == "__main__":
    start_main()
