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


def draw_card_from_stock(card_rectangles, stock_pile, drawn_cards):
    """
    Draw a card from the stockpile and place it on the draw pile (empty slot).
    Update the card rectangles to reflect the drawn card's position.
    """
    if stock_pile:  # Only draw if there are cards in the stockpile
        card_name = stock_pile.pop()  # Get the top card from the stockpile
        draw_pile_rect = card_rectangles['draw_pile']["rect"]

        # Update the drawn card's position (place it directly on top of the draw pile)
        new_rect = card_rectangles[card_name]["rect"]
        new_rect.topleft = draw_pile_rect.topleft  # Correctly place it over the draw pile
        card_rectangles[card_name] = {"rect": new_rect, "face_up": True, "drawn": True}

        drawn_cards.append(card_name)  # Track the drawn card


def draw_card_piles(screen, card_rectangles, card_images, slots_images, tableau_piles, foundation_piles, stock_pile, drawn_cards):
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
    if stock_pile:  # Only draw the stockpile if it still has cards.
        for card_name, card_info in card_rectangles.items():
            if "stock" in card_info and not card_info.get("drawn"):
                rect = card_info["rect"]
                screen.blit(slots_images["python_card_back"], rect)

    # Draw the draw pile (empty slot or the drawn card)
    if not drawn_cards:
        screen.blit(slots_images["empty_slot"], card_rectangles['draw_pile']["rect"])  # Empty slot
    else:
        # If there is a drawn card, draw the topmost drawn card on the draw pile
        top_drawn_card = drawn_cards[-1]  # Get the topmost drawn card
        card_info = card_rectangles[top_drawn_card]
        screen.blit(card_images[top_drawn_card], card_info["rect"])


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

    # Convert dictionary to list for ordered drawing
    card_rect_list = list(card_rectangles.items())

    # Variables to follow the state of the movement.
    dragging = False
    dragged_card = None
    offset_x = 0
    offset_y = 0

    # Track drawn cards separately
    drawn_cards = []

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the stockpile is clicked to draw a card to the draw pile
                if stock_pile and card_rectangles[stock_pile[-1]]["rect"].collidepoint(event.pos):
                    draw_card_from_stock(card_rectangles, stock_pile, drawn_cards)

                # Check if the mouse clicked on a card.
                for i, (card_name, card_info) in enumerate(card_rect_list):
                    rect = card_info["rect"]
                    if rect.collidepoint(event.pos) and card_info["face_up"]:
                        dragging = True
                        dragged_card = card_name
                        offset_x = rect.x - event.pos[0]
                        offset_y = rect.y - event.pos[1]

                        # Move the dragged card to the end of the list for drawing last (on top)
                        card_rect_list.append(card_rect_list.pop(i))
                        break

            elif event.type == pygame.MOUSEBUTTONUP:
                if dragging and dragged_card:
                    # After releasing the card, stop dragging.
                    dragging = False
                    dragged_card = None

            elif event.type == pygame.MOUSEMOTION:
                if dragging and dragged_card:
                    # Move the card with the mouse
                    for card_name, card_info in card_rect_list:
                        if card_name == dragged_card:
                            card_info["rect"].x = event.pos[0] + offset_x
                            card_info["rect"].y = event.pos[1] + offset_y

        screen.fill(dark_green)

        # Draw all card piles including stock, foundations (with ace slots), tableau (with empty slots), and draw pile.
        draw_card_piles(screen, card_rectangles, card_images, slots_images, tableau_piles, foundation_piles, stock_pile, drawn_cards)

        # Draw the cards in order
        for card_name, card_info in card_rect_list:
            if "rect" in card_info:
                rect = card_info["rect"]
                if "face_up" in card_info and card_info["face_up"]:
                    screen.blit(card_images[card_name], rect)  # Draw face-up cards.

        pygame.display.flip()


if __name__ == "__main__":
    start_game()
