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
import tkinter as tk
from tkinter import ttk
from Database import open_dbconnection, close_dbconnection, get_top_scores

# functions
class ScoreboardWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Scoreboard")

        # Create a treeview widget to display the scores
        self.treeview = ttk.Treeview(self, columns=("rank", "player", "score", "date"))
        self.treeview.heading("rank", text="Rank")
        self.treeview.heading("player", text="Player")
        self.treeview.heading("score", text="Score")
        self.treeview.heading("date", text="Date")
        self.treeview.column("rank", width=50)
        self.treeview.column("player", width=150)
        self.treeview.column("score", width=100)
        self.treeview.column("date", width=150)
        self.treeview.pack(fill="both", expand=True)

        # Button to close the window
        close_button = tk.Button(self, text="Close", command=self.destroy)
        close_button.pack(side="bottom", padx=10, pady=10)

        # Load the top scores from the database
        self.load_scores()

    def load_scores(self):
        # Open the database connection
        open_dbconnection()

        # Get the top scores from the database
        top_scores = get_top_scores()

        # Clear the treeview
        self.treeview.delete(*self.treeview.get_children())

        # Insert the scores into the treeview
        for i, (rank, player, score, date) in enumerate(top_scores, start=1):
            self.treeview.insert("", "end", values=(i, player, score, date))

        # Close the database connection
        close_dbconnection()

def show_scoreboard(parent):
    scoreboard_window = ScoreboardWindow(parent)
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
