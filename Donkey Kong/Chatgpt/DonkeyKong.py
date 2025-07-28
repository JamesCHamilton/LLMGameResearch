import pygame
import random

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong Clone")

# Colors
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 40))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = HEIGHT - 60
        self.velocity_y = 0
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 4
        if keys[pygame.K_RIGHT]:
            self.rect.x += 4
        if keys[pygame.K_SPACE] and self.on_ground:
            self.velocity_y = -12
            self.on_ground = False

        # Gravity
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Collision with platforms
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.on_ground = True

# Platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(BROWN)
        self.rect = self.image.get_rect(topleft=(x, y))

# Barrel class
class Barrel(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.direction = direction
        self.velocity_y = 0

    def update(self, platforms):
        self.rect.x += self.direction * 3
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        for platform in platforms:
            if self.rect.colliderect(platform.rect) and self.velocity_y >= 0:
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.direction *= -1  # Change direction on collision

# Goal
goal = pygame.Rect(WIDTH - 60, 100, 40, 40)

# Create game objects
player = Player()
platforms = pygame.sprite.Group()
barrels = pygame.sprite.Group()

# Static platform layout
platform_layout = [
    (0, HEIGHT - 20, WIDTH, 20),
    (0, 500, 600, 20),
    (200, 400, 600, 20),
    (0, 300, 600, 20),
    (200, 200, 600, 20),
    (0, 100, 600, 20),
]

for plat in platform_layout:
    p = Platform(*plat)
    platforms.add(p)

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(platforms)

# Main loop
running = True
barrel_timer = 0

while running:
    clock.tick(60)
    screen.fill(WHITE)

    # Spawn barrels every 2 seconds
    barrel_timer += 1
    if barrel_timer > 120:
        b = Barrel(50, 80, random.choice([-1, 1]))
        barrels.add(b)
        all_sprites.add(b)
        barrel_timer = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(platforms)
    for barrel in barrels:
        barrel.update(platforms)

    # Check for collision with barrels
    if pygame.sprite.spritecollideany(player, barrels):
        print("Game Over!")
        running = False

    # Check if player reaches goal
    if player.rect.colliderect(goal):
        print("You Win!")
        running = False

    # Draw everything
    all_sprites.draw(screen)
    pygame.draw.rect(screen, BLACK, goal)

    pygame.display.flip()

pygame.quit()
