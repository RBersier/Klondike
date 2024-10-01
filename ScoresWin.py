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
    """Displays a scoreboard window.

    Args:
        parent: The parent window.
    """

    # Create the main window
    scoreboard_window = tk.Toplevel(parent)
    scoreboard_window.title("Scoreboard")

    # Create a treeview widget
    treeview = ttk.Treeview(scoreboard_window, columns=("rank", "player", "score", "date"))
    treeview.heading("player", text="Player")
    treeview.heading("score", text="Score")
    treeview.heading("date", text="Date")
    treeview.column("rank", width=50)
    treeview.column("player", width=150)
    treeview.column("score", width=100)
    treeview.column("date", width=150)
    treeview.pack(fill="both", expand=True)

    # Load the top scores from the database
    def load_scores():
        try:
            # Open the database connection
            db_connection()

            # Get the top scores from the database
            top_scores = get_top_scores()

            # Clear the treeview
            treeview.delete(*treeview.get_children())

            # Insert the scores into the treeview
            for i, (rank, player, score, date) in enumerate(top_scores, start=1):
                treeview.insert("", "end", values=(i, player, score, date))

            # Close the database connection
            close_connection()
        except Exception as e:
            # Handle database connection or query errors
            print(f"Error loading scores: {e}")

    # Load the scores initially
    load_scores()

    # Create a button to close the window
    close_button = tk.Button(scoreboard_window, text="Close", command=scoreboard_window.destroy)
    close_button.pack(side="bottom", padx=10, pady=10)

    # Start the main loop for the scoreboard window
    scoreboard_window.mainloop()

def score_window():
    global home_page
    #Create the window
    score_page = tk.Tk()
    score_page.title("Klondike Scores")
    height = 800
    width = 800
    score_page.geometry(f"{width}x{height}")
    # background color
    score_page.configure(background="green")
    #launch window
    score_page.mainloop()
