import pygame
import random
import math
import sys

# Initialize PyGame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroids")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 50, 230)

# Game variables
FPS = 60
score = 0
lives = 3
level = 1
game_over = False
game_started = False

# Fonts
font_large = pygame.font.SysFont(None, 72)
font_medium = pygame.font.SysFont(None, 48)
font_small = pygame.font.SysFont(None, 36)

class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.velocity_x = 0
        self.velocity_y = 0
        self.acceleration = 0.1
        self.rotation_speed = 5
        self.size = 20
        self.shoot_cooldown = 0
        self.invincible = 0
        self.thrust = False
        
    def update(self):
        # Apply friction
        self.velocity_x *= 0.98
        self.velocity_y *= 0.98
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Screen wrapping
        if self.x < -self.size:
            self.x = WIDTH + self.size
        elif self.x > WIDTH + self.size:
            self.x = -self.size
        if self.y < -self.size:
            self.y = HEIGHT + self.size
        elif self.y > HEIGHT + self.size:
            self.y = -self.size
            
        # Update cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.invincible > 0:
            self.invincible -= 1
            
        # Apply thrust if active
        if self.thrust:
            rad_angle = math.radians(self.angle)
            self.velocity_x += math.sin(rad_angle) * self.acceleration
            self.velocity_y -= math.cos(rad_angle) * self.acceleration
            
    def rotate(self, direction):
        self.angle += direction * self.rotation_speed
        self.angle %= 360
        
    def draw(self, screen):
        if self.invincible > 0 and self.invincible % 10 < 5:
            return  # Flashing effect when invincible
            
        rad_angle = math.radians(self.angle)
        
        # Ship points
        points = [
            (self.x + math.sin(rad_angle) * self.size, 
             self.y - math.cos(rad_angle) * self.size),
            (self.x + math.sin(rad_angle + 2.5) * self.size * 0.7, 
             self.y - math.cos(rad_angle + 2.5) * self.size * 0.7),
            (self.x + math.sin(rad_angle + math.pi) * self.size * 0.8, 
             self.y - math.cos(rad_angle + math.pi) * self.size * 0.8),
            (self.x + math.sin(rad_angle - 2.5) * self.size * 0.7, 
             self.y - math.cos(rad_angle - 2.5) * self.size * 0.7)
        ]
        
        pygame.draw.polygon(screen, BLUE, points)
        
        # Draw thrust flame
        if self.thrust:
            flame_points = [
                (self.x + math.sin(rad_angle + math.pi) * self.size * 0.8, 
                 self.y - math.cos(rad_angle + math.pi) * self.size * 0.8),
                (self.x + math.sin(rad_angle + math.pi + 0.3) * self.size * 1.4, 
                 self.y - math.cos(rad_angle + math.pi + 0.3) * self.size * 1.4),
                (self.x + math.sin(rad_angle + math.pi - 0.3) * self.size * 1.4, 
                 self.y - math.cos(rad_angle + math.pi - 0.3) * self.size * 1.4)
            ]
            pygame.draw.polygon(screen, YELLOW, flame_points)
        
    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 15
            rad_angle = math.radians(self.angle)
            bullet_x = self.x + math.sin(rad_angle) * self.size
            bullet_y = self.y - math.cos(rad_angle) * self.size
            bullet_vx = self.velocity_x + math.sin(rad_angle) * 7
            bullet_vy = self.velocity_y - math.cos(rad_angle) * 7
            return Bullet(bullet_x, bullet_y, bullet_vx, bullet_vy)
        return None

class Asteroid:
    def __init__(self, x=None, y=None, size=3):
        self.size = size  # 3 = large, 2 = medium, 1 = small
        self.radius = self.size * 15
        
        if x is None or y is None:
            # Spawn from edge of screen
            side = random.randint(0, 3)
            if side == 0:  # Top
                self.x = random.randint(0, WIDTH)
                self.y = -self.radius
            elif side == 1:  # Right
                self.x = WIDTH + self.radius
                self.y = random.randint(0, HEIGHT)
            elif side == 2:  # Bottom
                self.x = random.randint(0, WIDTH)
                self.y = HEIGHT + self.radius
            else:  # Left
                self.x = -self.radius
                self.y = random.randint(0, HEIGHT)
        else:
            self.x = x
            self.y = y
            
        # Random direction and speed
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1.0, 3.0) / self.size
        self.velocity_x = math.sin(angle) * speed
        self.velocity_y = math.cos(angle) * speed
        
        # Rotation
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-2, 2)
        
        # Create irregular shape
        self.points = []
        for i in range(8):
            angle = 2 * math.pi * i / 8
            distance = self.radius * random.uniform(0.7, 1.3)
            self.points.append((math.sin(angle) * distance, math.cos(angle) * distance))
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rotation += self.rotation_speed
        
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
        # Draw asteroid
        points = []
        for px, py in self.points:
            rad_angle = math.radians(self.rotation)
            x = self.x + px * math.cos(rad_angle) - py * math.sin(rad_angle)
            y = self.y + px * math.sin(rad_angle) + py * math.cos(rad_angle)
            points.append((x, y))
            
        color = WHITE
        if self.size == 3:
            color = (200, 200, 200)  # Large asteroids are lighter
        elif self.size == 2:
            color = (150, 150, 150)  # Medium
        else:
            color = (100, 100, 100)  # Small
            
        pygame.draw.polygon(screen, color, points, 2)
        
    def break_apart(self):
        if self.size > 1:
            return [Asteroid(self.x, self.y, self.size-1) for _ in range(2)]
        return []

