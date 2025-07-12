import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
BALL_RADIUS = 10
BRICK_WIDTH = 80
BRICK_HEIGHT = 30
BRICK_ROWS = 5
BRICK_COLS = 10
BRICK_TOP_OFFSET = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

# Game colors for bricks
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, CYAN]

class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - 50
        self.speed = 8
        self.color = WHITE
    
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Ball:
    def __init__(self):
        self.radius = BALL_RADIUS
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.dx = 5.0
        self.dy = -5.0
        self.color = WHITE
        self.speed = 5.0
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def reset(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 100
        self.dx = random.choice([-self.speed, self.speed])
        self.dy = -self.speed
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, 
                          self.radius * 2, self.radius * 2)

class Brick:
    def __init__(self, x, y, color):
        self.width = BRICK_WIDTH
        self.height = BRICK_HEIGHT
        self.x = x
        self.y = y
        self.color = color
        self.active = True
    
    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Add a border
            pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Breakout")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        
        self.reset_game()
    
    def reset_game(self):
        self.paddle = Paddle()
        self.ball = Ball()
        self.bricks = []
        self.score = 0
        self.lives = 3
        self.game_state = "playing"  # "playing", "paused", "game_over", "won"
        self.create_bricks()
    
    def create_bricks(self):
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * BRICK_WIDTH
                y = row * BRICK_HEIGHT + BRICK_TOP_OFFSET
                color = BRICK_COLORS[row]
                brick = Brick(x, y, color)
                self.bricks.append(brick)
    
    def handle_collisions(self):
        # Ball and paddle collision
        if self.ball.get_rect().colliderect(self.paddle.get_rect()):
            # Calculate where the ball hit the paddle
            relative_intersect_x = (self.paddle.x + self.paddle.width / 2) - self.ball.x
            normalized_intersect = relative_intersect_x / (self.paddle.width / 2)
            bounce_angle = normalized_intersect * 0.75  # Max 75 degree bounce
            
            self.ball.dy = -abs(self.ball.dy)  # Always bounce up
            self.ball.dx = -self.ball.speed * bounce_angle
        
        # Ball and walls collision
        if self.ball.x <= self.ball.radius or self.ball.x >= SCREEN_WIDTH - self.ball.radius:
            self.ball.dx = -self.ball.dx
        if self.ball.y <= self.ball.radius:
            self.ball.dy = -self.ball.dy
        
        # Ball and bricks collision
        for brick in self.bricks:
            if brick.active and self.ball.get_rect().colliderect(brick.get_rect()):
                brick.active = False
                self.score += 10
                
                # Determine collision side and bounce accordingly
                ball_rect = self.ball.get_rect()
                brick_rect = brick.get_rect()
                
                # Calculate overlap on each side
                overlap_left = ball_rect.right - brick_rect.left
                overlap_right = brick_rect.right - ball_rect.left
                overlap_top = ball_rect.bottom - brick_rect.top
                overlap_bottom = brick_rect.bottom - ball_rect.top
                
                # Find the smallest overlap (the side of collision)
                min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
                
                if min_overlap == overlap_left or min_overlap == overlap_right:
                    self.ball.dx = -self.ball.dx
                else:
                    self.ball.dy = -self.ball.dy
                
                break  # Only handle one collision per frame
        
        # Ball falls below screen
        if self.ball.y >= SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_state = "game_over"
            else:
                self.ball.reset()
        
        # Check if all bricks are destroyed
        if all(not brick.active for brick in self.bricks):
            self.game_state = "won"
    
    def update(self):
        if self.game_state == "playing":
            # Handle paddle movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.paddle.move("left")
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.paddle.move("right")
            
            # Move ball
            self.ball.move()
            
            # Handle collisions
            self.handle_collisions()
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw game objects
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        
        for brick in self.bricks:
            brick.draw(self.screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 40))
        
        # Draw game state messages
        if self.game_state == "paused":
            pause_text = self.large_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
            
            instruction_text = self.font.render("Press SPACE to continue", True, WHITE)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(instruction_text, instruction_rect)
        
        elif self.game_state == "game_over":
            game_over_text = self.large_font.render("GAME OVER", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(final_score_text, final_score_rect)
            
            restart_text = self.font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(restart_text, restart_rect)
        
        elif self.game_state == "won":
            won_text = self.large_font.render("YOU WIN!", True, GREEN)
            text_rect = won_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(won_text, text_rect)
            
            final_score_text = self.font.render(f"Final Score: {self.score}", True, WHITE)
            final_score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(final_score_text, final_score_rect)
            
            restart_text = self.font.render("Press R to play again", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                
                if event.key == pygame.K_SPACE:
                    if self.game_state == "paused":
                        self.game_state = "playing"
                    elif self.game_state == "playing":
                        self.game_state = "paused"
                
                if event.key == pygame.K_r:
                    if self.game_state in ["game_over", "won"]:
                        self.reset_game()
        
        return True
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run() 