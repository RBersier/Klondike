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

import Database
import ScoresWin


def save_game_score():
    return

def get_username():
    username_window = tk.Toplevel(root)
    height = 100
    width = 200
    username_window.geometry(f"{width}x{height}")
    conn = Database.db_connection("127.0.0.1", "root", "Pa$$w0rd", "Solitaire")
    username_label = tk.Label(username_window, text="Enter your username:")
    username_entry = tk.Entry(username_window)
    username_button = tk.Button(username_window, text="Confirm", command=lambda: confirm_player(conn, username_entry.get(), username_window))

    username_label.pack()
    username_entry.pack()
    username_button.pack()

def new_username():
    new_username_window = tk.Toplevel(root)
    height = 100
    width = 200
    new_username_window.geometry(f"{width}x{height}")
    conn = Database.db_connection("127.0.0.1", "root", "Pa$$w0rd", "Solitaire")
    username_label = tk.Label(new_username_window, text="Enter your username:")
    username_entry = tk.Entry(new_username_window)
    username_button = tk.Button(new_username_window, text="Confirm", command=lambda: enter_new_player(conn, username_entry.get(), new_username_window))

    username_label.pack()
    username_entry.pack()
    username_button.pack()

def info(parent, message, title):
    info_window = tk.Toplevel(parent)
    info_window.title(title)
    height = 100
    width = 250
    info_window.geometry(f"{width}x{height}")
    message_label = tk.Label(info_window, text=message)
    ok_button = tk.Button(info_window, text="Ok", command=info_window.destroy)

    message_label.pack()
    ok_button.pack()

def confirm_player(conn, name, topWin):
    res = Database.get_player_id_by_name(conn, name)
    try:
        id = res[0][0]
        Database.db_connection("127.0.0.1", "root", "Pa$$w0rd", "Solitaire")
        """
        Add the function to add scores with the username.
        """
        Database.close_connection(conn)
    except:
        info(topWin, "player not found", "IMPORTANT!!!")
        return False

    topWin.destroy()
    root.destroy()
    ScoresWin.score_window()

def enter_new_player(conn, name, topWin):
    res = Database.get_player_id_by_name(conn, name)
    try:
        id = res[0][0]
        info(topWin, "player already existing", "IMPORTANT!!!")
        return False
    except:
        Database.db_connection("127.0.0.1", "root", "Pa$$w0rd", "Solitaire")
        Database.add_player(conn, name)
        print(name)
        """
        Add the function to add scores with the username.
        """
        Database.close_connection(conn)

    topWin.destroy()
    root.destroy()
    ScoresWin.score_window()

root = tk.Tk()
root.title("Login or Register")

question_label = tk.Label(root, text="Have you already played before?")
yes_button = tk.Button(root, text="Yes", command=get_username)
no_button = tk.Button(root, text="No", command=new_username)

question_label.pack()
yes_button.pack()
no_button.pack()

root.mainloop()

if __name__ == "__main__":
    save_game_score()