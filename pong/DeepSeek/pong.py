# DeepSeek DeepThink R1
import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")

# Colors
BACKGROUND = (15, 20, 25)
PADDLE_COLOR = (70, 130, 180)
BALL_COLOR = (220, 60, 50)
TEXT_COLOR = (220, 220, 220)
NET_COLOR = (50, 50, 60, 180)
UI_BG = (30, 35, 40, 200)
UI_BORDER = (60, 70, 90)

# Game objects
PADDLE_WIDTH, PADDLE_HEIGHT = 15, 100
BALL_SIZE = 15
BALL_SPEED = 5
PADDLE_SPEED = 7

# Create surfaces for visual effects
def create_glow_surface(size, color):
    surface = pygame.Surface((size*2, size*2), pygame.SRCALPHA)
    pygame.draw.circle(surface, (*color, 30), (size, size), size)
    pygame.draw.circle(surface, (*color, 100), (size, size), size*0.7)
    return surface

ball_glow = create_glow_surface(BALL_SIZE, BALL_COLOR)

class Paddle:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = 0
        self.score = 0
        
    def move(self):
        # Move the paddle, but keep it within screen bounds
        self.rect.y += self.speed
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def draw(self, surface):
        # Draw paddle with gradient and border
        pygame.draw.rect(surface, PADDLE_COLOR, self.rect)
        pygame.draw.rect(surface, (40, 90, 140), self.rect, 3)
        
        # Draw inner highlight
        highlight = pygame.Rect(self.rect.x + 3, self.rect.y + 3, 
                               self.rect.width - 6, self.rect.height // 3)
        pygame.draw.rect(surface, (120, 180, 220), highlight, border_radius=2)

class Ball:
    def __init__(self, x, y, size):
        self.rect = pygame.Rect(x, y, size, size)
        self.size = size
        self.reset()
        
    def reset(self):
        # Place ball in center and give it a random direction
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        angle = random.uniform(-math.pi/4, math.pi/4)
        
        # Randomly choose direction to left or right
        if random.random() < 0.5:
            angle += math.pi
            
        self.dx = math.cos(angle) * BALL_SPEED
        self.dy = math.sin(angle) * BALL_SPEED
        
    def move(self, left_paddle, right_paddle):
        # Move the ball
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # Ball collision with top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy *= -1
            # Add some vertical randomness to bounce
            self.dy += random.uniform(-0.5, 0.5)
            
        # Ball collision with paddles
        if self.rect.colliderect(left_paddle.rect) and self.dx < 0:
            self.handle_paddle_collision(left_paddle)
        elif self.rect.colliderect(right_paddle.rect) and self.dx > 0:
            self.handle_paddle_collision(right_paddle)
            
        # Ball goes out of bounds (scoring)
        if self.rect.left <= 0:
            right_paddle.score += 1
            self.reset()
        elif self.rect.right >= WIDTH:
            left_paddle.score += 1
            self.reset()
    
    def handle_paddle_collision(self, paddle):
        # Calculate bounce angle based on where ball hits paddle
        relative_y = (paddle.rect.centery - self.rect.centery) / (PADDLE_HEIGHT / 2)
        bounce_angle = relative_y * (math.pi/3)  # Max 60 degree angle
        
        # Determine new direction based on which paddle was hit
        direction = 1 if self.dx < 0 else -1
        
        self.dx = abs(self.dx) * -direction * 1.05  # Increase speed slightly
        self.dy = -math.sin(bounce_angle) * BALL_SPEED
        
        # Add visual feedback by making paddle flash
        global paddle_flash
        paddle_flash = 5
    
    def draw(self, surface):
        # Draw glow effect
        glow_rect = ball_glow.get_rect(center=self.rect.center)
        surface.blit(ball_glow, glow_rect)
        
        # Draw the ball
        pygame.draw.circle(surface, BALL_COLOR, self.rect.center, self.size)
        pygame.draw.circle(surface, (255, 200, 200), self.rect.center, self.size//2)

# Create game objects
left_paddle = Paddle(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = Paddle(WIDTH - 30 - PADDLE_WIDTH, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = Ball(WIDTH//2, HEIGHT//2, BALL_SIZE)

# Game variables
clock = pygame.time.Clock()
paddle_flash = 0
game_font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 60)

# Draw the net in the middle of the screen
def draw_net(surface):
    for y in range(0, HEIGHT, 20):
        pygame.draw.rect(surface, NET_COLOR, (WIDTH//2 - 2, y, 4, 10))

# Draw UI elements
def draw_ui(surface, left_score, right_score):
    # Draw semi-transparent background for scores
    score_bg = pygame.Rect(WIDTH//2 - 100, 10, 200, 60)
    pygame.draw.rect(surface, UI_BG, score_bg, border_radius=15)
    pygame.draw.rect(surface, UI_BORDER, score_bg, 3, border_radius=15)
    
    # Draw scores
    left_text = game_font.render(f"{left_score}", True, TEXT_COLOR)
    right_text = game_font.render(f"{right_score}", True, TEXT_COLOR)
    colon = game_font.render(":", True, TEXT_COLOR)
    
    surface.blit(left_text, (WIDTH//2 - 50 - left_text.get_width(), 30))
    surface.blit(colon, (WIDTH//2 - colon.get_width()//2, 30))
    surface.blit(right_text, (WIDTH//2 + 50, 30))
    
    # Draw title
    title = title_font.render("PYGAME PONG", True, TEXT_COLOR)
    surface.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT - 50))
    
    # Draw instructions
    instructions = game_font.render("W/S keys for left paddle | UP/DOWN arrows for right paddle", True, (150, 150, 170))
    surface.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 80))

# Draw paddle flash effect
def draw_paddle_flash(surface, paddle):
    flash = pygame.Surface((paddle.rect.width + 10, paddle.rect.height + 10), pygame.SRCALPHA)
    pygame.draw.rect(flash, (255, 255, 255, 150), 
                    (5, 5, paddle.rect.width, paddle.rect.height),
                    border_radius=3)
    surface.blit(flash, (paddle.rect.x - 5, paddle.rect.y - 5))

# Main game loop
while True:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # Key presses for paddle movement
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                left_paddle.speed = -PADDLE_SPEED
            if event.key == pygame.K_s:
                left_paddle.speed = PADDLE_SPEED
            if event.key == pygame.K_UP:
                right_paddle.speed = -PADDLE_SPEED
            if event.key == pygame.K_DOWN:
                right_paddle.speed = PADDLE_SPEED
        
        # Key releases for paddle movement
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_w, pygame.K_s):
                left_paddle.speed = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                right_paddle.speed = 0
    
    # Update game objects
    left_paddle.move()
    right_paddle.move()
    ball.move(left_paddle, right_paddle)
    
    # Reduce flash timer
    if paddle_flash > 0:
        paddle_flash -= 1
    
    # Drawing
    screen.fill(BACKGROUND)
    
    # Draw the net
    draw_net(screen)
    
    # Draw paddles
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    
    # Draw paddle flash if active
    if paddle_flash > 0:
        draw_paddle_flash(screen, left_paddle)
        draw_paddle_flash(screen, right_paddle)
    
    # Draw ball
    ball.draw(screen)
    
    # Draw UI
    draw_ui(screen, left_paddle.score, right_paddle.score)
    
    # Update display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(60)