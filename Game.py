"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 20.08.24
Latest update: 03.09.24
Version : 0.1

Description:    this file contains the code for
                running the game correctly.
"""

# imports
import pygame
import sys

# Boucle principale
def start_game():
    # Initialiser Pygame
    pygame.init()

    # Définir la taille de la fenêtre
    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    # Définir la couleur vert foncé (R, G, B)
    dark_green = (0, 100, 0)

    # Remplir l'écran avec la couleur vert foncé
    screen.fill(dark_green)

    # Mettre à jour l'affichage
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
