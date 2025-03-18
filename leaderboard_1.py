import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Leaderboard")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Fonts
title_font = pygame.font.Font(None, 80)  # Replace None with "path/to/your/custom_font.ttf"
column_font = pygame.font.Font(None, 40)

# Sample data
columns = ["Username", "Game Mode", "Score", "Piece Color", "Win/Lose"]
data = [
    ["Manjil", "PvP", 1, "Red", "Win"],
    ["Sworup", "PvP", 6, "White", "Lose"],
    ["Bipul", "PvP", 5, "Red", "Win"],
    ["Manjil", "PvP", 9, "White", "Lose"],
    ["Bipul", "PvP", 8, "Red", "Win"],
]

# Load background image (replace 'background.jpg' with your file path)
try:
    background_image = pygame.image.load("background.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
except FileNotFoundError:
    background_image = None

def draw_text_with_stroke(text, font, x, y, text_color, stroke_color, stroke_width, bold=False, italic=False):
    """Renders text with a stroke and optional bold/italic styles."""
    font.set_bold(bold)
    font.set_italic(italic)
    base_text = font.render(text, True, text_color)
    stroke_text = font.render(text, True, stroke_color)
    # Draw the stroke by offsetting
    for dx, dy in [(-stroke_width, 0), (stroke_width, 0), (0, -stroke_width), (0, stroke_width)]:
        screen.blit(stroke_text, (x + dx, y + dy))
    screen.blit(base_text, (x, y))

def draw_table():
    """Draws the table with borders and data."""
    # Table dimensions
    table_width = 900
    table_height = 360
    column_spacing = table_width // len(columns)
    row_spacing = table_height // (len(data) + 1)
    start_x = (WIDTH - table_width) // 2
    start_y = 150

    # Draw table background (black and opaque)
    pygame.draw.rect(screen, BLACK, (start_x, start_y, table_width, table_height))

    # Draw table border (red)
    pygame.draw.rect(screen, RED, (start_x, start_y, table_width, table_height), 3)

    # Draw column lines
    for col in range(len(columns) + 1):
        pygame.draw.line(
            screen, RED, 
            (start_x + col * column_spacing, start_y), 
            (start_x + col * column_spacing, start_y + table_height), 
            3
        )

    # Draw row lines
    for row in range(len(data) + 2):
        pygame.draw.line(
            screen, RED, 
            (start_x, start_y + row * row_spacing), 
            (start_x + table_width, start_y + row * row_spacing), 
            3
        )

    return start_x, start_y, column_spacing, row_spacing

def draw_leaderboard():
    """Draws the leaderboard screen."""
    # Draw background image if available
    if background_image:
        screen.blit(background_image, (0, 0))
    else:
        screen.fill(WHITE)

    # Draw title
    title_text = "LEADERBOARD"
    draw_text_with_stroke(title_text, title_font, WIDTH // 2 - 250, 50, BLACK, RED, 2, bold=True, italic=True)

    # Draw table and data
    start_x, start_y, column_spacing, row_spacing = draw_table()

    # Draw column headers
    for i, col_name in enumerate(columns):
        col_text = column_font.render(col_name, True, WHITE)
        screen.blit(col_text, (start_x + i * column_spacing + 10, start_y + 10))

    # Draw data rows
    for row_idx, row in enumerate(data):
        for col_idx, item in enumerate(row):
            item_text = column_font.render(str(item), True, WHITE)
            screen.blit(item_text, (start_x + col_idx * column_spacing + 10, start_y + (row_idx + 1) * row_spacing + 10))

def main():
    """Main loop."""
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        draw_leaderboard()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()