import pygame
import sys
from menu import CHECKERS, OptionsMenu, CreditsMenu
from tutorial import Tutorial
from pvpinput import pvp_input_screen
from pvaiinput import pvai_input_screen
from checkers.pvp import PVP
from leaderboard import Leaderboard




class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.display.set_caption('Checkers Game')
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 900, 600
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = 'resources/GAMEDAY.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        self.hover_color = (50, 50, 50)
        self.normal_color = (0, 0, 0)
        self.game_mode = None
        self.selecting_mode = False
        self.background_image = self.load_and_scale_background()
        self.tutorial_active = False
        self.current_menu_item = 0
        self.menu_items = ['Start', 'Options', 'Credits', 'Exit', 'Leaderboard']
        self.checkers = CHECKERS(self)
        self.curr_menu = self.checkers
        self.curr_menu.state='Start'
        self.options = OptionsMenu(self)
        self.credits = CreditsMenu(self)
        self.player_data = None
        from leaderboard import Leaderboard
        self.leaderboard = Leaderboard(self)
        try:
            self.font = pygame.font.Font(self.font_name, 20)
        except FileNotFoundError:
            print("Using system font as fallback")
            self.font = pygame.font.Font('arial', 20)

    def load_and_scale_background(self):
        background = pygame.image.load('resources/blurred_bg.png')
        return pygame.transform.scale(background, (self.DISPLAY_W, self.DISPLAY_H))

    def draw_blurred_background(self):
        blurred_background = pygame.transform.scale(self.background_image, (self.DISPLAY_W // 10, self.DISPLAY_H // 10))
        blurred_background = pygame.transform.smoothscale(blurred_background, (self.DISPLAY_W, self.DISPLAY_H))
        self.display.blit(blurred_background, (0, 0))

    def show_tutorial(self):
        tutorials = [
            {
                "text": "Moving pieces: Move diagonally to an empty square.",
                "images": [
                    pygame.transform.scale(pygame.image.load('resources/move1.png'), (400, 400)),
                    pygame.transform.scale(pygame.image.load('resources/move2.png'), (400, 400))
                ]
            },
            {
                "text": "Capturing opponent pieces: Jump over opponent pieces to capture.",
                "images": [
                    pygame.transform.scale(pygame.image.load('resources/capture1.png'), (400, 400)),
                    pygame.transform.scale(pygame.image.load('resources/capture2.png'), (400, 400))
                ]
            },
            {
                "text": "Promoting to a King: Reach the opponent's last row to promote to a King.",
                "images": [
                    pygame.transform.scale(pygame.image.load('resources/king1.png'), (400, 400)),
                    pygame.transform.scale(pygame.image.load('resources/king2.png'), (400, 400))
                ]
            }
        ]
        bg_img = pygame.image.load('resources/ch3.png')
        play_icon = pygame.image.load('resources/joystick.png')
        font = pygame.font.Font('resources/GAMEDAY.TTF', 20)
        tutorial = Tutorial(
            screen=self.window,
            tutorials=tutorials,
            font=font,
            play_icon=play_icon,
            bg_img=bg_img
        )
        running = True
        clock = pygame.time.Clock()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        running = False
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if tutorial.play_button_rect.collidepoint(event.pos):
                        running = False
                        self.playing = True
                        return
                tutorial.handle_event(event)
            tutorial.draw()
            pygame.display.flip()
            clock.tick(30)
    def game_loop(self):
        """
        Handles the game mode selection screen for the Checkers game.
        Ensures that no mode is selected until the player explicitly interacts.
        """
        # Define available game modes
        available_modes = ["pvp", "pvc", "how_to_play"]
        self.curr_menu.run_display = False
        self.playing = True
        
        # Completely remove any pre-selection
        selected_mode = None
        
        # Initialize game clock for consistent frame rate
        clock = pygame.time.Clock()
        # Load and scale mode selection images
        pvp_image = pygame.transform.scale(pygame.image.load('resources/person.png').convert_alpha(), (100, 100))
        pvc_image = pygame.transform.scale(pygame.image.load('resources/computer.png').convert_alpha(), (100, 100))
        
        # Calculate positioning for mode selection rectangles
        border_width, border_height, spacing = 180, 130, 80
        left_x = (self.DISPLAY_W // 2) - (border_width + spacing // 2)
        left_y = (self.DISPLAY_H // 2) - (border_height // 2)
        right_x = (self.DISPLAY_W // 2) + (spacing // 2)
        right_y = left_y
        how_to_play_x = self.DISPLAY_W // 2 - border_width // 2
        how_to_play_y = self.DISPLAY_H - (border_height - 20) + 40
        
        # Define rectangles for each mode
        rects = {
            "pvp": pygame.Rect(left_x, left_y, border_width, border_height),
            "pvc": pygame.Rect(right_x, right_y, border_width, border_height),
            "how_to_play": pygame.Rect(how_to_play_x, how_to_play_y, border_width, border_height // 2)
        }
        
        # Define arrow positioning for each mode
        arrow_positions = {
            "pvp": (left_x, left_y, border_width),
            "pvc": (right_x, right_y, border_width),
            "how_to_play": (how_to_play_x, how_to_play_y, border_width)
        }
        
        # Main game mode selection loop
        while self.playing:
            # Maintain consistent frame rate
            clock.tick(60)
            
            # Get current mouse position
            mouse_pos = pygame.mouse.get_pos()
            
            # Check for keyboard and system events
            self.check_events() 
            self.window.fill((0, 0, 0))  # Clear screen each frame
            
            
            # Draw background
            self.display.blit(self.background_image, (0, 0))
            
            # Draw title
            self.draw_text_with_stroke(
                'SELECT GAME MODE', 
                int(30 * 1.5), 
                self.DISPLAY_W // 2, 
                50, 
                color=(255, 0, 0), 
                stroke_color=(0, 0, 0)
            )
            
            
            # Handle mode selection and highlighting
            for mode, rect in rects.items():
                
                

                # Default to normal color unless specifiCcally selected
                color = self.normal_color
                
                # Highlight when mouse is over the rectangle
                if rect.collidepoint(mouse_pos):
                    color = self.hover_color
                

                    # Only select mode on mouse click
                    if pygame.mouse.get_pressed()[0]:

                        selected_mode = mode
                        # Mode-specific actions on mouse click
                        if selected_mode == "pvc": 
                            current_volume = self.curr_menu.volume if hasattr(self.curr_menu, 'volume') else 0
                            
                            if hasattr(self.curr_menu, 'background_music'):
                                self.curr_menu.stop_music() 
                            player=pvai_input_screen()
                            player_name=player["player_name"]
                            if player_name =="back":
                                if hasattr(self.curr_menu, 'background_music'):
                                    self.curr_menu.background_music.play(loops=-1)
                                    self.curr_menu.background_music.set_volume(current_volume)
                                self.curr_menu.run_display = True  
                                return
                            selected_game =self.select_yer_color()
                            # print("PVC mode selected",selected_game)
                            if selected_game is None:
                                continue
                            if selected_game == "red":
                                print("PVC mode selected",selected_game)
                                pygame.init()
                                pygame.mixer.stop()
                                pygame.mixer.music.stop()
                                WIN = pygame.display.set_mode((900, 600))
                                pygame.display.set_caption('Checkers')
                                from checkers.RedAi import PVRed
                                game=PVRed(WIN,player_name)
                                game.run_pvwhite()
                                self.playing = False
                                return player_name
                            elif selected_game == "white":
                                print("PVC mode selected",selected_game)
                                pygame.init()
                                pygame.mixer.stop()
                                pygame.mixer.music.stop()
                                WIN = pygame.display.set_mode((900, 600))
                                pygame.display.set_caption('Checkers')
                                # pygame.font.Font('resources/GAMEDAY.ttf')
                                from checkers.WhiteAi import PVWhite
                                game = PVWhite(WIN,player_name)
                                game.run_pvred()
                                self.playing = False
                                return player_name
                        
                        elif selected_mode == "how_to_play":
                            self.show_tutorial()
                        
                        elif selected_mode == "pvp":
                            # Existing PvP game launch code
                            current_volume = self.curr_menu.volume if hasattr(self.curr_menu, 'volume') else 0
                            
                            if hasattr(self.curr_menu, 'background_music'):
                                self.curr_menu.stop_music()
                            
                            player_info = pvp_input_screen() 

                            if player_info =="back":
                                if hasattr(self.curr_menu, 'background_music'):
                                    self.curr_menu.background_music.play(loops=-1)
                                    self.curr_menu.background_music.set_volume(current_volume)
                                self.curr_menu.run_display = True  
                                return
                                
                              
                            elif player_info:
                                print(f"Starting PvP game with: {player_info}")
                                self.player_data = player_info
                                pygame.init()
                                pygame.mixer.stop()
                                pygame.mixer.music.stop()
                                WIN = pygame.display.set_mode((900, 600))
                                pygame.display.set_caption('Checkers')
                                player1_name = player_info.get("player1", "Player 1")  
                                player2_name = player_info.get("player2", "Player 2")
                                from checkers.pvp import PVP
                                game = PVP(WIN,player1_name, player2_name)
                                returned_to_menu = game.run_PVP()
                                
                                if returned_to_menu:
                                    if hasattr(self.curr_menu, 'background_music'):
                                        self.curr_menu.background_music.play(loops=-1)
                                        self.curr_menu.background_music.set_volume(current_volume)
                                    self.playing = False
                                    self.curr_menu.run_display = True
                                    self.curr_menu.state = 'Start'
                                    self.curr_menu = self.checkers
                                    return None
                                
                                self.playing = False
                                return player_info
                    
                # Draw the rectangle with current color
                pygame.draw.rect(self.display, color, rect, border_radius=15)
                pygame.draw.rect(self.display, self.WHITE, rect, 3, border_radius=15)
            
            # Draw mode icons and labels
            self.display.blit(pvp_image, (left_x + (border_width - 100) // 2, left_y + 10))
            self.display.blit(pvc_image, (right_x + (border_width - 100) // 2, right_y + 10))
            
            self.draw_text('Player vs Player', 10, left_x + border_width//2, left_y + border_height - 20)
            self.draw_text('Player vs Computer', 10, right_x + border_width//2, right_y + border_height - 20)
            self.draw_text('How to Play?', 20, how_to_play_x + border_width//2 - 1, how_to_play_y + border_height//4)
            
            # Back button
            back_button_x, back_button_y = 20, 20
            back_button_width, back_button_height = 120, 50
            
            def back_action():
                self.playing = False
                self.curr_menu = self.checkers
                self.curr_menu.run_display = True
                self.curr_menu.state = 'Start'
                pygame.display.flip()
            
            self.draw_back_button(
                back_button_x, back_button_y,
                back_button_width, back_button_height,
                self.BLACK, (51, 51, 51),
                "Back", back_action
            )
            
            # Update screen and reset key states
            self.blit_screen()
            self.reset_keys()

            # Return to previous menu if back is pressed
            if self.BACK_KEY:
                self.playing = False
                self.curr_menu.run_display = True
                return

   
    

    def draw_text_with_stroke(self, text, size, x, y, color=(255, 255, 255), stroke_color=(0, 0, 0), font_name=None):
        font_name = font_name if font_name else self.font_name
        font = pygame.font.Font(font_name, size)
        font.set_italic(True)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (-2, 2), (2, -2), (2, 2)]:
            stroke_surface = font.render(text, True, stroke_color)
            self.display.blit(stroke_surface, text_rect.move(dx, dy))
        self.display.blit(text_surface, text_rect)

    def draw_back_button(self, x, y, width, height, color, hover_color, text, action=None):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        button_rect = pygame.Rect(x, y, width, height)
        current_color = hover_color if button_rect.collidepoint(mouse_pos) else color
        pygame.draw.rect(self.display, current_color, button_rect, border_radius=15)
        pygame.draw.rect(self.display, self.BLACK, button_rect, width=2, border_radius=15)
        self.draw_text(text, 20, button_rect.centerx, button_rect.centery, color=self.WHITE)
        if button_rect.collidepoint(mouse_pos) and mouse_click and action:
            action()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.show_exit_confirmation():
                    pygame.quit()
                    sys.exit()
                else:
                    self.curr_menu.run_display = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                elif event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                elif event.key == pygame.K_UP:
                    self.UP_KEY = True
                elif event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                elif event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY, self.LEFT_KEY, self.RIGHT_KEY = False, False, False, False, False, False
    
    def select_yer_color(self):
        clock = pygame.time.Clock()
        modes = ["white", "red"]
        current_mode_index = 0
        selected_color = modes[current_mode_index] 
        hover_color = (50, 50, 50)
        # Load and scale color selection images
        white_piece_image = pygame.transform.scale(pygame.image.load('resources/white_piece.png'), (100, 100))
        red_piece_image = pygame.transform.scale(pygame.image.load('resources/red_piece.png'), (100, 100))
        
        # Define rectangles and positioning
        border_width, border_height, spacing = 180, 130, 80
        left_x = (self.DISPLAY_W // 2) - (border_width + spacing // 2)
        left_y = (self.DISPLAY_H // 2) - (border_height // 2)
        right_x = (self.DISPLAY_W // 2) + (spacing // 2)
        right_y = left_y
        
        rects = {
            "white": pygame.Rect(left_x, left_y, border_width, border_height),
            "red": pygame.Rect(right_x, right_y, border_width, border_height)
        }
        
        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return selected_color
                    elif event.key == pygame.K_BACKSPACE:
                        return None
                    elif event.key == pygame.K_LEFT:
                        current_mode_index = (current_mode_index - 1) % len(modes)
                        selected_color = modes[current_mode_index]
                    elif event.key == pygame.K_RIGHT:
                        current_mode_index = (current_mode_index + 1) % len(modes)
                        selected_color = modes[current_mode_index]
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Check back button
                    back_button_rect = pygame.Rect(20, 20, 120, 50)
                    if back_button_rect.collidepoint(mouse_pos):
                        return None
                        
                    # Check color selection
                    for color, rect in rects.items():
                        if rect.collidepoint(mouse_pos):
                            return color
            
            # Draw background
            self.display.blit(self.background_image, (0, 0))
            
            # Draw title
            self.draw_text_with_stroke('SELECT PLAYER COLOR', int(30 * 1.5), self.DISPLAY_W // 2, 50, 
                                    color=(255, 0, 0), stroke_color=(0, 0, 0))
            
            # Draw color selection boxes
            for color, rect in rects.items(): 
                if rect.collidepoint(mouse_pos):
                    box_color = hover_color
                else:
                    box_color = self.normal_color  
                    # Draw the box with hover effect
                pygame.draw.rect(self.display, box_color, rect, border_radius=15)
                pygame.draw.rect(self.display, self.WHITE, rect, 3, border_radius=15)     
                # Add glow effect on hover
                if rect.collidepoint(mouse_pos):
                    glow_rect = rect.inflate(10, 10)
                    pygame.draw.rect(self.display, (100, 100, 100), glow_rect, 3, border_radius=20)

            
            # Draw piece images
            self.display.blit(white_piece_image, (left_x + (border_width - 100) // 2, left_y + 10))
            self.display.blit(red_piece_image, (right_x + (border_width - 100) // 2, right_y + 10))
            
            # Draw labels
            self.draw_text('White Pieces', 10, left_x + border_width//2, left_y + border_height - 20)
            self.draw_text('Red Pieces', 10, right_x + border_width//2, right_y + border_height - 20)
            
            # Draw back button
            back_button_rect = pygame.Rect(20, 20, 120, 50)
            back_hover = back_button_rect.collidepoint(mouse_pos)
            back_color = hover_color if back_hover else self.BLACK
        
            self.draw_back_button(20, 20, 120, 50, back_color, hover_color, "Back", lambda: None)
            
            # Update display
            self.blit_screen()
            self.reset_keys()





        

        

    def draw_text(self, text, size, x, y, color=(255, 255, 255), italic=False, font_name=None):
        font_name = font_name if font_name else self.font_name
        font = pygame.font.Font(font_name, size)
        font.set_italic(italic)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        self.display.blit(text_surface, text_rect)

    def blit_screen(self):
        self.window.blit(self.display, (0, 0))
        pygame.display.update()

    def show_exit_confirmation(self):
        clock = pygame.time.Clock()
        dialog_width, dialog_height = 500, 250
        dialog_x = (self.DISPLAY_W - dialog_width) // 2
        dialog_y = (self.DISPLAY_H - dialog_height) // 2
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        button_width, button_height = 140, 50
        yes_button_rect = pygame.Rect(
            dialog_x + 60, dialog_y + dialog_height - 90, button_width, button_height
        )
        no_button_rect = pygame.Rect(
            dialog_x + dialog_width - button_width - 60, dialog_y + dialog_height - 90, button_width, button_height
        )
        wood_color = (210, 180, 140)
        wood_border_color = (139, 69, 19)
        yes_hover_color = (255, 165, 79)
        no_hover_color = (144, 238, 144)
        button_color = (255, 222, 173)
        button_text_color = (0, 0, 0)
        blurred_background = pygame.transform.scale(self.background_image, (self.DISPLAY_W // 10, self.DISPLAY_H // 10))
        blurred_background = pygame.transform.smoothscale(blurred_background, (self.DISPLAY_W, self.DISPLAY_H))
        while True:
            clock.tick(60)
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():    
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if yes_button_rect.collidepoint(mouse_pos):
                        self.curr_menu = self.checkers
                        self.curr_menu.run_display = True
                        self.curr_menu.state = 'Start'
                        return True
                    if no_button_rect.collidepoint(mouse_pos):
                        return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
            self.window.blit(blurred_background, (0, 0))
            pygame.draw.rect(self.window, wood_color, dialog_rect, border_radius=15)
            pygame.draw.rect(self.window, wood_border_color, dialog_rect, 4, border_radius=15)
            yes_color = yes_hover_color if yes_button_rect.collidepoint(mouse_pos) else button_color
            no_color = no_hover_color if no_button_rect.collidepoint(mouse_pos) else button_color
            pygame.draw.rect(self.window, yes_color, yes_button_rect, border_radius=15)
            pygame.draw.rect(self.window, wood_border_color, yes_button_rect, 3, border_radius=15)
            pygame.draw.rect(self.window, no_color, no_button_rect, border_radius=15)
            pygame.draw.rect(self.window, wood_border_color, no_button_rect, 3, border_radius=15)
            font = pygame.font.Font(self.font_name, 25)
            title_text = font.render("Are you sure you want to exit?", True, (0, 0, 0))
            title_rect = title_text.get_rect(center=(self.DISPLAY_W // 2, dialog_y + 60))
            self.window.blit(title_text, title_rect)
            yes_text = font.render("Yes", True, button_text_color)
            no_text = font.render("No", True, button_text_color)
            yes_text_rect = yes_text.get_rect(center=yes_button_rect.center)
            no_text_rect = no_text.get_rect(center=no_button_rect.center)
            self.window.blit(yes_text, yes_text_rect)
            self.window.blit(no_text, no_text_rect)
            pygame.display.update()

if __name__ == '__main__':
    g = Game()
    while g.running:
        g.curr_menu.display_menu()
        if g.curr_menu.state == 'Start':
            player_info = g.game_loop()
            if player_info and isinstance(player_info, dict):
                print("Starting game with players:", player_info)
            else:
                g.curr_menu.display_menu()
