"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 20.08.24
Latest update: 20.08.24
Version : 0.1

Description:    this file contains the code for
                the first window to appear while launching the game.
"""

#Import
import tkinter as tk
from PIL import Image, ImageTk

#fonctions
def home_window():
    #Create the window
    home_page = tk.Tk()
    home_page.title("Klondike")
    height = 500
    width = 500
    home_page.geometry(f"{width}x{height}")

    #background color
    home_page.configure(background="green")

    #upload the cards' images

