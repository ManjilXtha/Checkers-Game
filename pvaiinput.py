import pygame
from PIL import Image, ImageFilter
from choose_piece import choose_piece_screen

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers Game - Input Screen")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
RED = (255, 69, 58)

# Fonts
title_font_path = "resources/Neometra-Caps-FFP.ttf"  # Replace with the correct path to your font file
try:
    title_font = pygame.font.Font(title_font_path, 60)
except FileNotFoundError:
    print("Font file not found. Using default font.")
    title_font = pygame.font.Font(None, 60)

font = pygame.font.Font(None, 36)

# Load and blur background image
background_image_path = "resources/ch2.jpg"  # Replace with the correct path to your image
background_image = Image.open(background_image_path).resize((SCREEN_WIDTH, SCREEN_HEIGHT))
blurred_image = background_image.filter(ImageFilter.GaussianBlur(radius=10))
blurred_image.save("resources/blurred_background.png")
pygame_background_image = pygame.image.load("resources/blurred_background.png")


def draw_text_with_stroke(surface, text, font, text_color, stroke_color, x, y, align="center"):
    """Draw text with a stroke (outline)."""
    text_surface = font.render(text, True, stroke_color)
    text_rect = text_surface.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect.topleft = (x, y)

    # Draw stroke
    offsets = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for offset in offsets:
        shadow_rect = text_rect.copy()
        shadow_rect.move_ip(*offset)
        surface.blit(font.render(text, True, stroke_color), shadow_rect)

    # Draw main text
    surface.blit(font.render(text, True, text_color), text_rect)


def draw_text(surface, text, font, color, x, y, align="center"):
    """Draws centered text on the screen."""
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if align == "center":
        text_rect.center = (x, y)
    elif align == "left":
        text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def text_input_box(surface, x, y, width, height, active, text, placeholder="Enter your name"):
    """Draws a text input box with placeholder."""
    color = BLUE if active else GRAY
    pygame.draw.rect(surface, WHITE, (x, y, width, height), border_radius=10)
    pygame.draw.rect(surface, color, (x, y, width, height), 2, border_radius=10)
    placeholder_color = GRAY if not text else BLACK
    draw_text(surface, text if text else placeholder, font, placeholder_color, x + width // 2, y + height // 2)


def draw_button(surface, text, rect, background_color, text_color, hover=False):
    """Draws a button."""
    button_color = background_color
    if hover:
        button_color = tuple(min(c + 20, 255) for c in button_color)
    pygame.draw.rect(surface, button_color, rect, border_radius=10)
    draw_text(surface, text, font, text_color, rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)


def pvai_input_screen():
    """Handles the Player vs AI input screen."""
    input_active = False
    input_text = ""
    running = True

    while running:
        screen.blit(pygame_background_image, (0, 0))  # Draw blurred background

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 550 and 200 <= event.pos[1] <= 240:
                    input_active = True
                else:
                    input_active = False
                    back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 100, 40)
                    if back_button_rect.collidepoint(event.pos):
                        print("Going back to the previous screen")
                        return {"player_name": "back"}
            if event.type == pygame.KEYDOWN:
                if input_active:
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    elif event.key == pygame.K_RETURN:
                        if input_text.strip():
                            print(f"Player Name: {input_text}")
                            return 
                    else:
                        input_text += event.unicode

        # Title
        draw_text_with_stroke(
            screen, "Player Input Screen", title_font, BLACK, WHITE, SCREEN_WIDTH // 2, 50
        )

        # Input box
        text_input_box(screen, 250, 200, 300, 40, input_active, input_text)

        # Buttons
        mouse_pos = pygame.mouse.get_pos()
        next_button_rect = pygame.Rect(325, 450, 150, 50)
        next_enabled = bool(input_text.strip())
        next_hover = next_button_rect.collidepoint(mouse_pos) if next_enabled else False
        next_text_color = BLACK if not next_enabled else WHITE
        next_background_color = GRAY if not next_enabled else RED

        draw_button(
            screen, "Next", next_button_rect, next_background_color, next_text_color, next_hover
        )

        back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 100, 40)
        back_hover = back_button_rect.collidepoint(mouse_pos)
        draw_button(screen, "Back", back_button_rect, BLACK, WHITE, back_hover)

        # Check Next button click
        if next_enabled and pygame.mouse.get_pressed()[0] and next_button_rect.collidepoint(mouse_pos):
            print(f"Player Name: {input_text}")
            return{
                "player_name":input_text
            }

        pygame.display.flip()


# Run the input screen
# pvai_input_screen()
# pygame.quit()
