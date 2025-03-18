class CHECKERS(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 15
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 48
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 82
        self.exitx, self.exity = self.mid_w, self.mid_h + 117
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        
        # Add game mode selection state
        self.in_game_mode_selection = False
        self.pvp_x, self.pvp_y = self.mid_w, self.mid_h + 15
        self.pvc_x, self.pvc_y = self.mid_w, self.mid_h + 48
        self.back_x, self.back_y = self.mid_w, self.mid_h + 82
        self.game_mode_state = "PVP"

    def display_menu(self):
        if not self.in_game_mode_selection:
            # Your existing menu display code here
            # ... (keep the existing display_menu code)
        else:
            self.display_game_mode_selection()

    def display_game_mode_selection(self):
        menu_image = pygame.image.load('ch2.jpg')
        menu_image = pygame.transform.scale(menu_image, (self.game.DISPLAY_W, self.game.DISPLAY_H))
        
        while self.run_display:
            self.game.check_events()
            self.check_game_mode_input()
            self.game.display.blit(menu_image, (0, 0))
            
            # Draw game mode selection menu
            self.game.draw_text('SELECT GAME MODE', 40, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 20)
            
            # PVP Button
            pvp_rect = pygame.Rect(self.pvp_x - 80, self.pvp_y - 15, 160, 30)
            pygame.draw.rect(self.game.display, 'black', pvp_rect)
            pygame.draw.rect(self.game.display, 'white', pvp_rect, 2)
            self.game.draw_text("Player vs Player", 10, self.pvp_x, self.pvp_y)
            
            # PVC Button
            pvc_rect = pygame.Rect(self.pvc_x - 80, self.pvc_y - 15, 160, 30)
            pygame.draw.rect(self.game.display, 'black', pvc_rect)
            pygame.draw.rect(self.game.display, 'white', pvc_rect, 2)
            self.game.draw_text("Player vs Computer", 10, self.pvc_x, self.pvc_y)
            
            # Back Button
            back_rect = pygame.Rect(self.back_x - 40, self.back_y - 15, 80, 30)
            pygame.draw.rect(self.game.display, 'black', back_rect)
            pygame.draw.rect(self.game.display, 'white', back_rect, 2)
            self.game.draw_text("Back", 10, self.back_x, self.back_y)
            
            self.draw_cursor()
            self.blit_screen()

    def check_game_mode_input(self):
        if self.game.BACK_KEY:
            self.in_game_mode_selection = False
            self.run_display = False
            return
            
        if self.game.DOWN_KEY:
            if self.game_mode_state == "PVP":
                self.game_mode_state = "PVC"
                self.cursor_rect.midtop = (self.pvc_x + self.offset, self.pvc_y)
            elif self.game_mode_state == "PVC":
                self.game_mode_state = "BACK"
                self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)
            elif self.game_mode_state == "BACK":
                self.game_mode_state = "PVP"
                self.cursor_rect.midtop = (self.pvp_x + self.offset, self.pvp_y)
                
        elif self.game.UP_KEY:
            if self.game_mode_state == "PVP":
                self.game_mode_state = "BACK"
                self.cursor_rect.midtop = (self.back_x + self.offset, self.back_y)
            elif self.game_mode_state == "PVC":
                self.game_mode_state = "PVP"
                self.cursor_rect.midtop = (self.pvp_x + self.offset, self.pvp_y)
            elif self.game_mode_state == "BACK":
                self.game_mode_state = "PVC"
                self.cursor_rect.midtop = (self.pvc_x + self.offset, self.pvc_y)
                
        if self.game.START_KEY:
            if self.game_mode_state == "PVP":
                self.game.playing = True
                self.game.game_mode = "PVP"
            elif self.game_mode_state == "PVC":
                self.game.playing = True
                self.game.game_mode = "PVC"
            elif self.game_mode_state == "BACK":
                self.in_game_mode_selection = False
            self.run_display = False

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.in_game_mode_selection = True
                self.game_mode_state = "PVP"
                self.cursor_rect.midtop = (self.pvp_x + self.offset, self.pvp_y)
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
            elif self.state == 'Exit':
                self.game.running, self.game.playing = False, False
            self.run_display = False
