import pygame
import sys
import math
import random

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 800, 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHIP_COLOR = (0, 255, 255)
ASTEROID_COLOR = (200, 200, 200)
BULLET_COLOR = (255, 255, 0)
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Ship settings
SHIP_SIZE = 30
SHIP_SPEED = 0.25
SHIP_ROTATE_SPEED = 5
BULLET_SPEED = 8
BULLET_LIFETIME = 60

# Asteroid settings
ASTEROID_MIN_SIZE = 30
ASTEROID_MAX_SIZE = 60
ASTEROID_MIN_SPEED = 1
ASTEROID_MAX_SPEED = 3
ASTEROID_COUNT = 5

class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0
        self.alive = True
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.x %= WIDTH
        self.y %= HEIGHT
    def draw(self):
        points = []
        for i in range(3):
            theta = math.radians(self.angle + i * 120)
            px = self.x + SHIP_SIZE * math.cos(theta) / 2
            py = self.y + SHIP_SIZE * math.sin(theta) / 2
            points.append((px, py))
        pygame.draw.polygon(screen, SHIP_COLOR, points)
    def accelerate(self):
        rad = math.radians(self.angle)
        self.vel_x += SHIP_SPEED * math.cos(rad)
        self.vel_y += SHIP_SPEED * math.sin(rad)
    def rotate(self, direction):
        self.angle = (self.angle + SHIP_ROTATE_SPEED * direction) % 360

class Asteroid:
    def __init__(self, x=None, y=None, size=None):
        self.size = size if size else random.randint(ASTEROID_MIN_SIZE, ASTEROID_MAX_SIZE)
        self.x = x if x is not None else random.randint(0, WIDTH)
        self.y = y if y is not None else random.randint(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(ASTEROID_MIN_SPEED, ASTEROID_MAX_SPEED)
        self.vel_x = speed * math.cos(angle)
        self.vel_y = speed * math.sin(angle)
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.x %= WIDTH
        self.y %= HEIGHT
    def draw(self):
        pygame.draw.circle(screen, ASTEROID_COLOR, (int(self.x), int(self.y)), self.size)
    def collide(self, x, y):
        return math.hypot(self.x - x, self.y - y) < self.size

class Bullet:
    def __init__(self, x, y, angle):
        rad = math.radians(angle)
        self.x = x
        self.y = y
        self.vel_x = BULLET_SPEED * math.cos(rad)
        self.vel_y = BULLET_SPEED * math.sin(rad)
        self.life = BULLET_LIFETIME
    def update(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.x %= WIDTH
        self.y %= HEIGHT
        self.life -= 1
    def draw(self):
        pygame.draw.circle(screen, BULLET_COLOR, (int(self.x), int(self.y)), 3)

def main():
    ship = Ship()
    asteroids = [Asteroid() for _ in range(ASTEROID_COUNT)]
    bullets = []
    running = True
    game_over = False
    score = 0
    lives = 3
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_SPACE:
                    bullets.append(Bullet(ship.x, ship.y, ship.angle))
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()
                    return
        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                ship.rotate(-1)
            if keys[pygame.K_RIGHT]:
                ship.rotate(1)
            if keys[pygame.K_UP]:
                ship.accelerate()
            ship.update()
            for bullet in bullets[:]:
                bullet.update()
                if bullet.life <= 0:
                    bullets.remove(bullet)
            for asteroid in asteroids:
                asteroid.update()
            # Bullet-asteroid collision
            for bullet in bullets[:]:
                for asteroid in asteroids[:]:
                    if asteroid.collide(bullet.x, bullet.y):
                        bullets.remove(bullet)
                        asteroids.remove(asteroid)
                        score += 10
                        # Split asteroid if large enough
                        if asteroid.size > ASTEROID_MIN_SIZE + 10:
                            for _ in range(2):
                                asteroids.append(Asteroid(x=asteroid.x, y=asteroid.y, size=asteroid.size // 2))
                        break
            # Ship-asteroid collision
            for asteroid in asteroids[:]:
                if asteroid.collide(ship.x, ship.y):
                    lives -= 1
                    if lives <= 0:
                        ship.alive = False
                        game_over = True
                    else:
                        # Reset ship position and velocity
                        ship.x = WIDTH // 2
                        ship.y = HEIGHT // 2
                        ship.vel_x = 0
                        ship.vel_y = 0
                    break
            # Win condition
            if not asteroids:
                game_over = True
        screen.fill(BLACK)
        if ship.alive:
            ship.draw()
        for asteroid in asteroids:
            asteroid.draw()
        for bullet in bullets:
            bullet.draw()
        # Draw score and lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (20, 20))
        screen.blit(lives_text, (20, 60))
        if game_over:
            if ship.alive:
                msg = font.render("You Win! Press R to Restart", True, WHITE)
            else:
                msg = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
