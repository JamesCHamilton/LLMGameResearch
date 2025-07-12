#Google Gemini 2.5 Flash 
import pygame
import random

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyPong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 7

# Ball properties
BALL_SIZE = 20
BALL_SPEED_X = 7
BALL_SPEED_Y = 7

# Fonts
FONT = pygame.font.Font(None, 74)

# --- Game Objects ---

# Paddle class
class Paddle:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = color

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, self.rect)

    def move(self, dy):
        self.rect.y += dy
        # Keep paddle within screen bounds
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ball class
class Ball:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.color = color
        self.dx = BALL_SPEED_X * random.choice((1, -1))
        self.dy = BALL_SPEED_Y * random.choice((1, -1))

    def draw(self):
        pygame.draw.ellipse(SCREEN, self.color, self.rect)

    def move(self):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # Wall collisions (top/bottom)
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.dx = BALL_SPEED_X * random.choice((1, -1))
        self.dy = BALL_SPEED_Y * random.choice((1, -1))

# --- Game Setup ---
player1_paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, RED)
player2_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, BLUE)
pong_ball = Ball(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, WHITE)

player1_score = 0
player2_score = 0

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- Paddle Movement ---
    keys = pygame.key.get_pressed()
    # Player 1
    if keys[pygame.K_w]:
        player1_paddle.move(-PADDLE_SPEED)
    if keys[pygame.K_s]:
        player1_paddle.move(PADDLE_SPEED)
    # Player 2
    if keys[pygame.K_UP]:
        player2_paddle.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        player2_paddle.move(PADDLE_SPEED)

    # --- Ball Movement ---
    pong_ball.move()

    # --- Ball Collision with Paddles ---
    if pong_ball.rect.colliderect(player1_paddle.rect) or \
       pong_ball.rect.colliderect(player2_paddle.rect):
        pong_ball.dx *= -1

    # --- Ball out of bounds (Scoring) ---
    if pong_ball.rect.left <= 0:
        player2_score += 1
        pong_ball.reset()
    if pong_ball.rect.right >= WIDTH:
        player1_score += 1
        pong_ball.reset()

    # --- Drawing ---
    SCREEN.fill(BLACK)  # Clear screen
    player1_paddle.draw()
    player2_paddle.draw()
    pong_ball.draw()

    # Draw scores
    score_text = FONT.render(f"{player1_score} : {player2_score}", True, WHITE)
    SCREEN.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit PyGame
pygame.quit()