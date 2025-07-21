import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Asteroids')

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Game variables
FPS = 60
clock = pygame.time.Clock()

class Ship:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.thrust = 0.1
        self.rotation_speed = 5
        self.radius = 20
        self.lives = 3
        self.invincible = 0
        self.shoot_cooldown = 0
        
    def update(self):
        # Apply friction
        self.velocity_x *= 0.98
        self.velocity_y *= 0.98
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Screen wrapping
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
            
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
    
    def rotate_left(self):
        self.angle -= self.rotation_speed
    
    def rotate_right(self):
        self.angle += self.rotation_speed
    
    def thrust_forward(self):
        angle_rad = math.radians(self.angle)
        self.velocity_x += math.sin(angle_rad) * self.thrust
        self.velocity_y -= math.cos(angle_rad) * self.thrust
    
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 15
            angle_rad = math.radians(self.angle)
            return Bullet(self.x, self.y, 
                          math.sin(angle_rad) * 10 + self.velocity_x, 
                          -math.cos(angle_rad) * 10 + self.velocity_y)
        return None
    
    def draw(self, screen):
        if self.invincible > 0 and pygame.time.get_ticks() % 200 < 100:
            return  # Blink when invincible
            
        angle_rad = math.radians(self.angle)
        points = [
            (self.x + math.sin(angle_rad) * self.radius, 
             self.y - math.cos(angle_rad) * self.radius),
            (self.x + math.sin(angle_rad + 2.1) * self.radius * 0.7, 
             self.y - math.cos(angle_rad + 2.1) * self.radius * 0.7),
            (self.x + math.sin(angle_rad - 2.1) * self.radius * 0.7, 
             self.y - math.cos(angle_rad - 2.1) * self.radius * 0.7)
        ]
        pygame.draw.polygon(screen, WHITE, points)
        
        # Draw thrust flame when moving forward
        keys = pygame.key.get_pressed()
        if keys[K_UP] or keys[K_w]:
            flame_points = [
                (self.x + math.sin(angle_rad + 3.14) * self.radius * 0.8, 
                 self.y - math.cos(angle_rad + 3.14) * self.radius * 0.8),
                (self.x + math.sin(angle_rad + 2.5) * self.radius * 0.5, 
                 self.y - math.cos(angle_rad + 2.5) * self.radius * 0.5),
                (self.x + math.sin(angle_rad - 2.5) * self.radius * 0.5, 
                 self.y - math.cos(angle_rad - 2.5) * self.radius * 0.5)
            ]
            pygame.draw.polygon(screen, RED, flame_points)

class Bullet:
    def __init__(self, x, y, velocity_x, velocity_y):
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.lifetime = 60  # Frames until bullet disappears
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.lifetime -= 1
        
        # Screen wrapping
        if self.x < 0:
            self.x = WIDTH
        elif self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        elif self.y > HEIGHT:
            self.y = 0
    
    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), 2)

class Asteroid:
    def __init__(self, x=None, y=None, size=3, velocity_x=None, velocity_y=None):
        self.size = size  # 3=large, 2=medium, 1=small
        self.radius = size * 15
        
        if x is None and y is None:
            # Spawn at edge of screen
            side = random.randint(0, 3)
            if side == 0:  # top
                self.x = random.randint(0, WIDTH)
                self.y = -self.radius
            elif side == 1:  # right
                self.x = WIDTH + self.radius
                self.y = random.randint(0, HEIGHT)
            elif side == 2:  # bottom
                self.x = random.randint(0, WIDTH)
                self.y = HEIGHT + self.radius
            else:  # left
                self.x = -self.radius
                self.y = random.randint(0, HEIGHT)
        else:
            self.x = x
            self.y = y
            
        if velocity_x is None and velocity_y is None:
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.5, 2.0)
            self.velocity_x = math.sin(angle) * speed
            self.velocity_y = math.cos(angle) * speed
        else:
            self.velocity_x = velocity_x
            self.velocity_y = velocity_y
            
        self.rotation = random.uniform(-2, 2)
        self.rotation_angle = 0
        self.points = []
        self.generate_shape()
    
    def generate_shape(self):
        num_points = random.randint(6, 12)
        self.points = []
        for i in range(num_points):
            angle = 2 * math.pi * i / num_points
            radius = self.radius * random.uniform(0.7, 1.3)
            self.points.append((math.sin(angle) * radius, math.cos(angle) * radius))
    
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rotation_angle += self.rotation
        
        # Screen wrapping
        if self.x < -self.radius:
            self.x = WIDTH + self.radius
        elif self.x > WIDTH + self.radius:
            self.x = -self.radius
        if self.y < -self.radius:
            self.y = HEIGHT + self.radius
        elif self.y > HEIGHT + self.radius:
            self.y = -self.radius
    
    def draw(self, screen):
        points = []
        for px, py in self.points:
            rotated_x = px * math.cos(self.rotation_angle) - py * math.sin(self.rotation_angle)
            rotated_y = px * math.sin(self.rotation_angle) + py * math.cos(self.rotation_angle)
            points.append((self.x + rotated_x, self.y + rotated_y))
        pygame.draw.polygon(screen, WHITE, points, 1)
    
    def split(self):
        if self.size > 1:
            new_asteroids = []
            for _ in range(2):
                angle = random.uniform(0, math.pi * 2)
                speed = random.uniform(1.0, 3.0)
                new_velocity_x = math.sin(angle) * speed
                new_velocity_y = math.cos(angle) * speed
                new_asteroids.append(Asteroid(self.x, self.y, self.size-1, 
                                             self.velocity_x + new_velocity_x, 
                                             self.velocity_y + new_velocity_y))
            return new_asteroids
        return []

