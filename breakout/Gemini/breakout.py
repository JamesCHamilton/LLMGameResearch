import pygame
import sys

# Initialize Pygame
pygame.init()

# --- Constants ---
# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Pygame Breakout"

# Colors (RGB tuples)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE] # Colors for different rows of bricks

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 7

# Ball properties
BALL_RADIUS = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = -5 # Start moving upwards

# Brick properties
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_GAP = 5 # Gap between bricks

# Calculate total width needed for bricks and gaps
total_bricks_width = BRICK_COLS * BRICK_WIDTH + (BRICK_COLS - 1) * BRICK_GAP
# Calculate starting X position to center the bricks
BRICK_START_X = (SCREEN_WIDTH - total_bricks_width) // 2
BRICK_START_Y = 50 # Starting Y position for the first row of bricks

# --- Game Classes/Functions ---

class Paddle(pygame.sprite.Sprite):
    """
    Represents the player's paddle at the bottom of the screen.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PADDLE_WIDTH, PADDLE_HEIGHT])
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 30 # Position slightly above the bottom
        self.speed = PADDLE_SPEED

    def update(self, keys):
        """
        Updates the paddle's position based on user input.
        """
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed

        # Keep paddle within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

class Ball(pygame.sprite.Sprite):
    """
    Represents the ball that bounces around the screen.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2], pygame.SRCALPHA) # SRCALPHA for transparency
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2 # Start in the middle
        self.speed_x = BALL_SPEED_X
        self.speed_y = BALL_SPEED_Y
        self.game_started = False # Flag to control ball movement before game starts

    def update(self):
        """
        Updates the ball's position and handles collisions with walls.
        """
        if not self.game_started:
            # Ball stays with paddle before game starts
            return

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Wall collisions
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.speed_x *= -1 # Reverse X direction
            # Adjust position to prevent sticking to wall
            if self.rect.left < 0: self.rect.left = 0
            if self.rect.right > SCREEN_WIDTH: self.rect.right = SCREEN_WIDTH

        if self.rect.top < 0:
            self.speed_y *= -1 # Reverse Y direction
            self.rect.top = 0 # Adjust position to prevent sticking to ceiling

    def reset(self):
        """
        Resets the ball to its initial position and stops its movement.
        """
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.centery = SCREEN_HEIGHT // 2
        self.speed_x = BALL_SPEED_X
        self.speed_y = -abs(BALL_SPEED_Y) # Ensure it moves upwards
        self.game_started = False

class Brick(pygame.sprite.Sprite):
    """
    Represents a single brick in the game.
    """
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([BRICK_WIDTH, BRICK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

def create_bricks():
    """
    Creates a grid of bricks.
    Returns a pygame.sprite.Group containing all bricks.
    """
    bricks = pygame.sprite.Group()
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x = BRICK_START_X + col * (BRICK_WIDTH + BRICK_GAP)
            y = BRICK_START_Y + row * (BRICK_HEIGHT + BRICK_GAP)
            # Cycle through colors for each row
            color_index = row % len(BRICK_COLORS)
            brick = Brick(x, y, BRICK_COLORS[color_index])
            bricks.add(brick)
    return bricks

def show_message(screen, message, color=WHITE):
    """
    Displays a message on the screen.
    """
    font = pygame.font.Font(None, 74) # Larger font for messages
    text_surface = font.render(message, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip() # Update the display to show the message

def main():
    """
    Main function to run the Breakout game.
    """
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(SCREEN_TITLE)

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    # Create game objects
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    all_sprites.add(paddle)
    all_sprites.add(ball)
    all_sprites.add(bricks) # Add bricks to all_sprites for drawing

    # Game variables
    score = 0
    lives = 3
    game_over = False
    game_won = False
    font = pygame.font.Font(None, 36) # Font for score and lives

    # --- Game Loop ---
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not ball.game_started and not game_over:
                    ball.game_started = True # Start the ball moving
                if event.key == pygame.K_r and game_over: # Restart game
                    # Reset game state
                    paddle = Paddle()
                    ball = Ball()
                    bricks = create_bricks()
                    all_sprites = pygame.sprite.Group()
                    all_sprites.add(paddle)
                    all_sprites.add(ball)
                    all_sprites.add(bricks)
                    score = 0
                    lives = 3
                    game_over = False
                    game_won = False

        if not game_over and not game_won:
            # Get pressed keys for paddle movement
            keys = pygame.key.get_pressed()
            paddle.update(keys)
            ball.update()

            # Ball-paddle collision
            if pygame.sprite.collide_rect(ball, paddle):
                # Simple bounce: reverse Y direction
                ball.speed_y *= -1
                # Adjust ball position to prevent sticking
                ball.rect.bottom = paddle.rect.top

                # More realistic bounce: change X speed based on where it hits the paddle
                # Calculate relative intersection point
                intersection_point = ball.rect.centerx - paddle.rect.centerx
                # Normalize to -1 to 1 range
                normalized_intersection = intersection_point / (PADDLE_WIDTH / 2)
                # Adjust ball's X speed based on normalized intersection
                ball.speed_x = BALL_SPEED_X * normalized_intersection * 1.5 # Multiplier for more dramatic bounce

            # Ball-brick collision
            # Use sprite.groupcollide to detect collisions between ball and bricks
            # The True, True arguments mean both sprites are removed if a collision occurs
            # (ball is not removed, but brick is removed)
            hit_bricks = pygame.sprite.spritecollide(ball, bricks, True) # True removes the brick
            for brick in hit_bricks:
                score += 10 # Increase score for each hit brick
                ball.speed_y *= -1 # Reverse ball's Y direction

            # Check if all bricks are destroyed
            if not bricks:
                game_won = True
                game_over = True # Set game_over to true to stop game logic

            # Check if ball goes below screen (missed by paddle)
            if ball.rect.top > SCREEN_HEIGHT:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    ball.reset() # Reset ball position if lives remain

        # --- Drawing ---
        screen.fill(BLACK) # Clear the screen

        # Draw all sprites
        all_sprites.draw(screen)

        # Display score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

        # Display messages
        if not ball.game_started and not game_over:
            show_message(screen, "Press SPACE to Start!", WHITE)
        elif game_over:
            if game_won:
                show_message(screen, "YOU WON! Press 'R' to Restart", GREEN)
            else:
                show_message(screen, "GAME OVER! Press 'R' to Restart", RED)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(60) # 60 frames per second

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
