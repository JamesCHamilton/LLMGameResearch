# Chat gpt 4-o generated
import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BALL_SPEED = 5
PADDLE_SPEED = 7
SCORE_FONT = pygame.font.SysFont("Arial", 40)

# Set up the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

# Paddles
paddle_width, paddle_height = 10, 100
left_paddle = pygame.Rect(50, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)
right_paddle = pygame.Rect(WIDTH - 50 - paddle_width, HEIGHT // 2 - paddle_height // 2, paddle_width, paddle_height)

# Ball
ball_size = 20
ball = pygame.Rect(WIDTH // 2 - ball_size // 2, HEIGHT // 2 - ball_size // 2, ball_size, ball_size)
ball_dx = BALL_SPEED
ball_dy = BALL_SPEED

# Score
left_score = 0
right_score = 0

# Game Loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)  # 60 FPS
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and left_paddle.top > 0:
        left_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
        left_paddle.y += PADDLE_SPEED
    if keys[pygame.K_UP] and right_paddle.top > 0:
        right_paddle.y -= PADDLE_SPEED
    if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
        right_paddle.y += PADDLE_SPEED

    # Ball Movement
    ball.x += ball_dx
    ball.y += ball_dy

    # Collisions with top/bottom walls
    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_dy *= -1

    # Collisions with paddles
    if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
        ball_dx *= -1

    # Scoring
    if ball.left <= 0:
        right_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_dx *= -1
    if ball.right >= WIDTH:
        left_score += 1
        ball.center = (WIDTH // 2, HEIGHT // 2)
        ball_dx *= -1

    # Draw paddles and ball
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)

    # Draw middle line
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    # Draw score
    left_text = SCORE_FONT.render(str(left_score), True, WHITE)
    right_text = SCORE_FONT.render(str(right_score), True, WHITE)
    screen.blit(left_text, (WIDTH // 4, 20))
    screen.blit(right_text, (WIDTH * 3 // 4, 20))

    pygame.display.flip()

pygame.quit()
sys.exit()
