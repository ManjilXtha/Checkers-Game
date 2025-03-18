import pygame

class CHECKERS:
    def __init__(self, game):
        self.game = game
        self.state = 'Start'
        self.startx = self.game.DISPLAY_W/2
        self.starty = self.game.DISPLAY_H/2
        self.optionsx = self.game.DISPLAY_W/2
        self.optionsy = self.game.DISPLAY_H/2 + 50
        self.creditsx = self.game.DISPLAY_W/2
        self.creditsy = self.game.DISPLAY_H/2 + 100
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
        self.run_display = True

    def draw_cursor(self):
        self.game.draw_text('*', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
        elif self.game.UP_KEY:
            if self.state == 'Start':
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Options':
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = 'Start'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = 'Options'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Start':
                self.game.playing = True
            elif self.state == 'Options':
                self.game.curr_menu = self.game.options
            elif self.state == 'Credits':
                self.game.curr_menu = self.game.credits
        self.game.reset_keys()

    def display_menu(self):
        self.run_display = True
        if self.state == 'Start':
            self.game.game_loop()
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Main Menu', 20, self.game.DISPLAY_W/2, self.game.DISPLAY_H/2 - 30)
            self.game.draw_text("Start Game", 15, self.startx, self.starty)
            self.game.draw_text("Options", 15, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 15, self.creditsx, self.creditsy)
            self.draw_cursor()
            self.blit_screen()
