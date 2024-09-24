"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 03.09.24
Latest update: 24.09.24
Version : 0.2

Description:    this file contains the code
                for the game
"""

# Imports
import pygame
import sys
import os
import random

def load_images(folder_path):
    # Load all the images from the specified folder.
    images = {}
    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            card_name = filename.split(".")[0]
            images[card_name] = pygame.image.load(os.path.join(folder_path, filename))
    return images

def initialize_rectangles_for_klondike(images, slots_images):
    """
    Initialize rectangles for Klondike with 7 tableau piles, stockpile, and 4 foundations.
    Also initialize the draw pile and the area where the drawn card will be displayed.
    """
    rectangles = {}
    tableau_piles = [[] for _ in range(7)]
    foundation_piles = [[] for _ in range(4)]  # 4 foundation piles for each suit
    stock_pile = []

    # Shuffle the deck for Klondike setup.
    deck = list(images.keys())
    random.shuffle(deck)

    # Distribute cards to tableau piles with only the top card face-up.
    start_x = 50
    spacing_x = 110  # Reduced the spacing a bit
    for i in range(7):
        for j in range(i + 1):  # Incrementally more cards in each pile.
            card_name = deck.pop()
            rect = images[card_name].get_rect(topleft=(start_x + i * spacing_x, 175 + j * 30))  # Adjust Y for tableau
            if j == i:  # Only top card is face-up.
                rectangles[card_name] = {"rect": rect, "face_up": True, "tableau": i, "index": j}
            else:
                rectangles[card_name] = {"rect": rect, "face_up": False, "tableau": i, "index": j}
            tableau_piles[i].append(card_name)

    # Stockpile at the top left (left side of the screen).
    stock_x, stock_y = 50, 50
    for card_name in deck:
        rect = images[card_name].get_rect(topleft=(stock_x, stock_y))  # Stockpile at top left.
        rectangles[card_name] = {"rect": rect, "face_up": False, "stock": True}
        stock_pile.append(card_name)

    # Draw pile rectangle (next to the stockpile).
    draw_pile_rect = pygame.Rect(stock_x + 110, stock_y, 71, 96)  # Adjusted x to bring closer to stockpile
    rectangles['draw_pile'] = {"rect": draw_pile_rect, "face_up": False, "draw_pile": True}

    # Foundation piles start empty, but we'll define their positions.
    foundation_x_start = 380  # Reduced to bring foundation closer
    foundation_y = 50
    for i in range(4):
        foundation_rect = pygame.Rect(foundation_x_start + i * spacing_x, foundation_y, 71, 96)  # 71x96 is standard card size
        rectangles[f'foundation_{i}'] = {"rect": foundation_rect, "face_up": False, "foundation": i}

    return rectangles, tableau_piles, foundation_piles, stock_pile

def draw_card_piles(screen, card_rectangles, card_images, slots_images, tableau_piles, foundation_piles):
    """
    Draw all the card piles (tableau, stock, foundations) and empty slots.
    """
    # Draw foundation slots (ace piles)
    foundation_slots = ["ace_of_clubs_slot", "ace_of_diamonds_slot", "ace_of_hearts_slot", "ace_of_spades_slot"]
    for i, slot_name in enumerate(foundation_slots):
        foundation_key = f'foundation_{i}'
        rect = card_rectangles[foundation_key]["rect"]
        if len(foundation_piles[i]) == 0:  # If foundation is empty, draw the specific ace slot image
            screen.blit(slots_images[slot_name], rect)
        else:
            # If foundation has cards, draw the top card (face-up)
            top_card = foundation_piles[i][-1]
            screen.blit(card_images[top_card], rect)

    # Draw tableau slots (empty slots for tableau piles)
    for i in range(7):
        if len(tableau_piles[i]) == 0:  # If a tableau pile is empty, draw the empty slot.
            tableau_rect = pygame.Rect(50 + i * 110, 300, 71, 96)  # Reduced spacing between tableau slots
            screen.blit(slots_images["empty_slot"], tableau_rect)
        else:
            # Draw cards (face-up and face-down cards in tableau)
            for card_name in tableau_piles[i]:
                card_info = card_rectangles[card_name]
                rect = card_info["rect"]
                if card_info["face_up"]:
                    screen.blit(card_images[card_name], rect)  # Draw face-up cards.
                else:
                    screen.blit(slots_images["python_card_back"], rect)  # Draw face-down cards (card back).

    # Draw stockpile cards (on the far left)
    for card_name, card_info in card_rectangles.items():
        if "stock" in card_info:
            rect = card_info["rect"]
            screen.blit(slots_images["python_card_back"], rect)

    # Draw the draw pile (empty slot next to the stockpile)
    screen.blit(slots_images["empty_slot"], card_rectangles['draw_pile']["rect"])

def start_game():
    global screen
    pygame.init()

    # Window setup
    pygame.display.set_caption("Klondike Game")
    screen_width = 850
    screen_height = 850
    screen = pygame.display.set_mode((screen_width, screen_height))

    dark_green = (0, 100, 0)

    # Load all card images and slot images
    card_images = load_images("images/cards")
    slots_images = load_images("images/slots")

    # Initialize card rectangles for Klondike
    card_rectangles, tableau_piles, foundation_piles, stock_pile = initialize_rectangles_for_klondike(card_images, slots_images)

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
                # Check if the mouse clicked on a card.
                for card_name, card_info in card_rectangles.items():
                    rect = card_info["rect"]
                    if rect.collidepoint(event.pos) and card_info["face_up"]:
                        dragging = True
                        dragged_card = card_name
                        offset_x = rect.x - event.pos[0]
                        offset_y = rect.y - event.pos[1]
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and dragged_card:
                    # After releasing the card, stop dragging.
                    dragging = False
                    dragged_card = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging and dragged_card:
                    # Move the card with the mouse
                    card_rectangles[dragged_card]["rect"].x = event.pos[0] + offset_x
                    card_rectangles[dragged_card]["rect"].y = event.pos[1] + offset_y

        screen.fill(dark_green)

        # Draw all card piles including stock, foundations (with ace slots), tableau (with empty slots), and draw pile.
        draw_card_piles(screen, card_rectangles, card_images, slots_images, tableau_piles, foundation_piles)

        pygame.display.flip()

if __name__ == "__main__":
    start_game()
