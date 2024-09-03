"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 20.08.24
Latest update: 20.08.24
Version : 0.1

Description:    this file contains the code for
                running the game correctly.
"""

# imports
import arcade

# Définir les dimensions de la fenêtre et nom
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Klondike"

# Couleur vert foncé (en RGB)
DARK_GREEN = (0, 100, 0, 1)


def on_draw(delta_time):
    """ Fonction de dessin, appelée à chaque image """
    arcade.clear()
    # Ici, nous ne faisons que remplir l'écran avec la couleur de fond
    # Cette fonction sera appelée automatiquement par arcade.run()


def main():
    # Ouvrir la fenêtre
    arcade.open_window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Définir la couleur de fond à vert foncé
    arcade.set_background_color(DARK_GREEN)

    # Spécifier la fonction de dessin avec le temps entre les appels
    arcade.schedule(on_draw, 1 / 60)  # Appelle on_draw à 60 FPS

    # Démarrer la boucle de rendu
    arcade.run()

main()

