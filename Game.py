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

    # Charger l'image
    a_clubs = pygame.image.load("images/cards/ace_of_clubs.png")
    a_hearts = pygame.image.load("images/cards/ace_of_hearts.png")
    a_spades = pygame.image.load("images/cards/ace_of_spades.png")
    a_diamonds = pygame.image.load("images/cards/ace_of_diamonds.png")

    # Obtenir un rectangle à partir de l'image pour gérer les positions
    a_clubs_rect = a_clubs.get_rect()
    a_clubs_rect.topleft = (100, 100)  # Position initiale de l'image

    a_hearts_rect = a_hearts.get_rect()
    a_hearts_rect.topleft = (200, 100)  # Position initiale de l'image

    a_spades_rect = a_spades.get_rect()
    a_spades_rect.topleft = (300, 100)  # Position initiale de l'image

    a_diamonds_rect = a_diamonds.get_rect()
    a_diamonds_rect.topleft = (400, 100)  # Position initiale de l'image

    moving_a_clubs = False
    moving_a_hearts = False
    moving_a_spades = False
    moving_a_diamonds = False

    # Remplir l'écran avec la couleur vert foncé
    screen.fill(dark_green)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
            # Vérifier si la souris clique sur l'image
                if a_clubs_rect.collidepoint(event.pos):
                    moving_a_clubs = True
                    mouse_x, mouse_y = event.pos
                    offset_x = a_clubs_rect.x - mouse_x
                    offset_y = a_clubs_rect.y - mouse_y
                elif a_hearts_rect.collidepoint(event.pos):
                    moving_a_hearts = True
                    mouse_x, mouse_y = event.pos
                    offset_x = a_hearts_rect.x - mouse_x
                    offset_y = a_hearts_rect.y - mouse_y
                elif a_spades_rect.collidepoint(event.pos):
                    moving_a_spades = True
                    mouse_x, mouse_y = event.pos
                    offset_x = a_spades_rect.x - mouse_x
                    offset_y = a_spades_rect.y - mouse_y
                elif a_diamonds_rect.collidepoint(event.pos):
                    moving_a_diamonds = True
                    mouse_x, mouse_y = event.pos
                    offset_x = a_diamonds_rect.x - mouse_x
                    offset_y = a_diamonds_rect.y - mouse_y

            elif event.type == pygame.MOUSEBUTTONUP:
                moving_a_clubs = False
                moving_a_hearts = False
                moving_a_spades = False
                moving_a_diamonds = False

            elif event.type == pygame.MOUSEMOTION:
                if moving_a_clubs:
                    mouse_x, mouse_y = event.pos
                    a_clubs_rect.x = mouse_x + offset_x
                    a_clubs_rect.y = mouse_y + offset_y
                elif moving_a_hearts:
                    mouse_x, mouse_y = event.pos
                    a_hearts_rect.x = mouse_x + offset_x
                    a_hearts_rect.y = mouse_y + offset_y
                elif moving_a_spades:
                    mouse_x, mouse_y = event.pos
                    a_spades_rect.x = mouse_x + offset_x
                    a_spades_rect.y = mouse_y + offset_y
                elif moving_a_diamonds:
                    mouse_x, mouse_y = event.pos
                    a_diamonds_rect.x = mouse_x + offset_x
                    a_diamonds_rect.y = mouse_y + offset_y


        # Remplir l'écran avec la couleur vert foncé
        screen.fill(dark_green)

        # Dessiner l'image
        screen.blit(a_clubs, a_clubs_rect)
        screen.blit(a_hearts, a_hearts_rect)
        screen.blit(a_spades, a_spades_rect)
        screen.blit(a_diamonds, a_diamonds_rect)

        # Mettre à jour l'affichage
        pygame.display.flip()

