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

# Load images
player_image = pygame.image.load("Assets/player.png")  # Replace with your player PNG path
object_image = pygame.image.load("Assets/object.png")  # Replace with your object PNG path

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

# Game loop
running = True
last_spawn_time = time.time()

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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

    pygame.display.update()

pygame.quit()
