import pygame
from checkers.constant import RED, WHITE, BLUE, SQUARE_SIZE,WIDTH,HEIGHT, DOUBLE_JUMP_SOUND, CAPTURE_SOUND, MOVE_SOUND, KING_SOUND,BOARD_HEIGHT,BOARD_WIDTH,SERRIA,ROPE
from checkers.board import Board
from checkers.piece import Piece
import pygame.mixer

class PVP:
    def __init__(self, win,player1_name, player2_name):
        self._init()
        self.win = win
        self.move_sound = pygame.mixer.Sound("resources/move-self.mp3")
        self.player1_name = player1_name  # Store Player 1 name
        self.player2_name = player2_name  # Load the sound
        # pygame.display.set_caption('Checkers')
        # self.run=True
        # self.pause=False

    def update(self):
        self.board.draw(self.win,self.player1_name,self.player2_name)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self,win):
        if self.board.winner()==WHITE:
            # self.display_winning_screen(win, "Player 1 (White) Wins!")
            self.player_vs_player_win_screen(win,"resources/player1_background.png","Player 1","Player 2")
            return WHITE
        elif self.board.winner()==RED:
            # self.display_winning_screen(win, "Player 2 (Red) Wins!")
            self.player_vs_player_win_screen(win,"resources/player2_background.png","Player 2","Player 1")
            return RED
        return None
    

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
            
        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            skipped = self.valid_moves[(row, col)]
            is_promotion = self.board.is_promotion(self.selected, row)

            # Prioritize the king promotion sound
            if is_promotion:
                KING_SOUND.play()
            elif skipped:
                if len(skipped) > 1:
                    DOUBLE_JUMP_SOUND.play()  # Double jump
                else:
                    CAPTURE_SOUND.play()  # Single capture
            else:
                MOVE_SOUND.play()  # Regular move

            # Move the selected piece
            self.board.move(self.selected, row, col)

            # Handle captures
            if skipped:
                self.board.remove(skipped)

            # Promote the piece if needed
            if is_promotion:
                self.board.promote_to_king(self.selected)

            self.change_turn()
            return True
        return False

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED
    
    # def pause_screen(self,win):
    #     overlay = pygame.Surface((WIDTH, HEIGHT))
    #     overlay.set_alpha(90)  # Transparency level
    #     overlay.fill((0, 0, 0))  # Black overlay
    #     win.blit(overlay, (0, 0))

    # # Draw play button
    #     button_size = 100
    #     playBtn = pygame.Rect(
    #         (WIDTH // 2 - button_size // 2, HEIGHT // 2 - button_size // 2),
    #         (button_size, button_size),
    #     )
    #     pygame.draw.rect(win, (50, 200, 50), playBtn)

    # # Draw play icon
    #     play_icon = pygame.image.load("resources/play.png")
    #     play_icon = pygame.transform.scale(play_icon, (80, 80))
    #     win.blit(play_icon, (WIDTH // 2 - 40, HEIGHT // 2 - 40))

    #     pygame.display.update()
    #     return playBtn
    
    def home_confirmation_screen(self,win):
        popup_width, popup_height = 400, 200
        popup_x = (WIDTH - popup_width) // 2
        popup_y = (HEIGHT - popup_height) // 2

         # Draw the popup background
        pygame.draw.rect(win, SERRIA, (popup_x, popup_y, popup_width, popup_height), border_radius=10)  # Dark gray box
        pygame.draw.rect(win, ROPE, (popup_x, popup_y, popup_width, popup_height), 5, border_radius=10)  # Border

        # Draw confirmation message
        font = pygame.font.Font('resources/Aller_Rg.ttf', 30)
        text = font.render("Return to Home Screen?", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, popup_y+ 50))
        win.blit(text, text_rect)
        mouse_pos=pygame.mouse.get_pos()
        # "Yes" button
        yes_btn = pygame.Rect(WIDTH // 2 - 100, popup_y + 120, 100, 40)
        yes_color = (200, 50, 50) if yes_btn.collidepoint(mouse_pos) else ROPE
        pygame.draw.rect(win, yes_color, yes_btn,border_radius=5)  # Green color
        yes_text = font.render("Yes", True, (255, 255, 255))
        win.blit(yes_text, yes_btn.move(25, 3))

        # "No" button
        no_btn = pygame.Rect(WIDTH // 2 + 20, popup_y + 120, 100, 40)
        no_color = (50, 200, 50) if no_btn.collidepoint(mouse_pos) else ROPE
        pygame.draw.rect(win, no_color, no_btn,border_radius=5)  # Red color
        no_text = font.render("No", True, (255,255,255))
        win.blit(no_text, no_btn.move(30, 3))

        pygame.display.update()
        return yes_btn, no_btn
    
    def draw_button(self,screen, text, rect, base_color, hover_color, font):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        button_color = hover_color if rect.collidepoint(mouse_pos) else base_color

        pygame.draw.rect(screen, button_color, rect, border_radius=10)
        button_text = font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, text_rect)

    def draw_text_with_stroke(self,surface, text, font, text_color, stroke_color, x, y):
        """
        Draws text with a stroke (outline).
        """
        text_surface = font.render(text, True, stroke_color)
        for offset_x, offset_y in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            surface.blit(text_surface, (x + offset_x, y + offset_y))
        text_surface = font.render(text, True, text_color)
        surface.blit(text_surface, (x, y))

    def player_vs_player_win_screen(self,screen, winner_image_path,winner,loser):
        """
        Displays the Player vs Player win screen with dynamic changes based on the winner.
        """
        large_font = pygame.font.Font(None, 120)  # Larger font for winner text
        small_font = pygame.font.Font(None, 40)   # Smaller font for loser text
        button_font = pygame.font.Font(None, 48)
        clock = pygame.time.Clock()

        # Load custom background images
        try:
            winner_image = pygame.image.load(winner_image_path)
            winner_image = pygame.transform.scale(winner_image, (1000, 720))
        except Exception as e:
            print(f"Error loading winner image: {e}")
            winner_image = None

        def rematch():
            self.reset()  # Replace with rematch logic

        def go_home():
            print("Returning to Home Screen!")  # Replace with home screen logic

        running = True
        while running:
        #     # Toggle background and text based on the winner
        #     if player1_wins:
        #         winner = "Player 1"
        #         loser = "Player 2"
            background_image = winner_image
        #     else:
        #         winner = "Player 2"
        #         loser = "Player 1"
        #         background_image = loser_image

            # Draw dimmed background
            screen.fill((0, 0, 0))  # Default black background
            if background_image:
                screen.blit(background_image, (0, 0))
                overlay = pygame.Surface((1000, 720), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 150))  # 150 is the alpha for dimming (0-255 scale)
                screen.blit(overlay, (0, 0))

            # Winning player text
            self.draw_text_with_stroke(
                screen,
                f"{winner} Wins!",
                large_font,
                (255, 255, 255),  # White text
                (0, 255, 0),  # Green stroke
                screen.get_width()//2 - large_font.size(f"{winner} Wins!")[0] // 2,
                200
            )

            # Losing player motivational text
            self.draw_text_with_stroke(
                screen,
                f"{loser} needs to git gud!",
                small_font,
                (255, 255, 255),  # White text
                (255, 0, 0),  # Red stroke
                screen.get_width()//2 - small_font.size(f"{loser} needs to git gud!")[0] // 2,
                550
            )

            # Button positions
            rematch_button_rect = pygame.Rect(50, 600, 150, 50)  # Left-aligned
            home_button_rect = pygame.Rect(800, 600, 150, 50)    # Right-aligned

            # Handle events
            event_list = pygame.event.get()
            self.draw_button(screen, "Rematch", rematch_button_rect, (50, 150, 50), (100, 200, 100), button_font)
            self.draw_button(screen, "Home", home_button_rect, (150, 50, 50), (200, 100, 100), button_font)

            pygame.display.flip()
            # clock.tick(30)
            pos=pygame.mouse.get_pos()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if rematch_button_rect.collidepoint(pos):
                        rematch()  # Reset the game board
                        return 
                    elif home_button_rect.collidepoint(pos):
                        running=False #return home function halne
    
    def run_PVP(self):
        pygame.init()
        pygame.mixer.init()
        clock = pygame.time.Clock()
        FPS = 60

        pause = False
        confirm = False

        def get_row_col_from_mouse(pos):
            x, y = pos
            if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_WIDTH:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                return row, col
            return None

        run = True
        while run:
            clock.tick(FPS)
            if self.winner(self.win) != None:
                self.winner(self.win)
                #run = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True

                if not pause and not confirm:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        retry_rect = pygame.Rect(BOARD_WIDTH + (WIDTH - BOARD_WIDTH) // 2 - 25,
                                              HEIGHT // 2 - 30, 
                                              55, 55)
                    
                        pause_rect = pygame.Rect(BOARD_WIDTH + (WIDTH - BOARD_WIDTH) // 2 - 25,
                                             HEIGHT // 2 - 90,
                                             55, 55)
                        # Home Button
                        home_rect = pygame.Rect(
                            BOARD_WIDTH + (WIDTH - BOARD_WIDTH) // 2 - 25,
                            HEIGHT // 2 +30,
                            55,
                            55,
                        )
                        if retry_rect.collidepoint(pos):  
                            self.reset()
                        if pause_rect.collidepoint(pos):
                            self.board.pause_screen(self.win)
                            pause=True
                        if home_rect.collidepoint(pos):
                            self.home_confirmation_screen(self.win)
                            confirm=True
                        else:
                            result = get_row_col_from_mouse(pos)
                            if result:
                                row, col = result
                                self.select(row, col)

                elif confirm:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        yes_btn, no_btn = self.home_confirmation_screen(self.win)
                        if yes_btn.collidepoint(pos):
                            return True # return False to exit the game loop
                        elif no_btn.collidepoint(pos):
                            confirm = False  # Resume game

                elif pause:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        play_btn = self.board.pause_screen(self.win)
                        if play_btn.collidepoint(pos):
                            pause = False

            if not pause and not confirm:
                self.update()
            elif confirm:
                self.home_confirmation_screen(self.win)
            else:
                self.board.pause_screen(self.win)
        return False

    