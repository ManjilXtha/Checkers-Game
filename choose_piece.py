import pygame
from PIL import Image, ImageFilter

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
RED = (255, 69, 58)
DARK_RED = (200, 0, 0)
HIGHLIGHT_COLOR = (50, 205, 50)  # Highlight green
HOVER_GREEN = (144, 238, 144)  # Lighter shade of green
HOVER_RED = (255, 99, 71)  # Lighter red for hover effect

# Initialize Pygame
pygame.init()

# Fonts
label_font = pygame.font.Font(None, 24)  # Font for "Red" and "White"
button_font = pygame.font.Font(None, 24)  # Font for "Start Game"
title_font = pygame.font.Font("resources/Neometra-Caps-FFP.ttf", 48)

# Load and blur background image
background_image = Image.open("resources/ch2.jpg")
background_image = background_image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
blurred_image = background_image.filter(ImageFilter.GaussianBlur(radius=10))
blurred_image.save("resources/blurred_background1.png")
pygame_background_image = pygame.image.load("resources/blurred_background1.png")

# Load piece images
red_piece_image = pygame.image.load("resources/red_piece.png")
white_piece_image = pygame.image.load("resources/white_piece.png")

# Resize piece images
piece_size = (100, 100)
red_piece_image = pygame.transform.scale(red_piece_image, piece_size)
white_piece_image = pygame.transform.scale(white_piece_image, piece_size)

def draw_text_with_stroke(text, font, text_color, stroke_color, surface, x, y, stroke_width=2):
    text_surface = font.render(text, True, stroke_color)
    text_rect = text_surface.get_rect(center=(x, y))

    for dx in [-stroke_width, 0, stroke_width]:
        for dy in [-stroke_width, 0, stroke_width]:
            if dx != 0 or dy != 0:
                surface.blit(font.render(text, True, stroke_color), text_rect.move(dx, dy))

    main_text_surface = font.render(text, True, text_color)
    surface.blit(main_text_surface, text_rect)

def draw_piece_box(surface, piece_image, label, x, y, is_selected, is_hovered):
    box_color = HIGHLIGHT_COLOR if is_selected else (HOVER_GREEN if is_hovered else GRAY)
    box_rect = pygame.Rect(x - 60, y - 60, 120, 160)

    pygame.draw.rect(surface, box_color, box_rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, box_rect, width=3, border_radius=10)

    surface.blit(piece_image, (x - 50, y - 50))

    label_box_rect = pygame.Rect(x - 50, y + 60, 100, 30)
    pygame.draw.rect(surface, WHITE, label_box_rect, border_radius=5)
    pygame.draw.rect(surface, BLACK, label_box_rect, width=2, border_radius=5)
    draw_text_with_stroke(label, label_font, BLACK, WHITE, surface, x, y + 75)

def draw_button(surface, text, font, rect, button_color, text_color, hover=False, radius=15):
    color = button_color if not hover else (
        min(button_color[0] + 40, 255),
        min(button_color[1] + 40, 255),
        min(button_color[2] + 40, 255)
    )
    pygame.draw.rect(surface, color, rect, border_radius=radius)
    draw_text_with_stroke(text, font, text_color, BLACK, surface, rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)

def choose_piece_screen(player_name):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Checkers Game - Choose Piece Screen")
    running = True
    selected_piece = None

    while running:
        screen.blit(pygame_background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        title_text = f"{player_name}, Choose Your Piece"
        draw_text_with_stroke(title_text, title_font, BLACK, WHITE, screen, SCREEN_WIDTH // 2, 100)

        red_piece_rect = pygame.Rect(240, 240, 120, 160)
        white_piece_rect = pygame.Rect(440, 240, 120, 160)
        red_hovered = red_piece_rect.collidepoint(mouse_pos) and selected_piece != "RED"
        white_hovered = white_piece_rect.collidepoint(mouse_pos) and selected_piece != "WHITE"

        draw_piece_box(screen, red_piece_image, "Red", 300, 300, selected_piece == "RED", red_hovered)
        draw_piece_box(screen, white_piece_image, "White", 500, 300, selected_piece == "WHITE", white_hovered)

        start_button_rect = pygame.Rect(325, 450, 150, 50)
        start_button_hovered = start_button_rect.collidepoint(mouse_pos)
        draw_button(screen, "Start Game", button_font, start_button_rect, RED if selected_piece else GRAY, 
                   WHITE if selected_piece else BLACK, start_button_hovered)

        back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 100, 40)
        back_hover = back_button_rect.collidepoint(mouse_pos)
        draw_button(screen, "Back", button_font, back_button_rect, RED, WHITE, back_hover)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if red_piece_rect.collidepoint(event.pos):
                    selected_piece = "RED"
                elif white_piece_rect.collidepoint(event.pos):
                    selected_piece = "WHITE"
                elif start_button_rect.collidepoint(event.pos) and selected_piece:
                    return selected_piece
                elif back_button_rect.collidepoint(event.pos):
                    return None

        pygame.display.flip()

if __name__ == "__main__":
    choose_piece_screen("Player")
    pygame.quit()
