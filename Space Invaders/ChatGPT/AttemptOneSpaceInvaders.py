import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load images
player_img = pygame.image.load('player.png')  # 64x64
enemy_img = pygame.image.load('enemy.png')    # 64x64
bullet_img = pygame.image.load('bullet.png')  # 32x32

# Player
player_x = WIDTH // 2 - 32
player_y = HEIGHT - 80
player_speed = 5

# Bullet
bullet_x = 0
bullet_y = player_y
bullet_speed = 7
bullet_state = "ready"  # "ready" or "fire"

# Enemy
num_enemies = 6
enemy_x = []
enemy_y = []
enemy_speed_x = []
enemy_speed_y = []
for _ in range(num_enemies):
    enemy_x.append(random.randint(0, WIDTH - 64))
    enemy_y.append(random.randint(50, 150))
    enemy_speed_x.append(3)
    enemy_speed_y.append(40)

# Score
score = 0
font = pygame.font.Font(None, 36)

# Collision
def is_collision(x1, y1, x2, y2):
    distance = math.hypot(x1 - x2, y1 - y2)
    return distance < 27

# Main loop
running = True
clock = pygame.time.Clock()

while running:
    screen.fill(BLACK)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Key Presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - 64:
        player_x += player_speed
    if keys[pygame.K_SPACE] and bullet_state == "ready":
        bullet_x = player_x + 16
        bullet_y = player_y
        bullet_state = "fire"

    # Bullet Movement
    if bullet_state == "fire":
        screen.blit(bullet_img, (bullet_x, bullet_y))
        bullet_y -= bullet_speed
        if bullet_y < 0:
            bullet_state = "ready"

    # Enemy Movement
    for i in range(num_enemies):
        enemy_x[i] += enemy_speed_x[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= WIDTH - 64:
            enemy_speed_x[i] *= -1
            enemy_y[i] += enemy_speed_y[i]

        # Collision
        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            bullet_y = player_y
            bullet_state = "ready"
            score += 1
            enemy_x[i] = random.randint(0, WIDTH - 64)
            enemy_y[i] = random.randint(50, 150)

        screen.blit(enemy_img, (enemy_x[i], enemy_y[i]))

    # Draw player
    screen.blit(player_img, (player_x, player_y))

    # Score text
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()
