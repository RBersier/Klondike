"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 03.09.24
Latest update: 03.09.24
Version : 0.1

Description:    this file contains the code for
                the window with the highscores board of the game.
"""

# Imports
import tkinter as tk
import HomePage

def score_window():
    global home_page
    #Create the window
    score_page = tk.Tk()
    score_page.title("Klondike")
    height = 800
    width = 800
    score_page.geometry(f"{width}x{height}")
    #launch window
    score_window.mainloop()
