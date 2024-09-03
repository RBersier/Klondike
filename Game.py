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
import os


def load_images(folder_path):
    """ Charge toutes les images de cartes à partir du dossier spécifié. """
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            card_name = filename.split(".")[0]
            images[card_name] = pygame.image.load(os.path.join(folder_path, filename))
    return images


def initialize_rectangles(images, start_x=100, start_y=100, spacing_x=50):
    """ Initialise les rectangles des cartes avec des positions espacées horizontalement. """
    rectangles = {}
    x, y = start_x, start_y
    for card_name in images.keys():
        rect = images[card_name].get_rect(topleft=(x, y))
        rectangles[card_name] = rect
        # Espacement horizontal pour la prochaine carte
        x += spacing_x
        # Si les cartes dépassent la largeur de l'écran, passe à la ligne suivante
        if x > 1280 - spacing_x:
            x = start_x
            y += 50  # Espacement vertical
    return rectangles


def start_game():
    pygame.init()

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    dark_green = (0, 100, 0)

    # Charger toutes les images de cartes
    card_images = load_images("images/cards")

    # Initialiser les rectangles pour chaque carte
    card_rectangles = initialize_rectangles(card_images)

    # Variables pour suivre l'état de déplacement
    dragging = False
    dragged_card = None
    offset_x = 0
    offset_y = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Vérifier si la souris clique sur une carte
                for card_name, rect in card_rectangles.items():
                    if rect.collidepoint(event.pos):
                        dragging = True
                        dragged_card = card_name
                        offset_x = rect.x - event.pos[0]
                        offset_y = rect.y - event.pos[1]
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                dragging = False
                dragged_card = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging and dragged_card:
                    # Déplacer la carte avec la souris
                    card_rectangles[dragged_card].x = event.pos[0] + offset_x
                    card_rectangles[dragged_card].y = event.pos[1] + offset_y

        screen.fill(dark_green)

        # Dessiner toutes les cartes à leurs positions
        for card_name, rect in card_rectangles.items():
            screen.blit(card_images[card_name], rect)

        pygame.display.flip()