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
from tkinter import messagebox
import tkinter as tk
from PIL import Image, ImageTk

# Variables

# Functions
# Function to launch the game.
def start():
    global home_page
    home_page.destroy()
    tutoask = messagebox.askyesno("Tutorial", "Do you need a tutorial to learn how to play ???")
    if tutoask:
        tutorial = messagebox.showinfo("Tutorial", """Klondike Rules\n\n\nObjective: \nThe goal of Klondike is to move all the cards to the four foundation piles, one for each suit (Hearts, Diamonds, Clubs, Spades), starting with the Ace and ending with the King.\n\nSetup:\n1. Shuffle a standard 52-card deck.\n2. Deal seven piles of cards. The first pile has one card, the second has two, the third has three, and so on, up to the seventh pile which has seven cards. Only the top card of each pile is face up, the rest are face down.\n3. Place the remaining cards face down in a deck (also called the stock) in the upper left corner of the playing area.\n\nFoundations: \nThere are four foundation piles, one for each suit. Cards must be placed in ascending order (Ace to King) and sorted by suit.\n\nTableau:\n1. The tableau consists of the seven piles of cards dealt at the start of the game.\n2. Cards in the tableau are arranged in descending order (King to Ace) and alternating colors (red on black or black on red).\n\nStock and Waste Pile:\n1. The stock is the pile of leftover cards not dealt to the tableau.\n2. Draw one cards from the stock and place them face up in a waste pile.\n3. Only the top card of the waste pile can be played to the tableau or the foundations.\n\nRules for Moving Cards:\n1. Within the Tableau:\nMove cards between piles on the tableau in descending order and alternating colors. For example, a red 7 can only be placed on a black 8.\nYou can move a group of cards as long as they follow the descending sequence and alternate colors.\nIf a tableau pile is empty, only a King (or a sequence starting with a King) can be placed in the empty space.\n2. To the Foundations:\nYou can move cards from the tableau or the waste pile to the foundations if they are in the correct order and suit. For example, if a foundation pile has an Ace of Hearts, you can place the 2 of Hearts on top of it, followed by the 3 of Hearts, and so on.\n3. From the Stock:\nDraw cards from the stock and place them in the waste pile. You can play the top card of the waste pile to the tableau or foundations.\n\nWinning: \nYou win the game when all cards are moved to the four foundation piles in the correct order and suit, from Ace to King.\n\nLosing: \nIf you have exhausted all possible moves and the stock is empty, the game is over.""")
        if tutorial == "ok":
            Game.start_game()
    else:
        Game.start_game()


# Function to go to the highscores page.
def see_scores():
    global home_page
    home_page.destroy()
    ScoresWin.score_window()



# Homepage function
def home_window():
    global home_page
    #Create the window
    home_page = tk.Tk()
    home_page.title("Klondike Menu")
    height = 500
    width = 500
    home_page.geometry(f"{width}x{height}")

    # Background color.
    home_page.configure(background="green")

    # Get the location of the pictures.
    image_location = "images/cards/"
    # Upload the Ace cards' images.
    heart_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_hearts.png"))
    club_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_clubs.png"))
    diamond_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_diamonds.png"))
    spade_ace = ImageTk.PhotoImage(Image.open(image_location + "ace_of_spades.png"))

    # Labels creation.
    label_heart_ace = tk.Label(home_page, image=heart_ace)
    label_club_ace = tk.Label(home_page, image=club_ace)
    label_diamond_ace = tk.Label(home_page, image=diamond_ace)
    label_spade_ace = tk.Label(home_page, image=spade_ace)

    # Label placement.
    label_heart_ace.place(relx=0.35, rely=0.25, anchor=tk.CENTER)
    label_club_ace.place(relx=0.45, rely=0.25, anchor=tk.CENTER)
    label_diamond_ace.place(relx=0.55, rely=0.25, anchor=tk.CENTER)
    label_spade_ace.place(relx=0.65, rely=0.25, anchor=tk.CENTER)

    # Buttons
    # Button start.
    start_button = tk.Button(home_page, text="Start", font=("Arial", 16), command=start)
    start_button.place(relx=0.5, rely=0.60, anchor=tk.CENTER)
    # Button to open score page.
    button_score = tk.Button(home_page, text="Score", font=("Arial", 16), command=see_scores)
    button_score.place(relx=0.5, rely=0.70, anchor=tk.CENTER)

    # Launch window.
    home_page.mainloop()

home_window()