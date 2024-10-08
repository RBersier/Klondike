"""
Project : Klondike
Module : Projet Dev
Author : Ryan BERSIER & Alexis LEAKOS
Start date: 03.09.24
Latest update: 08.10.24
Version : 0.3

Description:    this file contains the code
                for the game.
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
    spacing_x = 110
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
    draw_pile_rect = pygame.Rect(stock_x + 110, stock_y, 71, 96)
    rectangles['draw_pile'] = {"rect": draw_pile_rect, "face_up": False, "draw_pile": True}

    # Foundation piles (for each ace) starting empty, defined by positions.
    foundation_x_start = 380
    foundation_y = 50
    for i in range(4):
        foundation_rect = pygame.Rect(foundation_x_start + i * spacing_x, foundation_y, 71, 96)
        rectangles[f'foundation_{i}'] = {"rect": foundation_rect, "face_up": False, "foundation": i}

    return rectangles, tableau_piles, foundation_piles, stock_pile


def draw_card_from_stock(card_rectangles, stock_pile, unified_card_list):
    """
    Draw a card from the stockpile and place it on the draw pile (empty slot).
    Update the card rectangles to reflect the drawn card's position.
    """
    if stock_pile:  # Only draw if there are cards in the stockpile
        card_name = stock_pile.pop()  # Get the top card from the stockpile
        draw_pile_rect = card_rectangles['draw_pile']["rect"]

        # Update the drawn card's position (place it directly on top of the draw pile)
        new_rect = card_rectangles[card_name]["rect"]
        new_rect.topleft = draw_pile_rect.topleft  # Place it over the draw pile, without changing the empty slot

        card_rectangles[card_name] = {"rect": new_rect, "face_up": True, "movable": True}  # Mark the drawn card as movable

        unified_card_list.append((card_name, card_rectangles[card_name]))  # Add it to the unified card list


def draw_card_piles(screen, card_rectangles, card_images, slots_images, tableau_piles, foundation_piles, stock_pile):
    """
    Draw all the card piles (tableau, stock, foundations) and empty slots.
    """
    # Draw foundation slots (ace piles)
    foundation_slots = ["ace_of_clubs_slot", "ace_of_diamonds_slot", "ace_of_hearts_slot", "ace_of_spades_slot"]
    for i, slot_name in enumerate(foundation_slots):
        foundation_key = f'foundation_{i}'
        rect = card_rectangles[foundation_key]["rect"]

        # If the foundation pile is empty, show the empty slot image for that foundation
        if len(foundation_piles[i]) == 0:
            screen.blit(slots_images[slot_name], rect)
        else:
            # If foundation has cards, draw the top card (face-up)
            top_card = foundation_piles[i][-1]
            screen.blit(card_images[top_card], rect)

    # Draw tableau slots (empty slots for tableau piles)
    for i in range(7):
        if len(tableau_piles[i]) == 0:  # If a tableau pile is empty, draw the empty slot.
            tableau_rect = pygame.Rect(50 + i * 110, 300, 71, 96)  # Adjusted Y for tableau slots
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
    if stock_pile:  # Only draw the stockpile if it still has cards.
        for card_name, card_info in card_rectangles.items():
            if "stock" in card_info and not card_info.get("drawn"):
                rect = card_info["rect"]
                screen.blit(slots_images["python_card_back"], rect)

    # Draw the draw pile (empty slot)
    draw_pile_rect = card_rectangles['draw_pile']["rect"]
    screen.blit(slots_images["empty_slot"], draw_pile_rect)


def is_valid_move(top_card_name, dragged_card_name):
    """
    Check if the dragged card can be placed on top of the top card in a tableau pile.
    Klondike rules:
    - The dragged card must be one rank lower than the top card.
    - The dragged card must be of the opposite color.
    """
    # Extract rank and suit information from the card names (e.g., 'ace_of_spades', '2_of_hearts', etc.)
    top_rank, top_suit = top_card_name.split("_")[0], top_card_name.split("_")[2]
    dragged_rank, dragged_suit = dragged_card_name.split("_")[0], dragged_card_name.split("_")[2]

    # Define the rank order for comparison
    rank_order = ["ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "jack", "queen", "king"]

    # Check if the dragged card is one rank lower and is of opposite color
    return (rank_order.index(dragged_rank) == rank_order.index(top_rank) - 1) and \
        (is_opposite_color(top_suit, dragged_suit))


def is_opposite_color(suit1, suit2):
    """ Check if two suits are of opposite colors (red vs black) """
    red_suits = {"hearts", "diamonds"}
    black_suits = {"spades", "clubs"}

    return (suit1 in red_suits and suit2 in black_suits) or (suit1 in black_suits and suit2 in red_suits)


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
    card_rectangles, tableau_piles, foundation_piles, stock_pile = initialize_rectangles_for_klondike(card_images,
                                                                                                      slots_images)

    # Unified card list: keeps track of all cards to ensure proper z-order (draw order)
    unified_card_list = []

    # Add all tableau and foundation cards to the unified card list for z-order management
    for card_name, card_info in card_rectangles.items():
        if "tableau" in card_info or "foundation" in card_info:
            unified_card_list.append((card_name, card_info))

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
                # Check if the stockpile is clicked to draw a card to the draw pile
                if stock_pile and card_rectangles[stock_pile[-1]]["rect"].collidepoint(event.pos):
                    draw_card_from_stock(card_rectangles, stock_pile, unified_card_list)

                # Check if the mouse clicked on any card (tableau, foundation, or drawpile)
                for i, (card_name, card_info) in enumerate(
                        reversed(unified_card_list)):  # Iterate in reverse to check topmost cards first
                    rect = card_info["rect"]

                    tableau_index = card_info.get("tableau")
                    if rect.collidepoint(event.pos) and card_info.get("face_up") and tableau_index is not None:
                        clicked_card_index = tableau_piles[tableau_index].index(card_name)

                        # Check if all cards below the clicked card form a valid stack
                        valid_stack = True
                        cards_to_move = [card_name]  # Start with the clicked card
                        for j in range(clicked_card_index, len(tableau_piles[tableau_index]) - 1):
                            card1 = tableau_piles[tableau_index][j]
                            card2 = tableau_piles[tableau_index][j + 1]

                            if not is_valid_move(card1, card2):
                                valid_stack = False
                                break
                            cards_to_move.append(card2)  # Add the next card in the stack

                        # If it's a valid stack or the top card, allow dragging
                        if valid_stack:
                            dragging = True
                            dragged_cards = cards_to_move  # Store all cards in the stack to be moved
                            offset_x = rect.x - event.pos[0]
                            offset_y = rect.y - event.pos[1]
                            # Move the entire stack to the front of the unified card list
                            for card in cards_to_move:
                                unified_card_list.pop(unified_card_list.index((card, card_rectangles[card])))
                                unified_card_list.append(
                                    (card, card_rectangles[card]))  # Ensure all cards in the stack are drawn on top
                            break
            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and dragged_cards:
                    dragging = False
                    valid_drop = False

                    # Try to place the cards on one of the tableau piles
                    tableau_index = card_rectangles[dragged_cards[0]].get("tableau")
                    original_tableau_index = tableau_index  # Track the original tableau pile the cards came from

                    for new_tableau_index in range(7):  # Check if the cards are dropped on any tableau pile
                        tableau_rect = pygame.Rect(50 + new_tableau_index * 110,
                                                   175 + len(tableau_piles[new_tableau_index]) * 30, 71, 96)

                        if tableau_rect.collidepoint(event.pos):
                            # Check if the move is valid according to the rules
                            if len(tableau_piles[new_tableau_index]) == 0:  # Empty tableau pile accepts only King
                                if dragged_cards[0].startswith('king'):
                                    for card in dragged_cards:
                                        tableau_piles[new_tableau_index].append(card)
                                        card_rectangles[card]["tableau"] = new_tableau_index
                                    valid_drop = True
                            else:
                                top_card = tableau_piles[new_tableau_index][-1]
                                if is_valid_move(top_card, dragged_cards[0]):
                                    for card in dragged_cards:
                                        tableau_piles[new_tableau_index].append(card)
                                        card_rectangles[card]["tableau"] = new_tableau_index
                                    valid_drop = True

                    # If the move is valid and the cards were moved to a different pile
                    if valid_drop and original_tableau_index != new_tableau_index:
                        # Remove the dragged cards from the original tableau pile
                        for card in dragged_cards:
                            tableau_piles[original_tableau_index].remove(card)

                        # Flip the next card in the original pile, if there is one
                        if tableau_piles[original_tableau_index]:
                            top_card = tableau_piles[original_tableau_index][-1]
                            if not card_rectangles[top_card]["face_up"]:
                                card_rectangles[top_card]["face_up"] = True
                                card_rectangles[top_card]["movable"] = True

                    # If the move is invalid, return the cards to their original position
                    if not valid_drop:
                        for index, card in enumerate(dragged_cards):
                            original_position = (
                            50 + original_tableau_index * 110, 175 + (clicked_card_index + index) * 30)
                            card_rectangles[card]["rect"].topleft = original_position

                    # Reset dragged_cards variable
                    dragged_cards = None


            elif event.type == pygame.MOUSEMOTION:
                if dragging and dragged_cards:
                    # Move all the dragged cards together
                    for index, card_name in enumerate(dragged_cards):
                        card_info = card_rectangles[card_name]
                        card_info["rect"].x = event.pos[0] + offset_x
                        card_info["rect"].y = event.pos[1] + offset_y + (index * 30)  # Maintain stack spacing while dragging

        screen.fill(dark_green)

        # Draw all card piles including stock, foundations (with ace slots), tableau (with empty slots), and draw pile.
        draw_card_piles(screen, card_rectangles, card_images, slots_images, tableau_piles, foundation_piles, stock_pile)

        # Draw the cards from the unified list in the correct order (last card in the list will be drawn on top)
        for card_name, card_info in unified_card_list:
            if "rect" in card_info:
                rect = card_info["rect"]
                if "face_up" in card_info and card_info["face_up"]:
                    screen.blit(card_images[card_name], rect)  # Draw face-up cards.

        pygame.display.flip()


if __name__ == "__main__":
    start_game()
