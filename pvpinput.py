import pygame
import pygame.gfxdraw
from PIL import Image, ImageFilter
from player_database import PlayerDatabase
from choose_piece import choose_piece_screen  

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Checkers Game - Player vs Player Input")

db = PlayerDatabase()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (70, 130, 180)
RED = (255, 0, 0)
DARK_RED = (200, 0, 0)

# Fonts
title_font = pygame.font.Font("resources/Neometra-Caps-FFP.ttf", 48)  # Title font
label_font = pygame.font.Font("resources/GAMEDAY.ttf", 32)  # Label font
input_font = pygame.font.Font(None, 36)  # Input font

# Load and process background image
background_image = Image.open("resources/ch2.jpg")
blurred_image = background_image.filter(ImageFilter.GaussianBlur(10))
blurred_image = blurred_image.resize((SCREEN_WIDTH, SCREEN_HEIGHT))
blurred_surface = pygame.image.fromstring(blurred_image.tobytes(), blurred_image.size, blurred_image.mode)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_text_with_stroke(text, font, text_color, stroke_color, surface, x, y, stroke_width=2):
    text_surface = font.render(text, True, stroke_color)
    text_rect = text_surface.get_rect(center=(x, y))

    for dx in [-stroke_width, 0, stroke_width]:
        for dy in [-stroke_width, 0, stroke_width]:
            if dx != 0 or dy != 0:
                surface.blit(font.render(text, True, stroke_color), text_rect.move(dx, dy))

    main_text_surface = font.render(text, True, text_color)
    surface.blit(main_text_surface, text_rect)

def draw_rounded_rect(surface, color, rect, radius=15):
    pygame.draw.rect(surface, color, rect, border_radius=radius)

def text_input_box(surface, x, y, width, height, active, text, placeholder="Enter name"):
    color = BLUE if active else GRAY
    draw_rounded_rect(surface, WHITE, (x, y, width, height), radius=10)
    pygame.draw.rect(surface, color, (x, y, width, height), 2, border_radius=10)
    display_text = text if text else placeholder
    placeholder_color = GRAY if not text else BLACK
    draw_text(display_text, input_font, placeholder_color, surface, x + width // 2, y + height // 2)

def draw_button(surface, text, font, rect, button_color, text_color, hover=False, radius=15):
    color = button_color if not hover else (
        min(button_color[0] + 40, 255),
        min(button_color[1] + 40, 255),
        min(button_color[2] + 40, 255)
    )
    draw_rounded_rect(surface, color, rect, radius=radius)
    draw_text(text, font, text_color, surface, rect[0] + rect[2] // 2, rect[1] + rect[3] // 2)

def pvp_input_screen():
    input_active_p1 = False
    input_active_p2 = False
    input_text_p1 = ""
    input_text_p2 = ""
    running = True

    while running:
        screen.blit(blurred_surface, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if 250 <= event.pos[0] <= 550 and 200 <= event.pos[1] <= 240:
                    input_active_p1 = True
                    input_active_p2 = False
                elif 250 <= event.pos[0] <= 550 and 300 <= event.pos[1] <= 340:
                    input_active_p1 = False
                    input_active_p2 = True
                else:
                    input_active_p1 = False
                    input_active_p2 = False 
                    back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 100, 40)
                    if back_button_rect.collidepoint(event.pos):
                        return "back"

            if event.type == pygame.KEYDOWN:
                if input_active_p1:
                    if event.key == pygame.K_BACKSPACE:
                        input_text_p1 = input_text_p1[:-1]
                    else:
                        input_text_p1 += event.unicode
                elif input_active_p2:
                    if event.key == pygame.K_BACKSPACE:
                        input_text_p2 = input_text_p2[:-1]
                    else:
                        input_text_p2 += event.unicode

        draw_text_with_stroke("Player vs Player Input", title_font, BLACK, WHITE, screen, SCREEN_WIDTH // 2, 70)
        draw_text_with_stroke("Player 1:  ", label_font, WHITE, BLACK, screen, 180, 220)
        text_input_box(screen, 250, 200, 300, 40, input_active_p1, input_text_p1)
        draw_text_with_stroke("Player 2:  ", label_font, RED, BLACK, screen, 180, 320)
        text_input_box(screen, 250, 300, 300, 40, input_active_p2, input_text_p2)

        start_enabled = input_text_p1.strip() != "" and input_text_p2.strip() != ""
        button_color = RED if start_enabled else GRAY
        hover = start_enabled and 325 <= mouse_pos[0] <= 475 and 450 <= mouse_pos[1] <= 500

        back_button_rect = pygame.Rect(20, SCREEN_HEIGHT - 60, 100, 40)
        back_hover = back_button_rect.collidepoint(mouse_pos)
        draw_button(screen, "Back", input_font, back_button_rect, RED, WHITE, back_hover)

        draw_button(screen, "Next", input_font, (325, 450, 150, 50), button_color, WHITE if start_enabled else BLACK, hover)
        if hover and pygame.mouse.get_pressed()[0] and start_enabled:
            p1_piece_color = "WHITE"
            p2_piece_color = "RED"
            match_id = db.add_pvp_match(input_text_p1, input_text_p2, p1_piece_color, p2_piece_color)
            print(f"PvP match saved with ID: {match_id}")
            print(f"Starting game with Player 1: {input_text_p1} ({p1_piece_color}), Player 2: {input_text_p2} ({p2_piece_color})")
            # Instead of just setting running to False, return the player information
            return {
                "player1": input_text_p1,
                "player2": input_text_p2,
                "match_id": match_id,
                "p1_color": p1_piece_color,
                "p2_color": p2_piece_color
            }

        pygame.display.flip()



# if __name__ == "__main__":
#     pvp_input_screen()
#     pygame.quit()
