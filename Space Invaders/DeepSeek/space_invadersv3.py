import pygame
import random
import sys
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
PLAYER_SPEED = 5
ALIEN_SPEED = 1
ALIEN_DROP = 20
BULLET_SPEED = 7
ALIEN_FIRE_RATE = 0.01  # Chance per frame to fire

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Space Invaders')
clock = pygame.time.Clock()

# Load images
def load_image(name, scale=1):
    try:
        image = pygame.image.load(name)
        if scale != 1:
            size = image.get_size()
            image = pygame.transform.scale(image, (int(size[0] * scale), int(size[1] * scale)))
        return image.convert_alpha()
    except:
        # Create a placeholder if image not found
        surf = pygame.Surface((50, 40))
        surf.fill(RED if "alien" in name else GREEN if "player" in name else BLUE)
        return surf

# Try to load images, fall back to colored rectangles
try:
    player_img = load_image("player.png", 0.5)
    alien_img = load_image("alien.png", 0.5)
    bullet_img = load_image("bullet.png", 0.5)
    alien_bullet_img = load_image("alien_bullet.png", 0.5)
except:
    player_img = pygame.Surface((50, 40))
    player_img.fill(GREEN)
    alien_img = pygame.Surface((40, 30))
    alien_img.fill(RED)
    bullet_img = pygame.Surface((5, 15))
    bullet_img.fill(WHITE)
    alien_bullet_img = pygame.Surface((5, 15))
    alien_bullet_img.fill((255, 255, 0))  # Yellow bullets for aliens

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = WINDOW_WIDTH // 2
        self.rect.bottom = WINDOW_HEIGHT - 10
        self.speed = PLAYER_SPEED
        self.lives = 3
        self.score = 0
        
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.right < WINDOW_WIDTH:
            self.rect.x += self.speed
            
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        player_bullets.add(bullet)
        return bullet

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 1
        self.speed = ALIEN_SPEED
        
    def update(self):
        self.rect.x += self.speed * self.direction
        
    def shoot(self):
        bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
        all_sprites.add(bullet)
        alien_bullets.add(bullet)
        return bullet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -BULLET_SPEED
        
    def update(self):
        self.rect.y += self.speed
        # Kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = alien_bullet_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = BULLET_SPEED
        
    def update(self):
        self.rect.y += self.speed
        # Kill if it moves off the bottom of the screen
        if self.rect.top > WINDOW_HEIGHT:
            self.kill()

def create_aliens():
    aliens = pygame.sprite.Group()
    for row in range(4):
        for col in range(10):
            alien = Alien(100 + col * 60, 50 + row * 50)
            aliens.add(alien)
            all_sprites.add(alien)
    return aliens

def draw_text(surface, text, size, x, y):
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def show_game_over_screen():
    window.fill(BLACK)
    draw_text(window, "SPACE INVADERS", 64, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 4)
    draw_text(window, f"Final Score: {player.score}", 36, WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
    draw_text(window, "Press any key to play again", 24, WINDOW_WIDTH // 2, WINDOW_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP:
                waiting = False

# Initialize sprite groups
all_sprites = pygame.sprite.Group()
player_bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()
aliens = create_aliens()
player = Player()
all_sprites.add(player)
alien_direction = 1
alien_speed_increase = 0

# Game loop
game_over = False
running = True
while running:
    if game_over:
        show_game_over_screen()
        game_over = False
        # Reset game
        all_sprites = pygame.sprite.Group()
        player_bullets = pygame.sprite.Group()
        alien_bullets = pygame.sprite.Group()
        aliens = create_aliens()
        player = Player()
        all_sprites.add(player)
        alien_direction = 1
        alien_speed_increase = 0
    
    # Keep loop running at the right speed
    clock.tick(FPS)
    
    # Process input (events)
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.shoot()
    
    # Update
    all_sprites.update()
    
    # Check if aliens hit the edge
    move_down = False
    for alien in aliens:
        if alien.rect.right >= WINDOW_WIDTH:
            alien_direction = -1
            move_down = True
        elif alien.rect.left <= 0:
            alien_direction = 1
            move_down = True
    
    if move_down:
        for alien in aliens:
            alien.rect.y += ALIEN_DROP
            alien.direction = alien_direction
            alien.speed = ALIEN_SPEED + alien_speed_increase
    
    # Random alien shooting
    if random.random() < ALIEN_FIRE_RATE and len(aliens) > 0:
        shooter = random.choice(list(aliens.sprites()))
        shooter.shoot()
    
    # Check for bullet-alien collisions
    hits = pygame.sprite.groupcollide(aliens, player_bullets, True, True)
    for hit in hits:
        player.score += 10
        alien_speed_increase += 0.1  # Game gets slightly harder as aliens are eliminated
    
    # Check for bullet-player collisions
    hits = pygame.sprite.spritecollide(player, alien_bullets, True)
    for hit in hits:
        player.lives -= 1
        if player.lives <= 0:
            game_over = True
    
    # Check for alien-player collisions
    hits = pygame.sprite.spritecollide(player, aliens, False)
    if hits:
        game_over = True
    
    # Check if aliens reached the bottom
    for alien in aliens:
        if alien.rect.bottom >= WINDOW_HEIGHT:
            game_over = True
            break
    
    # Check if all aliens are dead
    if len(aliens) == 0:
        # Level complete - spawn new aliens
        aliens = create_aliens()
        alien_speed_increase += 0.5  # Increase speed for next level
    
    # Draw / render
    window.fill(BLACK)
    all_sprites.draw(window)
    
    # Draw score and lives
    draw_text(window, f"Score: {player.score}", 18, WINDOW_WIDTH // 2, 10)
    draw_text(window, f"Lives: {player.lives}", 18, WINDOW_WIDTH - 50, 10)
    
    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
sys.exit()