class Game:
    def __init__(self):
        self.ship = Ship()
        self.bullets = []
        self.asteroids = []
        self.score = 0
        self.level = 1
        self.game_over = False
        self.spawn_asteroids()
        
    def spawn_asteroids(self):
        for _ in range(2 + self.level):
            self.asteroids.append(Asteroid())
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT] or keys[K_a]:
            self.ship.rotate_left()
        if keys[K_RIGHT] or keys[K_d]:
            self.ship.rotate_right()
        if keys[K_UP] or keys[K_w]:
            self.ship.thrust_forward()
    
    def update(self):
        if self.game_over:
            return
            
        self.ship.update()
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.lifetime <= 0:
                self.bullets.remove(bullet)
        
        # Update asteroids
        for asteroid in self.asteroids[:]:
            asteroid.update()
            
            # Check collision with bullets
            for bullet in self.bullets[:]:
                dx = asteroid.x - bullet.x
                dy = asteroid.y - bullet.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < asteroid.radius:
                    self.bullets.remove(bullet)
                    self.asteroids.remove(asteroid)
                    new_asteroids = asteroid.split()
                    self.asteroids.extend(new_asteroids)
                    
                    # Add score based on asteroid size
                    self.score += (4 - asteroid.size) * 10
                    break
            
            # Check collision with ship
            if self.ship.invincible == 0:
                dx = asteroid.x - self.ship.x
                dy = asteroid.y - self.ship.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < asteroid.radius + self.ship.radius:
                    self.ship.lives -= 1
                    self.ship.invincible = 120  # 2 seconds of invincibility
                    self.ship.x = WIDTH // 2
                    self.ship.y = HEIGHT // 2
                    self.ship.velocity_x = 0
                    self.ship.velocity_y = 0
                    
                    if self.ship.lives <= 0:
                        self.game_over = True
                    break
        
        # Level progression
        if len(self.asteroids) == 0:
            self.level += 1
            self.spawn_asteroids()
    
    def draw(self, screen):
        screen.fill(BLACK)
        
        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(screen)
        
        # Draw asteroids
        for asteroid in self.asteroids:
            asteroid.draw(screen)
        
        # Draw ship
        self.ship.draw(screen)
        
        # Draw UI
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        lives_text = font.render(f"Lives: {self.ship.lives}", True, WHITE)
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (10, 90))
        
        if self.game_over:
            game_over_font = pygame.font.SysFont(None, 72)
            game_over_text = game_over_font.render("GAME OVER", True, WHITE)
            restart_text = font.render("Press R to restart", True, WHITE)
            
            screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, 
                                        HEIGHT//2 - game_over_text.get_height()//2))
            screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, 
                                      HEIGHT//2 + 50))

def main():
    game = Game()
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    bullet = game.ship.shoot()
                    if bullet:
                        game.bullets.append(bullet)
                elif event.key == K_r and game.game_over:
                    game = Game()  # Reset game
        
        game.handle_input()
        game.update()
        game.draw(screen)
        
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()