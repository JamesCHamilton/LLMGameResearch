import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Title and Icon
pygame.display.set_caption("Space Invaders")
# You can add an icon here if you have an image file, e.g., pygame.image.load('icon.png')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Player
player_width = 64
player_height = 64
player_x = (SCREEN_WIDTH - player_width) / 2
player_y = SCREEN_HEIGHT - player_height - 10
player_x_change = 0

# Enemy
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_x.append(random.randint(0, SCREEN_WIDTH - 64))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(40)

# Bullet
# ready - You can't see the bullet on the screen
# fire - The bullet is currently moving
bullet_x = 0
bullet_y = SCREEN_HEIGHT - player_height - 10
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, WHITE)
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, WHITE)
    screen.blit(over_text, ((SCREEN_WIDTH - over_text.get_width()) / 2, (SCREEN_HEIGHT - over_text.get_height()) / 2))

def player(x, y):
    # Draw player as a green rectangle
    pygame.draw.rect(screen, GREEN, (x, y, player_width, player_height))

def enemy(x, y, i):
    # Draw enemy as a red rectangle
    pygame.draw.rect(screen, RED, (x, y, 64, 64))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    # Draw bullet as a yellow rectangle
    pygame.draw.rect(screen, YELLOW, (x + 16, y + 10, 8, 16)) # Adjust bullet position and size

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt(math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
    if distance < 27: # Collision threshold
        return True
    else:
        return False

# Game Loop
running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # If a keystroke is pressed, check whether it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_x = player_x # Get the current x coordinate of the player
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player movement
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= SCREEN_WIDTH - player_width:
        player_x = SCREEN_WIDTH - player_width

    # Enemy movement
    for i in range(num_of_enemies):

        # Game Over
        if enemy_y[i] > SCREEN_HEIGHT - player_height - 50: # If enemy reaches near player
            for j in range(num_of_enemies):
                enemy_y[j] = 2000 # Move all enemies off screen
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 2
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= SCREEN_WIDTH - 64:
            enemy_x_change[i] = -2
            enemy_y[i] += enemy_y_change[i]

        # Collision
        collision = is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            bullet_y = SCREEN_HEIGHT - player_height - 10
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, SCREEN_WIDTH - 64)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_y <= 0:
        bullet_y = SCREEN_HEIGHT - player_height - 10
        bullet_state = "ready"
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
