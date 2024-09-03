import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

# Load images
player_image = pygame.image.load("Assets/player.png")
object_image = pygame.image.load("Assets/object.png")

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(player_image, (50, 50))  # Scale the image to fit
        self.rect = self.image.get_rect()
        self.rect.x = 375
        self.rect.y = 500
        self.speed = 5

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep player within screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800

# Object class
class Object(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(object_image, (30, 30))  # Scale the image to fit
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, 750)
        self.rect.y = random.randrange(-100, -40)
        self.speed = random.randint(2, 8)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > 600:
            self.kill()  # Remove the object when it goes off the screen

# Create groups for all sprites and objects
all_sprites = pygame.sprite.Group()
objects = pygame.sprite.Group()

# Create the player
player = Player()
all_sprites.add(player)

# Set the score
score = 0

# Initialize the start time
start_time = time.time()

# Function to draw text on the screen
def draw_text(surf, text, size, x, y):
    font_name = pygame.font.match_font("arial")
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, white)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# Function to draw a button
def draw_button(surf, text, x, y, w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(surf, active_color, (x, y, w, h))
        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(surf, inactive_color, (x, y, w, h))

    draw_text(surf, text, 20, x + (w / 2), y + (h / 4))

# Game functions for buttons
def resume_game():
    global game_state
    game_state = "playing"

def restart_game():
    global score, start_time, game_state, all_sprites, objects
    score = 0
    start_time = time.time()
    all_sprites.empty()
    objects.empty()
    player = Player()
    all_sprites.add(player)
    game_state = "playing"

def quit_game():
    pygame.quit()
    quit()

# Game loop
game_state = "playing"
last_spawn_time = time.time()

while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if game_state == "playing":
                    game_state = "paused"
                elif game_state == "paused":
                    resume_game()

    if game_state == "playing":
        # Update all sprites
        all_sprites.update()

        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        timer_text = "Time: {:.2f}".format(elapsed_time)

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
