import pygame
import sys
import math
import random

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asteroids')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Ship settings
SHIP_SIZE = 30
SHIP_SPEED = 5
SHIP_ROTATE_SPEED = 5
BULLET_SPEED = 10
BULLET_LIFETIME = 60

# Asteroid settings
ASTEROID_MIN_SIZE = 20
ASTEROID_MAX_SIZE = 50
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 3
ASTEROID_COUNT = 5

# Fonts
FONT = pygame.font.SysFont('Arial', 36)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 64)

# Helper functions
def wrap_position(pos):
    x, y = pos
    return x % WIDTH, y % HEIGHT

def angle_to_vector(angle):
    rad = math.radians(angle)
    return math.cos(rad), -math.sin(rad)

# Ship class
class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        self.lives = 3
        self.respawn()

    def respawn(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        self.invincible = 120  # frames

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += SHIP_ROTATE_SPEED
        if keys[pygame.K_RIGHT]:
            self.angle -= SHIP_ROTATE_SPEED
        if keys[pygame.K_UP]:
            vec = angle_to_vector(self.angle)
            self.vel_x += vec[0] * 0.2
            self.vel_y += vec[1] * 0.2
        self.x += self.vel_x
        self.y += self.vel_y
        self.x, self.y = wrap_position((self.x, self.y))
        self.vel_x *= 0.99
        self.vel_y *= 0.99
        if self.invincible > 0:
            self.invincible -= 1

    def draw(self, surface):
        # Draw triangle for ship
        points = []
        for i in range(3):
            angle = self.angle + i * 120
            vec = angle_to_vector(angle)
            px = self.x + vec[0] * SHIP_SIZE // 2
            py = self.y + vec[1] * SHIP_SIZE // 2
            points.append((px, py))
        color = WHITE if self.invincible % 20 < 10 else (100, 100, 100) if self.invincible > 0 else WHITE
        pygame.draw.polygon(surface, color, points)

    def get_position(self):
        return self.x, self.y

    def get_radius(self):
        return SHIP_SIZE // 2

# Bullet class
class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        vec = angle_to_vector(angle)
        self.vel_x = vec[0] * BULLET_SPEED
        self.vel_y = vec[1] * BULLET_SPEED
        self.lifetime = BULLET_LIFETIME

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.x, self.y = wrap_position((self.x, self.y))
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), 3)

    def is_alive(self):
        return self.lifetime > 0

    def get_position(self):
        return self.x, self.y

    def get_radius(self):
        return 3

# Asteroid class
class Asteroid:
    def __init__(self, x=None, y=None, size=None):
        self.size = size or random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        angle = random.uniform(0, 360)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        vec = angle_to_vector(angle)
        self.vel_x = vec[0] * speed
        self.vel_y = vec[1] * speed

    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.x, self.y = wrap_position((self.x, self.y))

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.size)

    def get_position(self):
        return self.x, self.y

    def get_radius(self):
        return self.size

# Collision detection
def collide(obj1, obj2):
    dx = obj1.get_position()[0] - obj2.get_position()[0]
    dy = obj1.get_position()[1] - obj2.get_position()[1]
    distance = math.hypot(dx, dy)
    return distance < (obj1.get_radius() + obj2.get_radius())

# Game loop
clock = pygame.time.Clock()
ship = Ship()
bullets = []
asteroids = [Asteroid() for _ in range(ASTEROID_COUNT)]
score = 0
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                # Fire bullet
                bullets.append(Bullet(ship.x, ship.y, ship.angle))

    if not game_over:
        keys = pygame.key.get_pressed()
        ship.update(keys)
        for bullet in bullets:
            bullet.update()
        for asteroid in asteroids:
            asteroid.update()
        # Remove dead bullets
        bullets = [b for b in bullets if b.is_alive()]
        # Bullet-asteroid collisions
        new_asteroids = []
        for bullet in bullets:
            for asteroid in asteroids:
                if collide(bullet, asteroid):
                    bullets.remove(bullet)
                    score += 10
                    if asteroid.size > ASTEROID_MIN_SIZE + 10:
                        # Split asteroid
                        for _ in range(2):
                            new_asteroids.append(Asteroid(asteroid.x, asteroid.y, asteroid.size // 2))
                    asteroids.remove(asteroid)
                    break
        asteroids.extend(new_asteroids)
        # Ship-asteroid collisions
        if ship.invincible == 0:
            for asteroid in asteroids:
                if collide(ship, asteroid):
                    ship.lives -= 1
                    ship.respawn()
                    if ship.lives <= 0:
                        game_over = True
        # Respawn asteroids if all destroyed
        if not asteroids:
            asteroids = [Asteroid() for _ in range(ASTEROID_COUNT)]

    # Draw everything
    SCREEN.fill(BLACK)
    ship.draw(SCREEN)
    for bullet in bullets:
        bullet.draw(SCREEN)
    for asteroid in asteroids:
        asteroid.draw(SCREEN)
    # Draw score and lives
    score_text = FONT.render(f'Score: {score}', True, WHITE)
    lives_text = FONT.render(f'Lives: {ship.lives}', True, WHITE)
    SCREEN.blit(score_text, (20, 20))
    SCREEN.blit(lives_text, (20, 60))
    # Draw game over
    if game_over:
        over_text = GAME_OVER_FONT.render('Game Over!', True, WHITE)
        SCREEN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 40))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit() 