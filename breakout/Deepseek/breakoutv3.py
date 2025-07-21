import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 15
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 75, 30
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
COLORS = [RED, GREEN, BLUE, YELLOW]

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout")
clock = pygame.time.Clock()

# Game objects
class Paddle:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, 
                               HEIGHT - 50, 
                               PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 8
        
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed
            
    def draw(self):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()
        
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.radius = BALL_RADIUS
        self.dx = random.choice([-5, 5])
        self.dy = -5
        
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        # Wall collision
        if self.x <= self.radius or self.x >= WIDTH - self.radius:
            self.dx *= -1
        if self.y <= self.radius:
            self.dy *= -1
            
    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

class Brick:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.color = color
        self.active = True
        
    def draw(self):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)
            pygame.draw.rect(screen, BLACK, self.rect, 2)

# Game setup
def setup_bricks():
    bricks = []
    rows = 4
    cols = WIDTH // BRICK_WIDTH
    
    for row in range(rows):
        for col in range(cols):
            if col * BRICK_WIDTH < WIDTH:
                brick = Brick(col * BRICK_WIDTH, 
                             row * BRICK_HEIGHT + 50, 
                             random.choice(COLORS))
                bricks.append(brick)
    return bricks

def check_collision(ball, paddle, bricks):
    # Paddle collision
    if (ball.y + ball.radius >= paddle.rect.top and 
        ball.x >= paddle.rect.left and 
        ball.x <= paddle.rect.right):
        ball.dy *= -1
        # Add some angle variation based on where it hits the paddle
        ball.dx = (ball.x - paddle.rect.centerx) * 0.05
        
    # Brick collision
    for brick in bricks:
        if brick.active and brick.rect.collidepoint(ball.x, ball.y):
            brick.active = False
            ball.dy *= -1
            return True
    return False

def draw_text(text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = setup_bricks()
    lives = 3
    score = 0
    game_over = False
    running = True
    
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and game_over:
                    # Reset game
                    paddle = Paddle()
                    ball = Ball()
                    bricks = setup_bricks()
                    lives = 3
                    score = 0
                    game_over = False
        
        if not game_over:
            # Paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                paddle.move("left")
            if keys[pygame.K_RIGHT]:
                paddle.move("right")
            
            # Ball movement
            ball.move()
            
            # Check collisions
            if check_collision(ball, paddle, bricks):
                score += 10
            
            # Check if ball is out of bounds
            if ball.y >= HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    ball.reset()
            
            # Check if all bricks are destroyed
            if all(not brick.active for brick in bricks):
                bricks = setup_bricks()
                ball.reset()
        
        # Drawing
        screen.fill(BLACK)
        
        if game_over:
            draw_text("GAME OVER", 64, WIDTH // 2, HEIGHT // 2 - 50)
            draw_text(f"Final Score: {score}", 36, WIDTH // 2, HEIGHT // 2 + 20)
            draw_text("Press SPACE to play again", 36, WIDTH // 2, HEIGHT // 2 + 70)
        else:
            paddle.draw()
            ball.draw()
            for brick in bricks:
                brick.draw()
            
            # Draw score and lives
            draw_text(f"Score: {score}", 36, 70, 20)
            draw_text(f"Lives: {lives}", 36, WIDTH - 70, 20)
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()