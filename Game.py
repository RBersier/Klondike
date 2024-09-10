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

# Imports
import pygame
import sys
import os


def load_images(folder_path):
    # Charge all the cards' pictures from a specified folder.
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            card_name = filename.split(".")[0]
            images[card_name] = pygame.image.load(os.path.join(folder_path, filename))
    return images


def initialize_rectangles(images, start_x=100, start_y=100, spacing_x=50):
    # Initialise the rectangles of the cards with positions horizontally spaced.
    rectangles = {}
    x, y = start_x, start_y
    for card_name in images.keys():
        rect = images[card_name].get_rect(topleft=(x, y))
        rectangles[card_name] = rect
        # Horizontal space with the next card.
        x += spacing_x
        # If the cards appear out of the window, make then appear one line bellow.
        if x > 1280 - spacing_x:
            x = start_x
            y += 50  # Vertical space.
    return rectangles


def start_game():
    pygame.init()

    #whindow's top part
    pygame.display.set_caption("Klondike Game")

    screen_width = 1280
    screen_height = 720
    screen = pygame.display.set_mode((screen_width, screen_height))

    dark_green = (0, 100, 0)

    # Charge all cards picture.
    card_images = load_images("images/cards")

    # Initialize the rectangles for each card
    card_rectangles = initialize_rectangles(card_images)

    # Variables to follow the state of the movement.
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
                # Check if the pointer clic on a card.
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
                    # move the card with the pointer.
                    card_rectangles[dragged_card].x = event.pos[0] + offset_x
                    card_rectangles[dragged_card].y = event.pos[1] + offset_y

        screen.fill(dark_green)

        # Draw all cards on their position.
        for card_name, rect in card_rectangles.items():
            screen.blit(card_images[card_name], rect)

        pygame.display.flip()