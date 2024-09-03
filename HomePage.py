"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 20.08.24
Latest update: 03.09.24
Version : 0.1

Description:    this file contains the code for
                the first window to appear while launching the game.
"""

# Imports
import Game
import ScoresWin
import tkinter as tk
from PIL import Image, ImageTk

# variables

# fonctions
# fonction to launch the game
def start():
    global home_page
    home_page.destroy()
    Game.start_game()


# fonction to go to the highscores page
def see_scores():
    global score_window
    score_window.destroy()
    ScoresWin.score_window()



#homepage fonction
def home_window():
    global home_page
    #Create the window
    home_page = tk.Tk()
    home_page.title("Klondike")
    height = 500
    width = 500
    home_page.geometry(f"{width}x{height}")

    #background color
    home_page.configure(background="green")

    #get the location of the pictures
    image_location = "images/cards/"
    #upload the Ace cards' images
    heart_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_hearts.png"))
    club_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_clubs.png"))
    diamond_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_diamonds.png"))
    spade_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_spades.png"))

    #Labels creation
    label_heart_ace = tk.Label(home_page, image=heart_ace)
    label_club_ace = tk.Label(home_page, image=club_ace)
    label_diamond_ace = tk.Label(home_page, image=diamond_ace)
    label_spade_ace = tk.Label(home_page, image=spade_ace)

    #label placement
    label_heart_ace.place(relx=0.35, rely=0.25, anchor=tk.CENTER)
    label_club_ace.place(relx=0.45, rely=0.25, anchor=tk.CENTER)
    label_diamond_ace.place(relx=0.55, rely=0.25, anchor=tk.CENTER)
    label_spade_ace.place(relx=0.65, rely=0.25, anchor=tk.CENTER)

    #Buttons
    start_button = tk.Button(home_page, text="Start", font=("Arial", 16), command=start)
    start_button.place(relx=0.5, rely=0.60, anchor=tk.CENTER)

    button_score = tk.Button(home_page, text="Score", font=("Arial", 16))
    button_score.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

    #launch window
    home_page.mainloop()

home_window()