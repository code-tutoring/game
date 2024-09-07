import pygame
import random

# Load images
object_image = pygame.image.load("Assets/object.png")  # Replace with your object PNG path

# Define the Object class, which represents the falling objects
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()  # Initialize the parent class (Sprite)
        self.image = pygame.transform.scale(object_image, (30, 30))  # Resize the object image
        self.rect = self.image.get_rect()  # Get the rectangular area of the object image
        self.rect.x = random.randrange(0, 750)  # Random horizontal starting position
        self.rect.y = random.randrange(-100, -40)  # Random vertical starting position above the screen
        self.speed = random.randint(2, 8)  # Random speed for the falling object


    # Update the object's position
    def update(self):
        self.rect.y += self.speed  # Move the object down the screen
        if self.rect.top > 600:  # If the object falls off the bottom of the screen
            self.kill()  # Remove the object from the game
