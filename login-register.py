"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 03.09.24
Latest update: 08.10.24
Version : 0.3

Description:    this file contains the code for
                register or get a player score in the DB.
"""

import tkinter as tk

def save_game_score():
    def get_username():
        username_window = tk.Toplevel(root)
        username_label = tk.Label(username_window, text="Enter your username:")
        username_entry = tk.Entry(username_window)
        username_button = tk.Button(username_window, text="Confirm", command=lambda: print(f"Nice to see you, {username_entry.get()} !"))

        username_label.pack()
        username_entry.pack()
        username_button.pack()

    root = tk.Tk()
    root.title("Login or Register")

    question_label = tk.Label(root, text="Have you already played before?")
    yes_button = tk.Button(root, text="Yes", command=get_username)
    no_button = tk.Button(root, text="No", command=get_username)

    question_label.pack()
    yes_button.pack()
    no_button.pack()

    root.mainloop()

if __name__ == "__main__":
    save_game_score()