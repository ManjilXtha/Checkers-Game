import pygame
import sys

class Tutorial:
    def __init__(self, screen, tutorials, font,play_icon,bg_img):
        self.screen = screen
        self.tutorials = tutorials
        self.font = font
        self.current_tutorial = 0
        self.current_image = 0
        
        self.bg_img=pygame.transform.scale(bg_img,screen.get_size())
        self.play_icon=pygame.transform.scale(play_icon,(50,50))
        # Button positions
        self.play_button_rect = self.play_icon.get_rect(center=(screen.get_width() // 2, 50))
        self.back_button_rect = pygame.Rect(20, 20, 100, 50)  # Top left for "Back"
        self.next_button_rect = pygame.Rect(screen.get_width() - 120, 20, 100, 50)  # Top right for "Next"

    def draw_button(self, rect, text, color=(255, 255, 255), bgcolor=(0, 0, 0)):
        """Draw a button with text."""
        pygame.draw.rect(self.screen, bgcolor, rect)
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def draw_play_button(self):
        """Draw the joystick button at the center of the top."""
        self.screen.blit(self.play_icon, self.play_button_rect.topleft)

    def draw_text(self, text, position, color=(0, 0, 0)):
        """Render tutorial text centered at the given position."""
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(midtop=position)
        self.screen.blit(text_surface, text_rect)

    def draw(self):
        """Draw the current tutorial step on the screen."""
        # Clear the screen
        
        self.screen.fill((255, 255, 255))
        
        self.screen.blit(self.bg_img,(0,0))
        self.draw_play_button()
        # Display the current image
        current_image_surface = self.tutorials[self.current_tutorial]["images"][self.current_image]
        image_rect = current_image_surface.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 30))
        self.screen.blit(current_image_surface, image_rect)

        # Display the tutorial text
        self.draw_text(
            self.tutorials[self.current_tutorial]["text"],
            (self.screen.get_width() // 2, self.screen.get_height() // 2 + 200)
        )

        # Draw buttons
        self.draw_button(self.back_button_rect, "Back")
        self.draw_button(self.next_button_rect, "Next")

    def handle_event(self, event):
        """Handle user input for navigating the tutorial."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.play_button_rect.collidepoint(event.pos):
                print("Play button pressed")
            elif self.back_button_rect.collidepoint(event.pos):
                self.previous_step()
            elif self.next_button_rect.collidepoint(event.pos):
                self.next_step()

    def next_step(self):
        """Go to the next image or tutorial."""
        self.current_image += 1
        if self.current_image >= len(self.tutorials[self.current_tutorial]["images"]):
            self.current_image = 0
            self.current_tutorial = (self.current_tutorial + 1) % len(self.tutorials)

    def previous_step(self):
        """Go to the previous image or tutorial."""
        self.current_image -= 1
        if self.current_image < 0:
            self.current_tutorial = (self.current_tutorial - 1) % len(self.tutorials)
            self.current_image = len(self.tutorials[self.current_tutorial]["images"]) - 1
