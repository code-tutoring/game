# Define the Player class, which represents the player-controlled character
import pygame

player_image = pygame.image.load("Assets/player.png")
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() # Initialize the parent class (Sprite)
        self.image = pygame.transform.scale(player_image, (50, 50))  # Scale the image to fit
        self.rect = self.image.get_rect() # Get the rectangular area of the player image
        self.rect.x = 375  # Initial horizontal position of the player
        self.rect.y = 500  # Initial vertical position of the player
        self.speed = 5  # Player's movement speed

    # Update the player's position based on keyboard input
    def update(self):
        keys = pygame.key.get_pressed()  # Get the current state of all keys
        if keys[pygame.K_LEFT]:  # If the left arrow key is pressed
            self.rect.x -= self.speed  # Move the player left
        if keys[pygame.K_RIGHT]:  # If the right arrow key is pressed
            self.rect.x += self.speed  # Move the player right

        # Prevent the player from moving off the screen
        if self.rect.left < 0:  # If the player goes off the left side
            self.rect.left = 0  # Stop at the left edge
        if self.rect.right > 800:  # If the player goes off the right side
            self.rect.right = 800  # Stop at the right edge