import pygame
from game import Game

def main():
    g = Game()
    while g.running:
        g.curr_menu.display_menu()
        g.game_loop()
    pygame.quit()

if __name__ == "__main__":
    main()