class Bullet:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.velocity_x = vx
        self.velocity_y = vy
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
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 3)

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.lifetime = random.randint(20, 40)
        self.size = random.randint(2, 4)
        
    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.size = max(0, self.size - 0.05)
        
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2)
        self.speed = random.uniform(0.2, 0.8)
        self.brightness = random.randint(150, 255)
        
    def update(self):
        self.x -= self.speed
        if self.x < 0:
            self.x = WIDTH
            self.y = random.randint(0, HEIGHT)
            
    def draw(self, screen):
        color = (self.brightness, self.brightness, self.brightness)
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)

# Create game objects
player = Player()
asteroids = []
bullets = []
particles = []
stars = [Star() for _ in range(100)]

# Create initial asteroids
for _ in range(5):
    asteroids.append(Asteroid())

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_r and game_over:
                # Reset game
                player = Player()
                asteroids = [Asteroid() for _ in range(5)]
                bullets = []
                particles = []
                score = 0
                lives = 3
                level = 1
                game_over = False
            elif event.key == pygame.K_SPACE and not game_over:
                if not game_started:
                    game_started = True
                else:
                    new_bullet = player.shoot()
                    if new_bullet:
                        bullets.append(new_bullet)
    
    if not game_over and game_started:
        # Player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.rotate(-1)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.rotate(1)
        player.thrust = keys[pygame.K_UP] or keys[pygame.K_w]
        
        # Shooting with spacebar (continuous)
        if keys[pygame.K_SPACE]:
            new_bullet = player.shoot()
            if new_bullet:
                bullets.append(new_bullet)
        
        # Update game objects
        player.update()
        
        for asteroid in asteroids[:]:
            asteroid.update()
            
            # Collision with player
            if player.invincible == 0:
                dx = player.x - asteroid.x
                dy = player.y - asteroid.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < player.size + asteroid.radius:
                    # Player hit
                    player.invincible = 120  # 2 seconds of invincibility
                    lives -= 1
                    if lives <= 0:
                        game_over = True
                    
                    # Create explosion particles
                    for _ in range(30):
                        particles.append(Particle(player.x, player.y, RED))
        
        for bullet in bullets[:]:
            bullet.update()
            if bullet.lifetime <= 0:
                bullets.remove(bullet)
                continue
                
            # Check collision with asteroids
            for asteroid in asteroids[:]:
                dx = bullet.x - asteroid.x
                dy = bullet.y - asteroid.y
                distance = math.sqrt(dx*dx + dy*dy)
                if distance < asteroid.radius:
                    # Asteroid hit
                    asteroids.remove(asteroid)
                    bullets.remove(bullet)
                    
                    # Create explosion particles
                    for _ in range(20):
                        particles.append(Particle(asteroid.x, asteroid.y, WHITE))
                    
                    # Break asteroid apart
                    new_asteroids = asteroid.break_apart()
                    asteroids.extend(new_asteroids)
                    
                    # Update score
                    score += 100 // asteroid.size
                    
                    break
        
        # Add new asteroids if none left
        if len(asteroids) == 0:
            level += 1
            for _ in range(3 + level):
                asteroids.append(Asteroid())
        
        # Update particles
        for particle in particles[:]:
            particle.update()
            if particle.lifetime <= 0:
                particles.remove(particle)
        
        # Update stars
        for star in stars:
            star.update()
    
    # Drawing
    screen.fill(BLACK)
    
    # Draw stars
    for star in stars:
        star.draw(screen)
    
    # Draw particles
    for particle in particles:
        particle.draw(screen)
    
    # Draw asteroids
    for asteroid in asteroids:
        asteroid.draw(screen)
    
    # Draw bullets
    for bullet in bullets:
        bullet.draw(screen)
    
    # Draw player
    player.draw(screen)
    
    # Draw UI
    score_text = font_small.render(f"Score: {score}", True, GREEN)
    lives_text = font_small.render(f"Lives: {lives}", True, RED)
    level_text = font_small.render(f"Level: {level}", True, BLUE)
    
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (10, 50))
    screen.blit(level_text, (10, 90))
    
    # Draw game over screen
    if game_over:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        game_over_text = font_large.render("GAME OVER", True, RED)
        score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
        restart_text = font_small.render("Press 'R' to Restart or ESC to Quit", True, YELLOW)
        
        screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 80))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 80))
    
    # Draw start screen
    if not game_started:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        title_text = font_large.render("ASTEROIDS", True, BLUE)
        controls_text = font_small.render("Controls: Arrow Keys to Move, Space to Shoot", True, WHITE)
        start_text = font_medium.render("Press SPACE to Start", True, GREEN)
        
        screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, HEIGHT//2 - 100))
        screen.blit(controls_text, (WIDTH//2 - controls_text.get_width()//2, HEIGHT//2))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 80))
    
    # Draw border
    pygame.draw.rect(screen, PURPLE, (0, 0, WIDTH, HEIGHT), 3)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()