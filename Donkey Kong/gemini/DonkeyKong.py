import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)

# Game constants
GRAVITY = 0.5
PLAYER_SPEED = 5
JUMP_STRENGTH = -10
BARREL_SPEED = 3
LADDER_CLIMB_SPEED = 3

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

class Player(pygame.sprite.Sprite):
    """
    Represents Mario, the player character.
    Handles movement, jumping, and ladder climbing.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([20, 30])
        self.image.fill(RED)  # Mario is red
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - 50 - self.rect.height  # Start on the bottom platform
        self.vel_y = 0
        self.on_ground = False
        self.on_ladder = False
        self.direction = 1 # 1 for right, -1 for left

    def update(self, platforms, ladders):
        """
        Updates Mario's position and state based on gravity, movement, and collisions.
        """
        # Apply gravity
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y

        # Check for platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    self.on_ground = True
                elif self.vel_y < 0:  # Jumping up
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Check for ladder collisions
        self.on_ladder = False
        for ladder in ladders:
            if self.rect.colliderect(ladder.rect):
                # If Mario is on a ladder and not jumping, allow climbing
                if not self.on_ground: # Only allow climbing if not on a platform
                    self.on_ladder = True
                    self.vel_y = 0 # Stop vertical movement when on ladder

        # Keep player within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.vel_y = 0

    def move_left(self):
        """Moves Mario left."""
        self.rect.x -= PLAYER_SPEED
        self.direction = -1

    def move_right(self):
        """Moves Mario right."""
        self.rect.x += PLAYER_SPEED
        self.direction = 1

    def jump(self):
        """Makes Mario jump if on the ground."""
        if self.on_ground:
            self.vel_y = JUMP_STRENGTH
            self.on_ground = False # No longer on ground after jumping

    def climb_up(self):
        """Makes Mario climb up a ladder."""
        if self.on_ladder:
            self.rect.y -= LADDER_CLIMB_SPEED

    def climb_down(self):
        """Makes Mario climb down a ladder."""
        if self.on_ladder:
            self.rect.y += LADDER_CLIMB_SPEED

class DonkeyKong(pygame.sprite.Sprite):
    """
    Represents Donkey Kong.
    Periodically throws barrels.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([40, 40])
        self.image.fill(BROWN)  # Donkey Kong is brown
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 100
        self.rect.y = 50  # Top of the screen

        self.last_barrel_time = pygame.time.get_ticks()
        self.barrel_interval = 2000 # Milliseconds between barrels

    def update(self, barrels):
        """
        Updates Donkey Kong's state, primarily throwing barrels.
        """
        current_time = pygame.time.get_ticks()
        if current_time - self.last_barrel_time > self.barrel_interval:
            self.throw_barrel(barrels)
            self.last_barrel_time = current_time

    def throw_barrel(self, barrels):
        """
        Creates and adds a new barrel to the game.
        """
        barrel = Barrel(self.rect.centerx, self.rect.bottom)
        barrels.add(barrel)


class Princess(pygame.sprite.Sprite):
    """
    Represents the Princess.
    The player's goal is to reach her.
    """
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([25, 35])
        self.image.fill(YELLOW)  # Princess is yellow
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 150
        self.rect.y = 50  # Near Donkey Kong


class Barrel(pygame.sprite.Sprite):
    """
    Represents a barrel thrown by Donkey Kong.
    Moves downwards and rolls horizontally.
    """
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([15, 15])
        self.image.fill(ORANGE)  # Barrels are orange
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.vel_x = BARREL_SPEED * random.choice([-1, 1]) # Random initial horizontal direction

    def update(self, platforms):
        """
        Updates barrel's position, applying gravity and handling platform collisions.
        """
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        self.rect.x += self.vel_x

        # Reverse horizontal direction if hitting screen edges
        if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.vel_x *= -1

        # Check for platform collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.vel_y > 0:  # Falling down
                    self.rect.bottom = platform.rect.top
                    self.vel_y = 0
                    # Barrels keep rolling horizontally on platforms
                elif self.vel_y < 0: # Hitting platform from below
                    self.rect.top = platform.rect.bottom
                    self.vel_y = 0

        # Remove barrel if it falls off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


class Platform(pygame.sprite.Sprite):
    """
    Represents a platform that Mario and barrels can walk/roll on.
    """
    def __init__(self, x, y, width, height, tilt_right=False):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(GRAY)  # Platforms are gray
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.tilt_right = tilt_right # For visual effect, not functional tilt

    def draw(self, screen):
        """Draws the platform, optionally with a tilt visual."""
        pygame.draw.rect(screen, GRAY, self.rect)
        if self.tilt_right:
            # Draw a slight slope for visual effect
            pygame.draw.line(screen, BLACK, (self.rect.left, self.rect.bottom), (self.rect.right, self.rect.top), 2)
        else:
            pygame.draw.line(screen, BLACK, (self.rect.left, self.rect.top), (self.rect.right, self.rect.bottom), 2)


class Ladder(pygame.sprite.Sprite):
    """
    Represents a ladder that Mario can climb.
    """
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface([20, height])
        self.image.fill(BROWN)  # Ladders are brown
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Game state management
GAME_STATE_START = 0
GAME_STATE_PLAYING = 1
GAME_STATE_GAME_OVER = 2
GAME_STATE_WIN = 3

current_game_state = GAME_STATE_START

