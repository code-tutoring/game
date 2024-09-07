import pygame  # Import the pygame module to create the game
import random  # Import random for generating random positions and speeds
import time    # Import time to keep track of elapsed time in the game
from player import Player
from object import Object

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

# Create groups for all sprites and objects
all_sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()

# Create the player and add to the all_sprites group
player = Player()
all_sprites.add(player)

# Set the score
score = 0

# Initialize the start time
start_time = time.time()

# Function to draw text on the screen
def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font("arial")  # Find a font similar to Arial
    font = pygame.font.Font(font_name, size)  # Set the font size
    text_surface = font.render(text, True, white)  # Create a text surface
    text_rect = text_surface.get_rect()  # Get the rectangular area of the text
    text_rect.midtop = (x, y)  # Position the text
    surf.blit(text_surface, text_rect)  # Draw the text on the screen

# Function to draw a button on the screen
def draw_button(surf, text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()  # Get the current mouse position
    click = pygame.mouse.get_pressed()  # Get the current mouse click state

    # Check if the mouse is over the button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(surf, active_color, (x, y, w, h))  # Draw the button in active color
        if click[0] == 1 and action is not None:  # If the button is clicked
            action()  # Call the action function
    else:
        pygame.draw.rect(surf, inactive_color, (x, y, w, h))  # Draw the button in inactive color

    # Draw the text on the button
    draw_text(surf, text, 20, x + (w / 2), y + (h / 4))

# Define functions to handle game states
def resume_game():
    global game_state
    game_state = "playing"

def restart_game():
    global score, start_time, game_state, all_sprites, objects
    score = 0  # Reset the score to 0
    start_time = time.time()  # Reset the start time
    all_sprites.empty()  # Clear all sprites
    objects.empty()  # Clear all objects
    player = Player()  # Create a new player
    all_sprites.add(player)  # Add the player to the sprites group
    game_state = "playing"  # Set the game state to playing

def quit_game():
    pygame.quit()
    quit()

# Main game loop
game_state = "playing"  # Initial game state
last_spawn_time = time.time()  # Time when the last object was spawned

while True:
    clock.tick(60)

    # Handle events like key presses or closing the game window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # If the user closes the window
            quit_game()  # Quit the game
        if event.type == pygame.KEYDOWN:  # If a key is pressed
            if event.key == pygame.K_ESCAPE:  # If the ESC key is pressed
                if game_state == "playing":  # If the game is currently playing
                    game_state = "paused"  # Pause the game
                elif game_state == "paused":  # If the game is paused
                    resume_game()  # Resume the game

    if game_state == "playing":  # If the game is in the playing state
        all_sprites.update()  # Update all sprites (player and objects)

        # Calculate how much time has passed since the game started
        elapsed_time = time.time() - start_time
        timer_text = "Time: {:.2f}".format(elapsed_time)  # Format the elapsed time

        # Constantly spawn new objects at more frequent intervals
        current_time = time.time()
        if current_time - last_spawn_time > random.uniform(0.1, 0.5):  # Random spawn interval between 0.1 and 0.5 seconds
            obj = Object()
            all_sprites.add(obj)
            objects.add(obj)
            last_spawn_time = current_time

        # Check for collisions between the player and objects
        hits = pygame.sprite.spritecollide(player, objects, True)
        for hit in hits:
            score += 1

        # Draw everything on the screen
        screen.fill(black)
        all_sprites.draw(screen)
        draw_text(screen, "Score: {}".format(score), 18, 50, 10)
        draw_text(screen, timer_text, 18, 750, 10)  # Display the timer in the top-right corner

    elif game_state == "paused":
        screen.fill(black)
        draw_text(screen, "Paused", 50, 400, 200)
        draw_button(screen, "Resume", 300, 300, 200, 50, red, green, resume_game)
        draw_button(screen, "Restart", 300, 370, 200, 50, red, green, restart_game)
        draw_button(screen, "Quit", 300, 440, 200, 50, red, green, quit_game)

    pygame.display.update()

