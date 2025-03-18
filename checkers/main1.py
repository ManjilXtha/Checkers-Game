import pygame

pygame.init()
pygame.mixer.init()

from checkers.constant import WIDTH, HEIGHT
from checkers.pvp import PVP

WIN = pygame.display.set_mode((900, 600))
pygame.display.set_caption('Checkers')
game=PVP(WIN)
game.run_PVP()
pygame.quit()