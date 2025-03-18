import pygame,random
from checkers.constant import RED, WHITE, YELLOW, SQUARE_SIZE,WIDTH,HEIGHT,DOUBLE_JUMP_SOUND, CAPTURE_SOUND, MOVE_SOUND, KING_SOUND,ROPE,SERRIA,BOARD_HEIGHT,BOARD_WIDTH
from checkers.board import Board
from minimax.algorithm1 import minimax
import pygame.mixer
class PVRed:
    def __init__(self, win,player_name):
        self._init()
        self.win = win
        self.player_name=player_name
        self.move_sound=pygame.mixer.Sound("resources/move-self.mp3")
    
    def update(self):
        self.board.draw_ai(self.win,self.player_name)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def winner(self,win):
        if self.board.winner()==RED:
            pygame.time.delay(500)
            self.you_win_overlay(self.win)
        elif self.board.winner()==WHITE:
            pygame.time.delay(500)
            self.you_lose_overlay(self.win)
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
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            is_promotion=self.board.is_promotion(self.selected,row)
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
            pygame.draw.circle(self.win, YELLOW , (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board
    
    def ai_move(self, board):
        self.board = board
        MOVE_SOUND.play()
        self.change_turn()
    
    def pause_screen(self,win):
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(90)  # Transparency level
        overlay.fill((0, 0, 0))  # Black overlay
        win.blit(overlay, (0, 0))

        button_size = 100
        playBtn = pygame.Rect(
            (WIDTH // 2 - button_size // 2, HEIGHT // 2 - button_size // 2),
            (button_size, button_size),
        )
        pygame.draw.rect(win, (50, 200, 50), playBtn,border_radius=10)

        play_icon = pygame.image.load("resources/play.png")
        play_icon = pygame.transform.scale(play_icon, (80, 80))
        win.blit(play_icon, (WIDTH // 2 - 40, HEIGHT // 2 - 40))
        pygame.display.update()
        return playBtn
    
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
        """Draws a button with hover effect and handles click events."""
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()
        button_color = hover_color if rect.collidepoint(mouse_pos) else base_color

        pygame.draw.rect(screen, button_color, rect, border_radius=10)
        button_text = font.render(text, True, (255, 255, 255))
        text_rect = button_text.get_rect(center=rect.center)
        screen.blit(button_text, text_rect)
    
    def draw_text_with_stroke(self,text, font, text_color, stroke_color, surface, x, y, stroke_width=2):
        """Draws text with a stroke (outline) effect."""
        text_surface = font.render(text, True, stroke_color)
        text_rect = text_surface.get_rect(center=(x, y))

        # Draw stroke by rendering the text in the stroke color around the main text
        for dx in [-stroke_width, 0, stroke_width+1]:
            for dy in [-stroke_width, 0, stroke_width+1]:
                if dx != 0 or dy != 0:  # Avoid rendering at the center
                    surface.blit(font.render(text, True, stroke_color), text_rect.move(dx, dy))

        # Draw the main text
        main_text_surface = font.render(text, True, text_color)
        surface.blit(main_text_surface, text_rect)

    def draw_confetti(self,screen):
        for _ in range(20):
            x = random.randint(0, 1000)
            y = random.randint(0, 720)
            color = random.choice([(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0)])
            pygame.draw.circle(screen, color, (x, y), random.randint(5, 10))


    def you_win_overlay(self,screen):
        font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 48)

        home_button_rect = pygame.Rect(200, 450, 150, 50)
        play_again_button_rect = pygame.Rect(650, 450, 200, 50)

        def go_home():
            print("Go to Home Screen!")  # Replace with home screen logic

        def play_again():
            self.reset()  # Replace with game restart logic
        running=True
        while running:
            screen.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            self.draw_confetti(screen)

            # Render "YOU WIN!" with a green stroke
            self.draw_text_with_stroke(
                "YOU WIN!", font, (255, 255, 255), (0, 255, 0), screen,screen.get_width()//2, 300, stroke_width=3
            )

            event_list = pygame.event.get()
            self.draw_button(screen, "Home", home_button_rect, (100, 100, 200), (150, 150, 250), button_font)
            self.draw_button(screen, "Play Again", play_again_button_rect, (100, 200, 100), (150, 250, 150), button_font)

            pygame.display.flip()
            # clock.tick(60)
            pos=pygame.mouse.get_pos()
            for event in event_list:
                if event.type == pygame.QUIT:
                    running=False
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if home_button_rect.collidepoint(pos):
                        running=False
                    elif play_again_button_rect.collidepoint(pos):
                        self.reset()
                        return
                
    def you_lose_overlay(self,screen):
        font = pygame.font.Font(None, 72)
        button_font = pygame.font.Font(None, 48)
        clock = pygame.time.Clock()
        cracked_glass_image = pygame.image.load("resources/cracked_glass.png")
        cracked_glass_image = pygame.transform.scale(cracked_glass_image, (1000, 720))

        home_button_rect = pygame.Rect(200, 450, 150, 50)
        retry_button_rect = pygame.Rect(650, 450, 150, 50)

        def go_home():
            print("Go to Home Screen!")  # Replace with home screen logic

        def retry_game():
            print("Retrying Game!")  # Replace with game restart logic
        running=True
        while running:  # Animation loop
            screen.fill((0, 0, 0), special_flags=pygame.BLEND_RGBA_MULT)
            screen.blit(cracked_glass_image, (0, 0))

            # Render "YOU LOSE!" with a red stroke
            self.draw_text_with_stroke(
                "YOU LOSE!", font, (255, 255, 255), (255, 0, 0), screen, screen.get_width()//2, 300, stroke_width=3
            )

            event_list = pygame.event.get()

            # Draw the buttons
            self.draw_button(screen, "Home", home_button_rect, (200, 100, 100), (250, 150, 150), button_font)
            self.draw_button(screen, "Retry", retry_button_rect, (100, 100, 200), (150, 150, 250), button_font)

            pygame.display.flip()
            # clock.tick(60)
            pos=pygame.mouse.get_pos()
            # Handle events
            for event in event_list:
                if event.type == pygame.QUIT:
                    running=False
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    if home_button_rect.collidepoint(pos):
                        running=False
                    elif retry_button_rect.collidepoint(pos):
                        self.reset()
                        return

    def run_pvwhite(self):
        pygame.init()
        pygame.mixer.init()
        run = True
        clock = pygame.time.Clock()
        FPS=60
        pause=False
        confirm=False
        def get_row_col_from_mouse(pos):
            x, y = pos
            if 0<=x<BOARD_WIDTH and 0<=y<BOARD_HEIGHT:
                row = y // SQUARE_SIZE
                col = x // SQUARE_SIZE
                return row, col
            return None
        while run:
            clock.tick(FPS)

            if self.turn == WHITE:
                value, new_board = minimax(self.get_board(), 5, WHITE, self,-999,999)
                # print(value)
                self.ai_move(new_board)

            if self.winner(self.win) != None:
                self.winner(self.win)
                

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if not pause and not confirm:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        #retry
                        retry_rect = pygame.Rect(BOARD_WIDTH + (WIDTH - BOARD_WIDTH) // 2 - 25, 
                                                HEIGHT // 2 - 30, 
                                                55, 55)
                        #pause
                        pause_rect = pygame.Rect(BOARD_WIDTH + (WIDTH - BOARD_WIDTH) // 2 - 25,
                                                HEIGHT // 2 - 90,
                                                55,55)
                        #home
                        home_rect = pygame.Rect(
                            BOARD_WIDTH + (WIDTH - BOARD_WIDTH) // 2 - 25,
                            HEIGHT // 2 + 30,
                            55,
                            55,
                        )

                        if retry_rect.collidepoint(pos):  
                            self.reset()
                        if pause_rect.collidepoint(pos):
                            self.pause_screen(self.win)
                            pause=True
                        if home_rect.collidepoint(pos):
                            self.home_confirmation_screen(self.win)
                            confirm=True
                        else:
                            result = get_row_col_from_mouse(pos)
                            if result:
                                row,col=result
                                self.select(row, col)
                elif confirm:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        yes_btn, no_btn = self.home_confirmation_screen(self.win)
                        if yes_btn.collidepoint(pos):
                            run = False  # Exit to home or implement home screen navigation here
                        elif no_btn.collidepoint(pos):
                            confirm = False
                elif pause:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos=pygame.mouse.get_pos()
                        if playBtn.collidepoint(pos):
                            pause=False
            
            if not pause and not confirm:
                self.update()
            elif confirm:
                yes_btn,no_btn=self.home_confirmation_screen(self.win)
            else:
                playBtn=self.pause_screen(self.win)
        

