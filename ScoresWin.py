"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 03.09.24
Latest update: 24.09.24
Version : 0.2

Description:    this file contains the code for
                the window with the highscores board of the game.
"""

# Imports
from Database import db_connection, close_connection, get_top_scores
import tkinter as tk
from tkinter import ttk

# Functions
def show_scoreboard(parent):
    global score_window, treeview
    """Displays a scoreboard window.

    Args:
        parent: The parent window.
    """

    # Create a treeview widget
    style = ttk.Style(parent)
    style.configure("Treeview", background="green", foreground="white")

    treeview = ttk.Treeview(parent, columns=("rank", "player", "score", "date"))
    treeview.heading("rank", text="Rank")
    treeview.heading("player", text="Player")
    treeview.heading("score", text="Score")
    treeview.heading("date", text="Date")
    treeview.column("rank", width=50)
    treeview.column("player", width=150)
    treeview.column("score", width=100)
    treeview.column("date", width=150)
    treeview.pack(fill="both", expand=True)

    # Load the scores initially
    load_scores()

    # Create a button to close the window
    close_button = tk.Button(parent, text="Close", command=parent.destroy)
    close_button.pack(side="bottom", padx=10, pady=10)

# Load the top scores from the database
def load_scores():
    try:
        # Open the database connection
        conn = db_connection(host="127.0.0.1", password="Pa$$w0rd", user="CPNV", database="solitaire")

        # Get the top scores from the database
        top_scores = get_top_scores(conn)

        # Clear the treeview
        treeview.delete(*treeview.get_children())

        # Insert the scores into the treeview
        for i, (player, score, date) in enumerate(top_scores, start=1):
            print()
            treeview.insert("", "end", values=(i, player, score, date))

        # Close the database connection
        close_connection(conn)
    except Exception as e:
        # Handle database connection or query errors
        print(f"Error loading scores: {e}")

def score_window():
    global home_page
    #Create the window
    score_page = tk.Tk()
    score_page.title("Klondike Scores")
    # background color
    score_page.configure(background="green")
    show_scoreboard(score_page)
    #launch window
    score_page.mainloop()