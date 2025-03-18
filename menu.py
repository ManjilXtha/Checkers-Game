import pygame
import os

class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
        self.hover_color = (50, 50, 50)
        self.normal_color = (0, 0, 0)
        pygame.mixer.init()
        self.volume = 0
        self.background_music = pygame.mixer.Sound('resources/sound.mp3')
        self.background_music.set_volume(0)
        self.background_music.play(loops=-1) 
    def stop_music(self):
        self.background_music.stop()
            
    def start_music(self):
        self.background_music.play(loops=-1)
        self.background_music.set_volume(self.volume)

    def draw_cursor(self):
        offset_x = -20
        self.game.draw_text('>', 25, self.cursor_rect.x + offset_x, self.cursor_rect.y, color=(0, 0, 0))

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
    def reset_state(self):
        self.state = 'Start'
        self.run_display = True
    
class CHECKERS(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = "Start"
        self.startx, self.starty = self.mid_w, self.mid_h + 30
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 90
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 150
        self.exitx, self.exity = self.mid_w, self.mid_h + 210
        self.leaderboardx = self.game.DISPLAY_W - 100
        self.leaderboardy = self.game.DISPLAY_H - 50
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

        self.leaderboard_image = pygame.image.load('resources/leaderboard1.png')
        self.leaderboard_image = pygame.transform.scale(self.leaderboard_image, (40, 40))

        self.buttons = [
            {"text": "Start Game", "x": self.startx, "y": self.starty, "width": 240, "state": 'Start'},
            {"text": "Options", "x": self.optionsx, "y": self.optionsy, "width": 160, "state": 'Options'},
            {"text": "Credits", "x": self.creditsx, "y": self.creditsy, "width": 160, "state": 'Credits'},
            {"text": "Exit", "x": self.exitx, "y": self.exity, "width": 100, "state": 'Exit'},
            {"text": "", "x": self.leaderboardx, "y": self.leaderboardy, "width": 40, "state": 'Leaderboard', "is_image": True}
        ]
        
        self.menu_items = [button["state"] for button in self.buttons]
        self.current_item = 0
        pass

    def display_menu(self):
        menu_image = pygame.image.load('resources/ch3.png')
        menu_image = pygame.transform.scale(menu_image, (self.game.DISPLAY_W, self.game.DISPLAY_H))

        self.run_display = True
        while self.run_display:
            mouse_pos = pygame.mouse.get_pos()
            self.game.check_events()
            self.check_input()

            self.game.display.blit(menu_image, (0, 0))
            self.draw_title()

            if self.game.UP_KEY:
                self.current_item = (self.current_item - 1) % len(self.buttons)
                self.state = self.buttons[self.current_item]["state"]

            if self.game.DOWN_KEY:
                self.current_item = (self.current_item + 1) % len(self.buttons)
                self.state = self.buttons[self.current_item]["state"]

            for i, button in enumerate(self.buttons):
                rect = pygame.Rect(button["x"] - button["width"] / 2, button["y"] - 30, button["width"], 60)

                if rect.collidepoint(mouse_pos):
                    self.current_item = i
                    self.state = self.menu_items[i]

                color = self.hover_color if i == self.current_item else self.normal_color
                if button.get("is_image", False):
                    image_rect = self.leaderboard_image.get_rect(center=(button["x"], button["y"]))
                    self.game.display.blit(self.leaderboard_image, image_rect)
                else:
                    pygame.draw.rect(self.game.display, color, rect, border_radius=15)
                    pygame.draw.rect(self.game.display, (255, 255, 255), rect, 3, border_radius=15)
                    self.game.draw_text(button["text"], 20, button["x"], button["y"])

                if rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
                    self.state = button["state"]
                    self.handle_state_selection()

            current_button = self.buttons[self.current_item]
            self.cursor_rect.midtop = (current_button["x"] + self.offset, current_button["y"])
            self.draw_cursor()
            self.blit_screen()

    def draw_title(self):
        font = pygame.font.Font(None, int(70 * 1.5))
        font.set_bold(True)
        font.set_italic(True)

        text_surface = font.render("CHECKERS", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.game.DISPLAY_W / 2, 50))

        stroke_color = (255, 0, 0)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            outline_surface = font.render("CHECKERS", True, stroke_color)
            outline_rect = outline_surface.get_rect(center=(self.game.DISPLAY_W / 2 + dx, 50 + dy))
            self.game.display.blit(outline_surface, outline_rect)

        self.game.display.blit(text_surface, text_rect)

    def check_input(self):
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options 
                self.run_display = False
                self.game.options.display_menu()
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits 
                self.run_display = False
                self.game.credits.display_menu()
            elif self.state == 'Leaderboard':
                self.game.leaderboard.display_leaderboard()
            elif self.state == 'Exit':
                if self.game.show_exit_confirmation():
                    self.game.running = False

    def handle_state_selection(self):
        if self.state == 'Start':
            self.game.playing = True
            self.run_display = False    
        elif self.state == 'Options':
            self.game.curr_menu = self.game.options
            self.run_display = False
            self.game.options.display_menu()
        elif self.state == 'Credits':
            self.game.curr_menu = self.game.credits  
            self.run_display = False 
            self.game.credits.display_menu() 
        elif self.state == 'Leaderboard':
            self.game.leaderboard.display_leaderboard()
            self.run_display = True

            
        elif self.state == 'Exit':
            if self.game.show_exit_confirmation():
                self.game.running = False
        


class OptionsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Volume'
        self.setup_volume_controls()

        self.background_image = pygame.image.load('resources/blurred_bg.png')
        self.background_image = pygame.transform.scale(self.background_image, (self.game.DISPLAY_W, self.game.DISPLAY_H))

        self.back_button_rect = pygame.Rect(20, self.game.DISPLAY_H - 60, 100, 40)

    def setup_volume_controls(self):
        self.volume = 1
        self.slider_width = 300
        self.slider_height = 8
        self.slider_x = (self.game.DISPLAY_W // 2) - (self.slider_width // 2)
        self.slider_y = (self.game.DISPLAY_H // 2)
        self.slider_rect = pygame.Rect(self.slider_x, self.slider_y, self.slider_width, self.slider_height)
        self.knob_radius = 10

        self.label_x = self.game.DISPLAY_W // 2
        self.label_y = self.slider_y - 50

        self.plus_button_rect = pygame.Rect(self.slider_rect.right + 20, self.slider_y - 10, 20, 20)
        self.minus_button_rect = pygame.Rect(self.slider_rect.left - 40, self.slider_y - 10, 20, 20)

        self.background_music.set_volume(self.volume)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.blit(self.background_image, (0, 0))

            self.draw_title()
            self.draw_volume_label()
            self.draw_volume_slider()
            self.draw_volume_buttons()
            self.draw_back_button()
            self.handle_volume_control()

            self.blit_screen()

    def draw_title(self):
        font = pygame.font.Font(None, int(60 * 2))
        font.set_bold(True)
        font.set_italic(True)

        text_surface = font.render("OPTIONS", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.game.DISPLAY_W / 2, 50))

        stroke_color = (255, 0, 0)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            outline_surface = font.render("OPTIONS", True, stroke_color)
            outline_rect = outline_surface.get_rect(center=(self.game.DISPLAY_W / 2 + dx, 50 + dy))
            self.game.display.blit(outline_surface, outline_rect)

        self.game.display.blit(text_surface, text_rect)

    def draw_volume_label(self):
        font = pygame.font.Font(None, 36)
        label_text = "Background Music"

        text_surface = font.render(label_text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.label_x, self.label_y))

        stroke_color = (255, 255, 255)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            outline_surface = font.render(label_text, True, stroke_color)
            outline_rect = outline_surface.get_rect(center=(self.label_x + dx, self.label_y + dy))
            self.game.display.blit(outline_surface, outline_rect)

        self.game.display.blit(text_surface, text_rect)

    def draw_volume_slider(self):
        pygame.draw.rect(self.game.display, (0, 0, 0), self.slider_rect)
        knob_x = self.slider_rect.x + int(self.slider_rect.width * self.volume)
        knob_y = self.slider_rect.centery
        pygame.draw.circle(self.game.display, (255, 255, 255), (knob_x, knob_y), self.knob_radius)

    def draw_volume_buttons(self):
        font = pygame.font.Font(None, 30)

        pygame.draw.rect(self.game.display, (200, 200, 200), self.minus_button_rect, border_radius=15)
        pygame.draw.rect(self.game.display, (255, 255, 255), self.minus_button_rect, 3, border_radius=15)
        minus_text = font.render("-", True, (0, 0, 0))
        minus_rect = minus_text.get_rect(center=self.minus_button_rect.center)
        self.game.display.blit(minus_text, minus_rect)

        pygame.draw.rect(self.game.display, (200, 200, 200), self.plus_button_rect, border_radius=15)
        pygame.draw.rect(self.game.display, (255, 255, 255), self.plus_button_rect, 3, border_radius=15)
        plus_text = font.render("+", True, (0, 0, 0))
        plus_rect = plus_text.get_rect(center=self.plus_button_rect.center)
        self.game.display.blit(plus_text, plus_rect)

    def draw_back_button(self):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.back_button_rect.collidepoint(mouse_pos)

        button_color = self.hover_color if is_hovered else self.normal_color
        pygame.draw.rect(self.game.display, button_color, self.back_button_rect, border_radius=15)
        pygame.draw.rect(self.game.display, (255, 255, 255), self.back_button_rect, 3, border_radius=15)

        font = pygame.font.Font(None, 30)
        text = font.render("Back", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.back_button_rect.center)
        self.game.display.blit(text, text_rect)
    def handle_volume_control(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()[0]
        if mouse_click and self.slider_rect.collidepoint(mouse_pos):
            new_x = max(self.slider_rect.left, min(mouse_pos[0], self.slider_rect.right))
            self.volume = (new_x - self.slider_rect.x) / self.slider_rect.width
            self.volume = max(0, min(1, self.volume))
            self.background_music.set_volume(self.volume)
        if mouse_click:
            if self.minus_button_rect.collidepoint(mouse_pos):
                self.volume = max(0, self.volume - 0.05)
            elif self.plus_button_rect.collidepoint(mouse_pos):
                self.volume = min(1, self.volume + 0.05)
            self.background_music.set_volume(self.volume)


    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.checkers
            self.run_display = False

        if pygame.mouse.get_pressed()[0]:
            if self.back_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.game.curr_menu = self.game.checkers
                self.run_display = False

class CreditsMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.credits_image = pygame.image.load('resources/blurred_bg.png')
        self.credits_image = pygame.transform.scale(self.credits_image, (self.game.DISPLAY_W, self.game.DISPLAY_H))

        self.box_width = 300
        self.box_height = 200
        self.box_margin = 30
        self.top_margin = 200
        self.left_screen_margin = 50
        self.right_screen_margin = 50

        total_width = 3 * self.box_width + 2 * self.box_margin
        start_x = (self.game.DISPLAY_W - total_width - self.left_screen_margin - self.right_screen_margin) // 2 + self.left_screen_margin
        self.box_positions = [
            (start_x + i * (self.box_width + self.box_margin), self.top_margin)
            for i in range(3)
        ]

        self.box_texts = [
            [
                "Bipulranjan Paudel",
                "Frontend:",
                "- User input form",
                "- Sound integration",
                "Backend:",
                "- Piece movement",
                "- Minimax algorithm",
            ],
            [
                "Manjil Shrestha",
                "Frontend:",
                "- Entire game menu",
                "Backend:",
                "- File handling",
                "- Minimax pruning",
                "- Alpha-beta pruning"
            ],
            [
                "Sworup Shrestha",
                "Frontend:",
                "- Piece designing",
                "- UI improvements",
                "Backend:",
                "- Score calculation",
                "- Alpha-beta pruning",
            ],
        ]

        self.back_button_rect = pygame.Rect(20, self.game.DISPLAY_H - 60, 100, 40)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.blit(self.credits_image, (0, 0))
            self.draw_title()

            for i, position in enumerate(self.box_positions):
                self.draw_box(position, self.box_texts[i])

            self.draw_back_button()
            self.blit_screen()

    def draw_title(self):
        font = pygame.font.Font(None, 70)
        font.set_italic(True)

        text_surface = font.render("CREDITS", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(self.game.DISPLAY_W / 2, 80))

        stroke_color = (255, 0, 0)
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            outline_surface = font.render("CREDITS", True, stroke_color)
            outline_rect = outline_surface.get_rect(center=(self.game.DISPLAY_W / 2 + dx, 80 + dy))
            self.game.display.blit(outline_surface, outline_rect)

        self.game.display.blit(text_surface, text_rect)

    def draw_box(self, position, text_lines):
        box_rect = pygame.Rect(position[0], position[1], self.box_width, self.box_height)

        pygame.draw.rect(self.game.display, (0, 0, 0), box_rect, border_radius=15)
        pygame.draw.rect(self.game.display, (255, 255, 255), box_rect, 3, border_radius=15)

        font = pygame.font.Font(None, 25)
        text_y = position[1] + 20
        for line in text_lines:
            text_surface = font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(position[0] + self.box_width // 2, text_y))
            self.game.display.blit(text_surface, text_rect)
            text_y += 25

    def draw_back_button(self):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.back_button_rect.collidepoint(mouse_pos)

        button_color = self.hover_color if is_hovered else self.normal_color
        pygame.draw.rect(self.game.display, button_color, self.back_button_rect, border_radius=15)
        pygame.draw.rect(self.game.display, (255, 255, 255), self.back_button_rect, 3, border_radius=15)

        font = pygame.font.Font(None, 30)
        text = font.render("Back", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.back_button_rect.center)
        self.game.display.blit(text, text_rect)

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.checkers
            self.run_display = False

        if pygame.mouse.get_pressed()[0]:
            if self.back_button_rect.collidepoint(pygame.mouse.get_pos()):
                self.game.curr_menu = self.game.checkers
                self.run_display = False

