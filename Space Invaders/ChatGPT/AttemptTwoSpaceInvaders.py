import pygame
import random
import math

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Player
player_width = 64
player_height = 32
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 5

# Bullet
bullet_width = 5
bullet_height = 15
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"  # ready or fire

# Enemy
num_enemies = 6
enemy_width = 40
enemy_height = 30
enemy_x = [random.randint(0, WIDTH - enemy_width) for _ in range(num_enemies)]
enemy_y = [random.randint(50, 150) for _ in range(num_enemies)]
enemy_speed_x = [3 for _ in range(num_enemies)]
enemy_speed_y = [40 for _ in range(num_enemies)]

# Score
score = 0
font = pygame.font.Font(None, 36)

def is_collision(x1, y1, x2, y2):
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance < 27

clock = pygame.time.Clock()
running = True
while running:
    screen.fill(BLACK)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x + player_width // 2 - bullet_width // 2
        bullet_y = player_y
        bullet_state = "fire"

    # Bullet Movement
    if bullet_state == "fire":
        pygame.draw.rect(screen, GREEN, (bullet_x, bullet_y, bullet_width, bullet_height))
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

    # Enemies
    for i in range(num_enemies):
        enemy_x[i] += enemy_speed_x[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= WIDTH - enemy_width:
            enemy_speed_x[i] *= -1
            enemy_y[i] += enemy_speed_y[i]

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, WIDTH - enemy_width)
            enemy_y[i] = random.randint(50, 150)

        pygame.draw.rect(screen, RED, (enemy_x[i], enemy_y[i], enemy_width, enemy_height))

    # Draw player
    pygame.draw.rect(screen, WHITE, (player_x, player_y, player_width, player_height))

    # Draw score
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
