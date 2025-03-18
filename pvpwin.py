import pygame

def draw_button(screen, text, rect, base_color, hover_color, font, callback, event_list):
    mouse_pos = pygame.mouse.get_pos()
    button_color = hover_color if rect.collidepoint(mouse_pos) else base_color

    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    button_text = font.render(text, True, (255, 255, 255))
    text_rect = button_text.get_rect(center=rect.center)
    screen.blit(button_text, text_rect)

    for event in event_list:
        if event.type == pygame.MOUSEBUTTONDOWN and rect.collidepoint(mouse_pos):
            callback()
            return True
    return False

def draw_text_with_stroke(surface, text, font, text_color, stroke_color, x, y):
    text_surface = font.render(text, True, stroke_color)
    for offset_x, offset_y in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        surface.blit(text_surface, (x + offset_x, y + offset_y))
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, (x, y))

def player_vs_player_win_screen(screen, winner_image_path, winner, loser):
    pygame.init()
    large_font = pygame.font.Font(None, 120)
    small_font = pygame.font.Font(None, 40)
    button_font = pygame.font.Font(None, 48)
    clock = pygame.time.Clock()

    try:
        winner_image = pygame.image.load(winner_image_path)
        winner_image = pygame.transform.scale(winner_image, (900, 600))
    except Exception as e:
        print(f"Error loading winner image: {e}")
        winner_image = None

    def rematch():
        pygame.quit()
        from Front_MENU import game
        g = game.Game()
        g.game_loop()

    def go_home():
        pygame.quit()
        from Front_MENU.game import Game
        g = Game()
        while g.running:
            g.curr_menu.display_menu()

    def back_to_menu():
        pygame.quit()
        from Front_MENU.game import Game
        g = Game()
        while g.running:
            g.curr_menu.display_menu()

    running = True
    while running:
        screen.fill((0, 0, 0))
        if winner_image:
            screen.blit(winner_image, (0, 0))
            overlay = pygame.Surface((900, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

        draw_text_with_stroke(
            screen,
            f"{winner} Wins!",
            large_font,
            (255, 255, 255),
            (0, 255, 0),
            screen.get_width()//2 - large_font.size(f"{winner} Wins!")[0] // 2,
            200
        )

        draw_text_with_stroke(
            screen,
            f"{loser} needs to git gud!",
            small_font,
            (255, 255, 255),
            (255, 0, 0),
            screen.get_width()//2 - small_font.size(f"{loser} needs to git gud!")[0] // 2,
            550
        )

        # Try Again button in center
        try_again_rect = pygame.Rect(screen.get_width()//2 - 100, 400, 200, 60)
        
        # Bottom buttons
        rematch_button_rect = pygame.Rect(50, 500, 150, 50)
        home_button_rect = pygame.Rect(800, 500, 150, 50)
        back_button_rect = pygame.Rect(screen.get_width()//2 - 75, 500, 150, 50)

        event_list = pygame.event.get()
        
        # Draw all buttons
        if draw_button(screen, "Try Again", try_again_rect, (50, 150, 50), (100, 200, 100), button_font, rematch, event_list):
            return
        if draw_button(screen, "Rematch", rematch_button_rect, (50, 150, 50), (100, 200, 100), button_font, rematch, event_list):
            return
        if draw_button(screen, "Home", home_button_rect, (150, 50, 50), (200, 100, 100), button_font, go_home, event_list):
            return
        if draw_button(screen, "Menu", back_button_rect, (255, 0, 0), (200, 0, 0), button_font, back_to_menu, event_list):
            return

        for event in event_list:
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1000, 720))
    pygame.display.set_caption("PvP Win Screen")

    player1_win_image = "resources/player1_background.png"
    player2_win_image = "resources/player2_background.png"

    player_vs_player_win_screen(
        screen,
        winner_image_path=player1_win_image,
        winner="Player 1",
        loser="Player 2",
    )
