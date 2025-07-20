import pygame
import math
import random
import sys

# Initialize
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Helper functions
def wrap_position(pos):
    x, y = pos
    return [x % WIDTH, y % HEIGHT]

def angle_to_vector(angle):
    rad = math.radians(angle)
    return math.cos(rad), math.sin(rad)

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# Ship class
class Ship:
    def __init__(self):
        self.position = [WIDTH / 2, HEIGHT / 2]
        self.velocity = [0, 0]
        self.angle = 0
        self.thrust = False
        self.radius = 15
        self.invincible_timer = 0

    def draw(self):
        ang = math.radians(self.angle)
        tip = (self.position[0] + math.cos(ang) * self.radius,
               self.position[1] + math.sin(ang) * self.radius)
        left = (self.position[0] + math.cos(ang + 2.5) * self.radius,
                self.position[1] + math.sin(ang + 2.5) * self.radius)
        right = (self.position[0] + math.cos(ang - 2.5) * self.radius,
                 self.position[1] + math.sin(ang - 2.5) * self.radius)

        if self.invincible_timer % 20 < 10:
            pygame.draw.polygon(screen, WHITE, [tip, left, right])

    def update(self):
        if self.thrust:
            forward = angle_to_vector(self.angle)
            self.velocity[0] += forward[0] * 0.1
            self.velocity[1] += forward[1] * 0.1

        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position = wrap_position(self.position)

        self.velocity[0] *= 0.99
        self.velocity[1] *= 0.99

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

    def reset(self):
        self.position = [WIDTH / 2, HEIGHT / 2]
        self.velocity = [0, 0]
        self.angle = 0
        self.invincible_timer = 120  # 2 seconds of invincibility

# Bullet class
class Bullet:
    def __init__(self, pos, angle):
        vec = angle_to_vector(angle)
        self.position = list(pos)
        self.velocity = [vec[0] * 6, vec[1] * 6]
        self.radius = 2
        self.lifespan = 60

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position = wrap_position(self.position)
        self.lifespan -= 1

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.position[0]), int(self.position[1])), self.radius)

# Asteroid class
class Asteroid:
    def __init__(self, pos=None, size=3):
        if pos:
            self.position = list(pos)
        else:
            self.position = [random.choice([0, WIDTH]), random.randint(0, HEIGHT)]
        self.velocity = [random.uniform(-2, 2), random.uniform(-2, 2)]
        self.angle = random.uniform(0, 360)
        self.size = size
        self.radius = 15 * size

    def update(self):
        self.position[0] += self.velocity[0]
        self.position[1] += self.velocity[1]
        self.position = wrap_position(self.position)

    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.position[0]), int(self.position[1])), self.radius, 1)

# Game state
ship = Ship()
bullets = []
asteroids = [Asteroid() for _ in range(5)]
score = 0
lives = 3
font = pygame.font.SysFont(None, 30)
game_over = False

# Main loop
running = True
while running:
    screen.fill(BLACK)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Controls
        if keys[pygame.K_LEFT]:
            ship.angle -= 5
        if keys[pygame.K_RIGHT]:
            ship.angle += 5
        ship.thrust = keys[pygame.K_UP]

        if keys[pygame.K_SPACE] and len(bullets) < 10:
            bullet = Bullet(ship.position[:], ship.angle)
            bullets.append(bullet)

        # Update
        ship.update()
        for bullet in bullets[:]:
            bullet.update()
            if bullet.lifespan <= 0:
                bullets.remove(bullet)

        for asteroid in asteroids[:]:
            asteroid.update()

            # Bullet collision
            for bullet in bullets[:]:
                if distance(bullet.position, asteroid.position) < asteroid.radius:
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10
                    if asteroid.size > 1:
                        for _ in range(2):
                            asteroids.append(Asteroid(asteroid.position, asteroid.size - 1))
                    break

            # Ship collision
            if ship.invincible_timer <= 0:
                if distance(ship.position, asteroid.position) < asteroid.radius + ship.radius:
                    lives -= 1
                    ship.reset()
                    if lives <= 0:
                        game_over = True

        # Draw
        ship.draw()
        for bullet in bullets:
            bullet.draw()
        for asteroid in asteroids:
            asteroid.draw()

        # HUD
        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 40))
    else:
        # Game Over screen
        over_text = font.render("GAME OVER", True, WHITE)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(over_text, (WIDTH // 2 - 60, HEIGHT // 2 - 20))
        screen.blit(score_text, (WIDTH // 2 - 70, HEIGHT // 2 + 10))

    # Refresh screen
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
