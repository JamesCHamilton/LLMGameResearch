import pygame
import random
import sys

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRAVITY = 0.5
JUMP_STRENGTH = -10
PLAYER_SPEED = 5
BARREL_SPEED = 3

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Donkey Kong")
clock = pygame.time.Clock()

# Load images (using simple rectangles for this example)
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 50))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.on_ground = False
        
    def update(self, platforms):
        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y
        
        # Check for platform collisions
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y > 0:
                if self.rect.bottom > platform.rect.top and self.rect.bottom < platform.rect.bottom:
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity_y = 0
        
        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.on_ground = True
            self.velocity_y = 0
            
    def jump(self):
        if self.on_ground:
            self.velocity_y = JUMP_STRENGTH
            
class DonkeyKong(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((80, 80))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH - 150
        self.rect.y = 100
        self.throw_timer = 0
        
    def update(self):
        self.throw_timer += 1
        return self.throw_timer > 120  # Throw a barrel every 2 seconds
        
    def throw_barrel(self):
        self.throw_timer = 0
        return Barrel(self.rect.centerx, self.rect.bottom)

class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = -1  # -1 for left, 1 for right
        self.falling = False
        
    def update(self, platforms):
        if not self.falling:
            self.rect.x += self.direction * BARREL_SPEED
            
            # Check if barrel should fall off platform
            on_platform = False
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    on_platform = True
                    break
                    
            if not on_platform:
                self.falling = True
        else:
            # Barrel is falling
            self.rect.y += BARREL_SPEED * 2
            
            # Check if barrel landed on a platform
            for platform in platforms:
                if self.rect.colliderect(platform.rect) and self.rect.bottom > platform.rect.top:
                    self.rect.bottom = platform.rect.top
                    self.falling = False
                    # Change direction when landing
                    self.direction *= -1
                    break

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Ladder(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        super().__init__()
        self.image = pygame.Surface((20, height))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Create game objects
all_sprites = pygame.sprite.Group()
platforms = pygame.sprite.Group()
barrels = pygame.sprite.Group()
ladders = pygame.sprite.Group()

# Create platforms (simplified Donkey Kong level)
platforms.add(Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Ground
platforms.add(Platform(100, 450, 600, 20))
platforms.add(Platform(150, 350, 500, 20))
platforms.add(Platform(200, 250, 400, 20))
platforms.add(Platform(250, 150, 300, 20))

# Create ladders (for climbing)
ladders.add(Ladder(400, SCREEN_HEIGHT - 50, 100))
ladders.add(Ladder(350, 350, 100))
ladders.add(Ladder(450, 250, 100))
ladders.add(Ladder(400, 150, 100))

# Create characters
player = Player()
donkey_kong = DonkeyKong()

all_sprites.add(platforms)
all_sprites.add(ladders)
all_sprites.add(player)
all_sprites.add(donkey_kong)

# Game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()
    
    # Get pressed keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player.rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player.rect.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        # Check if player is on a ladder
        for ladder in ladders:
            if player.rect.colliderect(ladder.rect):
                player.rect.y -= PLAYER_SPEED
                player.velocity_y = 0
    if keys[pygame.K_DOWN]:
        # Check if player is on a ladder
        for ladder in ladders:
            if player.rect.colliderect(ladder.rect):
                player.rect.y += PLAYER_SPEED
                player.velocity_y = 0
    
    # Update
    player.update(platforms)
    
    if donkey_kong.update():
        new_barrel = donkey_kong.throw_barrel()
        barrels.add(new_barrel)
        all_sprites.add(new_barrel)
    
    barrels.update(platforms)
    
    # Check for collisions with barrels
    if pygame.sprite.spritecollide(player, barrels, False):
        print("Game Over!")
        running = False
    
    # Check if player reached the top (win condition)
    if player.rect.top <= 100:
        print("You Win!")
        running = False
    
    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)
    barrels.draw(screen)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()