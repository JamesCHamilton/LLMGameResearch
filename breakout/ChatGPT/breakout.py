import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 102, 204)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (50, 50, 50)

# Clock and font
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Paddle
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
paddle = pygame.Rect((WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40), (PADDLE_WIDTH, PADDLE_HEIGHT))

# Ball
BALL_RADIUS = 10
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx, ball_dy = 4, -4

# Bricks
BRICK_ROWS, BRICK_COLS = 6, 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30
bricks = []

for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + 40, BRICK_WIDTH - 2, BRICK_HEIGHT - 2)
        bricks.append(brick)

# Game loop
running = True
while running:
    screen.fill(GRAY)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move paddle
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= 7
    if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
        paddle.x += 7

    # Move ball
    ball.x += ball_dx
    ball.y += ball_dy

    # Collisions with walls
    if ball.left <= 0 or ball.right >= WIDTH:
        ball_dx *= -1
    if ball.top <= 0:
        ball_dy *= -1

    # Ball falls below screen
    if ball.top > HEIGHT:
        ball.x, ball.y = WIDTH // 2, HEIGHT // 2
        ball_dx, ball_dy = 4, -4

    # Collision with paddle
    if ball.colliderect(paddle):
        ball_dy *= -1
        ball.y = paddle.top - BALL_RADIUS * 2

    # Collision with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        ball_dy *= -1

    # Draw bricks
    for brick in bricks:
        pygame.draw.rect(screen, BLUE, brick)

    # Draw paddle and ball
    pygame.draw.rect(screen, GREEN, paddle)
    pygame.draw.ellipse(screen, RED, ball)

    # Game won
    if not bricks:
        text = font.render("You Win!", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2))
        pygame.display.flip()
        pygame.time.wait(2000)
        running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
