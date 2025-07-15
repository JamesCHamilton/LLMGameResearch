#Github Copilot
import pygame
import sys

# Game settings
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FPS = 60
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 20
PADDLE_SPEED = 7
BALL_SPEED_X, BALL_SPEED_Y = 5, 5

# Initialize PyGame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pong')
clock = pygame.time.Clock()

# Paddle and ball setup
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH-40, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH//2 - BALL_SIZE//2, HEIGHT//2 - BALL_SIZE//2, BALL_SIZE, BALL_SIZE)

ball_speed_x = BALL_SPEED_X
ball_speed_y = BALL_SPEED_Y

score_left = 0
score_right = 0
font = pygame.font.SysFont(None, 48)

def draw():
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, left_paddle)
    pygame.draw.rect(screen, WHITE, right_paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))
    score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
    pygame.display.flip()

def reset_ball():
    global ball_speed_x, ball_speed_y
    ball.center = (WIDTH//2, HEIGHT//2)
    ball_speed_x *= -1
    ball_speed_y *= -1

def main():
    global ball_speed_x, ball_speed_y, score_left, score_right
    running = True
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        if not game_over:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w] and left_paddle.top > 0:
                left_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
                left_paddle.y += PADDLE_SPEED
            if keys[pygame.K_UP] and right_paddle.top > 0:
                right_paddle.y -= PADDLE_SPEED
            if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
                right_paddle.y += PADDLE_SPEED
            # Ball movement
            ball.x += ball_speed_x
            ball.y += ball_speed_y
            # Collision with top/bottom
            if ball.top <= 0 or ball.bottom >= HEIGHT:
                ball_speed_y *= -1
            # Collision with paddles
            if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
                ball_speed_x *= -1
            # Score
            if ball.left <= 0:
                score_right += 1
                reset_ball()
            if ball.right >= WIDTH:
                score_left += 1
                reset_ball()
            # Game over check
            if score_left == 11 or score_right == 11:
                game_over = True
        draw()
        if game_over:
            winner = "Left" if score_left == 11 else "Right"
            msg = font.render(f"Game Over! {winner} Player Wins", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2 - msg.get_height()//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
        clock.tick(FPS)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