def create_level():
    """
    Creates the platforms and ladders for the game level.
    Returns sprite groups for platforms and ladders.
    """
    platforms = pygame.sprite.Group()
    ladders = pygame.sprite.Group()

    # Define platform layout (x, y, width, height, tilt_right)
    # Bottom platform
    platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 20, False))

    # Second level platform (from bottom, going left)
    platforms.add(Platform(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT - 150, SCREEN_WIDTH * 0.9, 20, False))

    # Third level platform (from bottom, going right)
    platforms.add(Platform(0, SCREEN_HEIGHT - 250, SCREEN_WIDTH * 0.9, 20, True))

    # Fourth level platform (from bottom, going left)
    platforms.add(Platform(SCREEN_WIDTH * 0.1, SCREEN_HEIGHT - 350, SCREEN_WIDTH * 0.9, 20, False))

    # Fifth level platform (from bottom, going right)
    platforms.add(Platform(0, SCREEN_HEIGHT - 450, SCREEN_WIDTH * 0.9, 20, True))

    # Top platform (Donkey Kong and Princess)
    platforms.add(Platform(SCREEN_WIDTH * 0.1, 100, SCREEN_WIDTH * 0.8, 20, False))


    # Define ladder layout (x, y, height)
    ladders.add(Ladder(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT - 150, 100))
    ladders.add(Ladder(SCREEN_WIDTH * 0.7, SCREEN_HEIGHT - 250, 100))
    ladders.add(Ladder(SCREEN_WIDTH * 0.3, SCREEN_HEIGHT - 350, 100))
    ladders.add(Ladder(SCREEN_WIDTH * 0.8, SCREEN_HEIGHT - 450, 100))
    ladders.add(Ladder(SCREEN_WIDTH * 0.5, 100, 350)) # Long ladder to top

    return platforms, ladders

# Create sprite groups
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
ladders = pygame.sprite.Group()
barrels = pygame.sprite.Group()

player = Player()
donkey_kong = DonkeyKong()
princess = Princess()

# Add initial sprites to groups
all_sprites.add(player, donkey_kong, princess)

# Game loop
running = True
clock = pygame.time.Clock()

def reset_game():
    """Resets all game elements to their initial state."""
    global player, donkey_kong, princess, all_sprites, barrels, platforms, ladders, current_game_state

    all_sprites.empty()
    barrels.empty()

    platforms, ladders = create_level()

    player = Player()
    donkey_kong = DonkeyKong()
    princess = Princess()

    all_sprites.add(player, donkey_kong, princess)
    for p in platforms:
        all_sprites.add(p)
    for l in ladders:
        all_sprites.add(l)

    current_game_state = GAME_STATE_PLAYING

# Initial level creation
platforms, ladders = create_level()
for p in platforms:
    all_sprites.add(p)
for l in ladders:
    all_sprites.add(l)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if current_game_state == GAME_STATE_START:
                if event.key == pygame.K_SPACE:
                    reset_game()
            elif current_game_state == GAME_STATE_GAME_OVER or current_game_state == GAME_STATE_WIN:
                if event.key == pygame.K_r:
                    reset_game()
            elif current_game_state == GAME_STATE_PLAYING:
                if event.key == pygame.K_UP:
                    player.jump()
                if event.key == pygame.K_SPACE: # Also allow space for jumping
                    player.jump()

    if current_game_state == GAME_STATE_PLAYING:
        # Player movement input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player.move_left()
        if keys[pygame.K_RIGHT]:
            player.move_right()
        if keys[pygame.K_UP]:
            player.climb_up()
        if keys[pygame.K_DOWN]:
            player.climb_down()

        # Update sprites
        player.update(platforms, ladders)
        donkey_kong.update(barrels)
        barrels.update(platforms)

        # Check for barrel collisions with player
        if pygame.sprite.spritecollideany(player, barrels):
            current_game_state = GAME_STATE_GAME_OVER

        # Check if player reached the princess
        if player.rect.colliderect(princess.rect):
            current_game_state = GAME_STATE_WIN

    # Drawing
    SCREEN.fill(BLUE)  # Sky background

    # Draw platforms and ladders first
    for p in platforms:
        p.draw(SCREEN)
    for l in ladders:
        SCREEN.blit(l.image, l.rect)

    # Draw other sprites
    SCREEN.blit(player.image, player.rect)
    SCREEN.blit(donkey_kong.image, donkey_kong.rect)
    SCREEN.blit(princess.image, princess.rect)
    for barrel in barrels:
        SCREEN.blit(barrel.image, barrel.rect)

    # Display game state messages
    if current_game_state == GAME_STATE_START:
        text_surface = large_font.render("Donkey Kong", True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(text_surface, text_rect)

        instruction_surface = font.render("Press SPACE to Start", True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        SCREEN.blit(instruction_surface, instruction_rect)

    elif current_game_state == GAME_STATE_GAME_OVER:
        game_over_surface = large_font.render("GAME OVER", True, RED)
        game_over_rect = game_over_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(game_over_surface, game_over_rect)

        restart_surface = font.render("Press 'R' to Restart", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        SCREEN.blit(restart_surface, restart_rect)

    elif current_game_state == GAME_STATE_WIN:
        win_surface = large_font.render("YOU WIN!", True, GREEN)
        win_rect = win_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
        SCREEN.blit(win_surface, win_rect)

        restart_surface = font.render("Press 'R' to Play Again", True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
        SCREEN.blit(restart_surface, restart_rect)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
