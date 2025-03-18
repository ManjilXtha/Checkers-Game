import pygame

class Leaderboard:
    def __init__(self, game):
        self.game = game
        self.WIDTH, self.HEIGHT = 900, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.title_font = pygame.font.Font(None, 80)
        self.column_font = pygame.font.Font(None, 40)
        self.running = True
        
        # Define columns and data structure
        self.columns = ["Username", "Game Mode", "Score", "Piece Color", "Win/Lose"]
        self.data = [
            ["bipul", "PvAI", 1, "Red", "Win"],
            ["sworup", "PvP", 6, "White", "Lose"],
            ["manjil", "PvAI", 5, "Red", "Win"],
            ["bishwas", "PvP", 9, "White", "Lose"],
            ["test", "PvAI", 8, "Red", "Win"],
        ]
        
        # Load background
        try:
            self.background_image = pygame.image.load("resources/ch2.jpg")
            self.background_image = pygame.transform.scale(self.background_image, (self.WIDTH, self.HEIGHT))
        except FileNotFoundError:
            self.background_image = None
            
    def draw_text_with_stroke(self, text, font, x, y, text_color, stroke_color, stroke_width, bold=False, italic=False):
        font.set_bold(bold)
        font.set_italic(italic)
        base_text = font.render(text, True, text_color)
        stroke_text = font.render(text, True, stroke_color)
        
        for dx, dy in [(-stroke_width, 0), (stroke_width, 0), (0, -stroke_width), (0, stroke_width)]:
            self.screen.blit(stroke_text, (x + dx, y + dy))
        self.screen.blit(base_text, (x, y))
            
    def draw_table(self):
        table_width = 900
        table_height = 360
        column_spacing = table_width // len(self.columns)
        row_spacing = table_height // (len(self.data) + 1)
        start_x = (self.WIDTH - table_width) // 2
        start_y = 150

        # Draw table background and border
        pygame.draw.rect(self.screen, (0, 0, 0), (start_x, start_y, table_width, table_height))
        pygame.draw.rect(self.screen, (255, 0, 0), (start_x, start_y, table_width, table_height), 3)

        # Draw grid lines
        for col in range(len(self.columns) + 1):
            pygame.draw.line(
                self.screen, (255, 0, 0),
                (start_x + col * column_spacing, start_y),
                (start_x + col * column_spacing, start_y + table_height),
                3
            )

        for row in range(len(self.data) + 2):
            pygame.draw.line(
                self.screen, (255, 0, 0),
                (start_x, start_y + row * row_spacing),
                (start_x + table_width, start_y + row * row_spacing),
                3
            )

        return start_x, start_y, column_spacing, row_spacing
            
    def display_leaderboard(self):
        self.running = True
        clock = pygame.time.Clock()
        
        while self.running:
            self.game.check_events()
            
            if self.game.BACK_KEY:
                self.running = False
                self.game.curr_menu.run_display = True
                return
                
            # Draw background
            if self.background_image:
                self.screen.blit(self.background_image, (0, 0))
            else:
                self.screen.fill((255, 255, 255))
                
            # Draw title
            title_text = "LEADERBOARD"
            self.draw_text_with_stroke(
                title_text, self.title_font,
                self.WIDTH // 2 - 250, 50,
                (0, 0, 0), (255, 0, 0), 2,
                bold=True, italic=True
            )
            
            # Draw table structure and get positions
            start_x, start_y, column_spacing, row_spacing = self.draw_table()
            
            # Draw column headers
            for i, col_name in enumerate(self.columns):
                col_text = self.column_font.render(col_name, True, (255, 255, 255))
                self.screen.blit(col_text, (start_x + i * column_spacing + 10, start_y + 10))
            
            # Draw data rows
            for row_idx, row in enumerate(self.data):
                for col_idx, item in enumerate(row):
                    item_text = self.column_font.render(str(item), True, (255, 255, 255))
                    self.screen.blit(item_text, (start_x + col_idx * column_spacing + 10, 
                                               start_y + (row_idx + 1) * row_spacing + 10))
            
            # Draw back button
            def back_action():
                self.running = False
                self.game.curr_menu.run_display = True
            
            self.game.draw_back_button(
                20, 20, 120, 50,
                (0, 0, 0), (51, 51, 51),
                "Back", back_action
            )
            
            pygame.display.flip()
            clock.tick(60)
