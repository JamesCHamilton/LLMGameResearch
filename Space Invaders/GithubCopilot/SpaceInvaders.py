import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Player settings
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 30
PLAYER_SPEED = 7

# Bullet settings
BULLET_WIDTH, BULLET_HEIGHT = 5, 15
BULLET_SPEED = 10

# Enemy settings
ENEMY_WIDTH, ENEMY_HEIGHT = 40, 30
ENEMY_ROWS, ENEMY_COLS = 5, 10
ENEMY_X_GAP, ENEMY_Y_GAP = 10, 10
ENEMY_SPEED = 2
ENEMY_DESCEND = 20

font = pygame.font.SysFont(None, 36)
clock = pygame.time.Clock()

def create_enemies():
    enemies = []
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            x = col * (ENEMY_WIDTH + ENEMY_X_GAP) + 60
            y = row * (ENEMY_HEIGHT + ENEMY_Y_GAP) + 50
            enemies.append(pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT))
    return enemies

def draw(player, bullets, enemies):
    SCREEN.fill(BLACK)
    pygame.draw.rect(SCREEN, GREEN, player)
    for bullet in bullets:
        pygame.draw.rect(SCREEN, BLUE, bullet)
    for enemy in enemies:
        pygame.draw.rect(SCREEN, RED, enemy)
    pygame.display.flip()

def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_WIDTH // 2, HEIGHT - 60, PLAYER_WIDTH, PLAYER_HEIGHT)
    bullets = []
    enemies = create_enemies()
    enemy_dx = ENEMY_SPEED
    running = True
    game_over = False
    win = False
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bullet = pygame.Rect(player.centerx - BULLET_WIDTH // 2, player.top, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(bullet)
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()
                    return
        if not game_over:
            # Player movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player.left > 0:
                player.x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player.right < WIDTH:
                player.x += PLAYER_SPEED
            # Bullets movement
            for bullet in bullets[:]:
                bullet.y -= BULLET_SPEED
                if bullet.bottom < 0:
                    bullets.remove(bullet)
            # Enemy movement
            move_down = False
            for enemy in enemies:
                enemy.x += enemy_dx
                if enemy.right >= WIDTH or enemy.left <= 0:
                    move_down = True
            if move_down:
                enemy_dx *= -1
                for enemy in enemies:
                    enemy.y += ENEMY_DESCEND
            # Bullet-enemy collision
            for bullet in bullets[:]:
                for enemy in enemies[:]:
                    if bullet.colliderect(enemy):
                        bullets.remove(bullet)
                        enemies.remove(enemy)
                        break
            # Enemy-player collision or enemies reach bottom
            for enemy in enemies:
                if enemy.colliderect(player) or enemy.bottom >= HEIGHT:
                    game_over = True
            # Win condition
            if not enemies:
                win = True
                game_over = True
        draw(player, bullets, enemies)
        if game_over:
            if win:
                msg = font.render("You Win! Press R to Restart", True, WHITE)
            else:
                msg = font.render("Game Over! Press R to Restart", True, WHITE)
            SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
