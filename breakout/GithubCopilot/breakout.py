import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRICK_COLOR = (200, 0, 0)
PADDLE_COLOR = (0, 200, 200)
BALL_COLOR = (200, 200, 0)

# Paddle settings
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
PADDLE_SPEED = 7

# Ball settings
BALL_RADIUS = 10
BALL_SPEED = 5

# Brick settings
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 30

# Create bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_rect = pygame.Rect(
            col * BRICK_WIDTH,
            row * BRICK_HEIGHT + 40,
            BRICK_WIDTH - 2,
            BRICK_HEIGHT - 2
        )
        bricks.append(brick_rect)

# Paddle
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 40, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_dx = BALL_SPEED * random.choice([-1, 1])
ball_dy = -BALL_SPEED

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def draw():
    SCREEN.fill(BLACK)
    for brick in bricks:
        pygame.draw.rect(SCREEN, BRICK_COLOR, brick)
    pygame.draw.rect(SCREEN, PADDLE_COLOR, paddle)
    pygame.draw.ellipse(SCREEN, BALL_COLOR, ball)
    pygame.display.flip()

def reset():
    global ball, ball_dx, ball_dy, paddle, bricks
    ball.x = WIDTH // 2
    ball.y = HEIGHT // 2
    ball_dx = BALL_SPEED * random.choice([-1, 1])
    ball_dy = -BALL_SPEED
    paddle.x = WIDTH // 2 - PADDLE_WIDTH // 2
    bricks = []
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            brick_rect = pygame.Rect(
                col * BRICK_WIDTH,
                row * BRICK_HEIGHT + 40,
                BRICK_WIDTH - 2,
                BRICK_HEIGHT - 2
            )
            bricks.append(brick_rect)

def main():
    global ball_dx, ball_dy  # Fix UnboundLocalError
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Paddle movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.x -= PADDLE_SPEED
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.x += PADDLE_SPEED

        # Ball movement
        ball.x += ball_dx
        ball.y += ball_dy

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx *= -1
        if ball.top <= 0:
            ball_dy *= -1

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_dy *= -1
            ball.y = paddle.y - BALL_RADIUS * 2

        # Ball collision with bricks
        hit_index = ball.collidelist(bricks)
        if hit_index != -1:
            hit_brick = bricks.pop(hit_index)
            # Determine collision side
            if abs(ball.bottom - hit_brick.top) < BALL_SPEED or abs(ball.top - hit_brick.bottom) < BALL_SPEED:
                ball_dy *= -1
            else:
                ball_dx *= -1

        # Ball falls below paddle
        if ball.top > HEIGHT:
            msg = font.render("Game Over! Press R to Restart", True, WHITE)
            SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        reset()
                        waiting = False

        # Win condition
        if not bricks:
            msg = font.render("You Win! Press R to Restart", True, WHITE)
            SCREEN.blit(msg, (WIDTH // 2 - msg.get_width() // 2, HEIGHT // 2))
            pygame.display.flip()
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                        reset()
                        waiting = False

        draw()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()