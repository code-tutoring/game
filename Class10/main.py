import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the game window (width = 800, height = 600)
screen = pygame.display.set_mode((800, 600))

# Control the game's frame rate
clock = pygame.time.Clock()

# Define colors using RGB (Red, Green, Blue) values
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Caption the name of the game
pygame.display.set_caption("Catch the coins!")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()