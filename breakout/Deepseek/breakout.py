import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Colors
BACKGROUND = (10, 20, 30)
PADDLE_COLOR = (70, 130, 180)
BALL_COLOR = (220, 220, 220)
BRICK_COLORS = [
    (220, 60, 60),    # Red
    (255, 140, 0),    # Orange
    (255, 215, 0),    # Yellow
    (50, 205, 50),    # Green
    (30, 144, 255),   # Blue
]
TEXT_COLOR = (220, 220, 220)
BORDER_COLOR = (40, 100, 150)
GAME_OVER_BG = (20, 30, 40, 200)

# Game constants
PADDLE_WIDTH = 120
PADDLE_HEIGHT = 20
PADDLE_SPEED = 8
BALL_RADIUS = 12
BALL_SPEED_X = 5
BALL_SPEED_Y = -5
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_GAP = 5

# Game state
class GameState:
    START = 0
    PLAYING = 1
    GAME_OVER = 2

# Paddle class
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 50
        self.speed = PADDLE_SPEED
        self.color = PADDLE_COLOR
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=8)
        # Draw a highlight on the paddle
        pygame.draw.rect(screen, (100, 180, 255), 
                         (self.rect.x, self.rect.y, self.rect.width, 5), 
                         border_radius=8)
    
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed

# Ball class
class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-1, 1]) * BALL_SPEED_X
        self.dy = BALL_SPEED_Y
        self.color = BALL_COLOR
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 
                               self.radius * 2, self.radius * 2)
        self.active = False
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
        # Draw a highlight on the ball
        pygame.draw.circle(screen, (255, 255, 255), 
                          (self.x - self.radius//3, self.y - self.radius//3), 
                          self.radius//3)
    
    def move(self):
        if not self.active:
            return
            
        # Move the ball
        self.x += self.dx
        self.y += self.dy
        self.rect.center = (self.x, self.y)
        
        # Wall collisions
        if self.x - self.radius <= 0 or self.x + self.radius >= WIDTH:
            self.dx *= -1
            self.play_sound("wall")
        if self.y - self.radius <= 0:
            self.dy *= -1
            self.play_sound("wall")
    
    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-1, 1]) * BALL_SPEED_X
        self.dy = BALL_SPEED_Y
        self.rect.center = (self.x, self.y)
        self.active = False
    
    def play_sound(self, sound_type):
        # This is a placeholder for sound effects
        pass

# Brick class
class Brick:
    def __init__(self, x, y, color):
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.x = x
        self.y = y
        self.color = color
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.visible = True
    
    def draw(self):
        if self.visible:
            pygame.draw.rect(screen, self.color, self.rect, border_radius=4)
            # Draw a border around the brick
            pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius=4)

# Particle effect for when bricks are hit
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Game class
class BreakoutGame:
    def __init__(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.particles = []
        self.score = 0
        self.lives = 3
        self.game_state = GameState.START
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        self.create_bricks()
    
    def create_bricks(self):
        self.bricks = []
        start_x = (WIDTH - (BRICK_COLS * (BRICK_WIDTH + BRICK_GAP) - BRICK_GAP)) // 2
        start_y = 60
        
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = start_y + row * (BRICK_HEIGHT + BRICK_GAP)
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                self.bricks.append(Brick(x, y, color))
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.START:
                        self.game_state = GameState.PLAYING
                        self.ball.active = True
                    elif self.game_state == GameState.PLAYING:
                        self.ball.active = True
                    elif self.game_state == GameState.GAME_OVER:
                        self.reset_game()
                
                if event.key == pygame.K_r:
                    self.reset_game()
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def update(self):
        if self.game_state != GameState.PLAYING:
            return
        
        # Move paddle with keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.paddle.move("left")
        if keys[pygame.K_RIGHT]:
            self.paddle.move("right")
        
        # Move the ball
        self.ball.move()
        
        # Ball-paddle collision
        if self.ball.rect.colliderect(self.paddle.rect) and self.ball.dy > 0:
            self.ball.dy *= -1
            # Add some angle based on where the ball hits the paddle
            offset = (self.ball.x - self.paddle.rect.centerx) / (self.paddle.width / 2)
            self.ball.dx = offset * BALL_SPEED_X
            self.ball.play_sound("paddle")
        
        # Ball-brick collisions
        for brick in self.bricks:
            if brick.visible and self.ball.rect.colliderect(brick.rect):
                brick.visible = False
                self.score += 10
                
                # Create particle effect
                for _ in range(20):
                    self.particles.append(Particle(
                        brick.rect.centerx, brick.rect.centery,
                        brick.color
                    ))
                
                # Ball direction change
                if abs(self.ball.rect.bottom - brick.rect.top) < 10 and self.ball.dy > 0:
                    self.ball.dy *= -1
                elif abs(self.ball.rect.top - brick.rect.bottom) < 10 and self.ball.dy < 0:
                    self.ball.dy *= -1
                elif abs(self.ball.rect.right - brick.rect.left) < 10 and self.ball.dx > 0:
                    self.ball.dx *= -1
                elif abs(self.ball.rect.left - brick.rect.right) < 10 and self.ball.dx < 0:
                    self.ball.dx *= -1
                
                self.ball.play_sound("brick")
                break
        
        # Check if ball fell off the bottom
        if self.ball.y > HEIGHT:
            self.lives -= 1
            self.ball.reset()
            if self.lives <= 0:
                self.game_state = GameState.GAME_OVER
        
        # Check if all bricks are destroyed
        if all(not brick.visible for brick in self.bricks):
            self.create_bricks()
            self.ball.reset()
            self.lives += 1  # Bonus life for clearing the level
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        # Draw background
        screen.fill(BACKGROUND)
        
        # Draw decorative border
        pygame.draw.rect(screen, BORDER_COLOR, (0, 0, WIDTH, HEIGHT), 10)
        
        # Draw particles
        for particle in self.particles:
            particle.draw()
        
        # Draw bricks
        for brick in self.bricks:
            brick.draw()
        
        # Draw paddle
        self.paddle.draw()
        
        # Draw ball
        self.ball.draw()
        
        # Draw score and lives
        score_text = self.font.render(f"Score: {self.score}", True, TEXT_COLOR)
        lives_text = self.font.render(f"Lives: {self.lives}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 15))
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 20, 15))
        
        # Draw game state messages
        if self.game_state == GameState.START:
            self.draw_start_screen()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        
        # Draw instructions
        instructions = self.small_font.render("Press SPACE to launch ball, R to restart, ESC to quit", True, TEXT_COLOR)
        screen.blit(instructions, (WIDTH//2 - instructions.get_width()//2, HEIGHT - 30))
    
    def draw_start_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title = self.font.render("BREAKOUT", True, (255, 215, 0))
        start_text = self.font.render("Press SPACE to Start", True, TEXT_COLOR)
        controls = self.small_font.render("Use LEFT and RIGHT arrows to move paddle", True, TEXT_COLOR)
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 60))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT//2 + 50))
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill(GAME_OVER_BG)
        screen.blit(overlay, (0, 0))
        
        game_over = self.font.render("GAME OVER", True, (220, 60, 60))
        score_text = self.font.render(f"Final Score: {self.score}", True, TEXT_COLOR)
        restart = self.font.render("Press R to Restart", True, TEXT_COLOR)
        
        screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 60))
    
    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.create_bricks()
        self.particles = []
        self.score = 0
        self.lives = 3
        self.game_state = GameState.START

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = BreakoutGame()
    
    while True:
        game.handle_events()
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()