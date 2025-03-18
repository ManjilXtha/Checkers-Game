import pygame

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 600
ROWS, COLS = 8, 8
BOARD_WIDTH,BOARD_HEIGHT=600,600
SQUARE_SIZE = BOARD_WIDTH//COLS

#rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW=(255,255,0)
GREY = (100, 100, 100)
GOLD = (255, 215, 0)
SERRIA=(221,139,73)
ROPE=(142,78,30)
JAMBALAYA=(86,48,20)

CROWN = pygame.transform.scale(pygame.image.load('resources/crown.png'), (35, 25))

# Load sounds
MOVE_SOUND = pygame.mixer.Sound('resources/move-self.mp3')
CAPTURE_SOUND = pygame.mixer.Sound('resources/capture.mp3')
DOUBLE_JUMP_SOUND = pygame.mixer.Sound('resources/move-check.mp3')
KING_SOUND = pygame.mixer.Sound('resources/promote.mp3')