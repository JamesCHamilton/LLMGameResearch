import pygame
import random
import math

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# --- Game Initialization ---
pygame.init()
pygame.mixer.init() # For sounds, if we add them later
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 24)

# --- Helper Functions ---
def wrap_position(pos, screen_dim):
    """Wraps a position vector around the screen."""
    if pos.x > screen_dim[0]:
        pos.x = 0
    if pos.x < 0:
        pos.x = screen_dim[0]
    if pos.y > screen_dim[1]:
        pos.y = 0
    if pos.y < 0:
        pos.y = screen_dim[1]
    return pos

def draw_text(surf, text, size, x, y, color):
    """Draws text on the screen."""
    font_obj = pygame.font.Font(pygame.font.match_font('arial'), size)
    text_surface = font_obj.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

# --- Game Classes ---

class Player(pygame.sprite.Sprite):
    """Represents the player's spaceship."""
    def __init__(self):
        super().__init__()
        self.original_image = pygame.Surface((25, 20), pygame.SRCALPHA)
        pygame.draw.polygon(self.original_image, WHITE, [(0, 20), (12.5, 0), (25, 20)])
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.vel = pygame.math.Vector2(0, 0)
        self.angle = 0
        self.rotation_speed = 4.5
        self.acceleration = 0.25
        self.friction = 0.99 # A value slightly less than 1 to slow down over time
        self.max_speed = 7
        self.radius = 10 # For collision detection

    def rotate(self, direction):
        """Rotate the ship. Direction is 1 for right, -1 for left."""
        self.angle += self.rotation_speed * direction
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        
        # Update the image to reflect rotation
        self.image = pygame.transform.rotate(self.original_image, -self.angle) # Negative angle for correct rotation
        self.rect = self.image.get_rect(center=self.pos)

    def thrust(self):
        """Apply forward thrust."""
        rad_angle = math.radians(self.angle)
        acceleration_vector = pygame.math.Vector2(math.sin(rad_angle), -math.cos(rad_angle)) * self.acceleration
        self.vel += acceleration_vector
        
        # Cap the speed
        if self.vel.length() > self.max_speed:
            self.vel.scale_to_length(self.max_speed)

    def shoot(self):
        """Creates a new bullet instance."""
        rad_angle = math.radians(self.angle)
        # Calculate the spawn position at the tip of the ship
        spawn_offset = pygame.math.Vector2(math.sin(rad_angle), -math.cos(rad_angle)) * 20
        bullet_pos = self.pos + spawn_offset
        return Bullet(bullet_pos, self.angle)

    def update(self):
        """Update player position and apply friction."""
        self.vel *= self.friction
        self.pos += self.vel
        self.pos = wrap_position(self.pos, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.rect.center = self.pos

class Bullet(pygame.sprite.Sprite):
    """Represents a bullet fired by the player."""
    def __init__(self, pos, angle):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=pos)
        self.pos = pygame.math.Vector2(pos)
        self.speed = 10
        rad_angle = math.radians(angle)
        self.vel = pygame.math.Vector2(math.sin(rad_angle), -math.cos(rad_angle)) * self.speed
        self.lifespan = 60 # Frames before disappearing
        self.age = 0

    def update(self):
        """Move the bullet and handle its lifespan."""
        self.pos += self.vel
        self.rect.center = self.pos
        self.age += 1
        if self.age > self.lifespan:
            self.kill() # Remove the sprite from all groups
        
        # Screen wrapping for bullets
        if not (0 <= self.rect.centerx <= SCREEN_WIDTH and 0 <= self.rect.centery <= SCREEN_HEIGHT):
            self.kill()


class Asteroid(pygame.sprite.Sprite):
    """Represents an asteroid."""
    def __init__(self, size, position=None):
        super().__init__()
        self.size = size # 3 = large, 2 = medium, 1 = small
        self.size_map = {3: 40, 2: 20, 1: 10}
        self.radius = self.size_map[self.size]
        
        # Create an irregular polygon shape
        self.points = []
        num_points = random.randint(7, 12)
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi
            dist = random.uniform(self.radius * 0.7, self.radius * 1.3)
            self.points.append((math.cos(angle) * dist, math.sin(angle) * dist))
            
        # Create the image and rect
        self.image = pygame.Surface((self.radius * 2.6, self.radius * 2.6), pygame.SRCALPHA)
        poly_points = [(p[0] + self.radius * 1.3, p[1] + self.radius * 1.3) for p in self.points]
        pygame.draw.polygon(self.image, WHITE, poly_points, 2)
        self.original_image = self.image
        self.rect = self.image.get_rect()
        
        # Position and velocity
        if position:
            self.pos = pygame.math.Vector2(position)
        else:
            # Spawn at an edge
            edge = random.choice(['top', 'bottom', 'left', 'right'])
            if edge == 'top': self.pos = pygame.math.Vector2(random.randint(0, SCREEN_WIDTH), -self.radius)
            if edge == 'bottom': self.pos = pygame.math.Vector2(random.randint(0, SCREEN_WIDTH), SCREEN_HEIGHT + self.radius)
            if edge == 'left': self.pos = pygame.math.Vector2(-self.radius, random.randint(0, SCREEN_HEIGHT))
            if edge == 'right': self.pos = pygame.math.Vector2(SCREEN_WIDTH + self.radius, random.randint(0, SCREEN_HEIGHT))

        self.vel = pygame.math.Vector2(random.uniform(-1.5, 1.5), random.uniform(-1.5, 1.5))
        self.rect.center = self.pos
        
        # Rotation
        self.angle = 0
        self.rot_speed = random.uniform(-1, 1)

    def update(self):
        """Move and rotate the asteroid."""
        self.pos += self.vel
        self.pos = wrap_position(self.pos, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        self.angle += self.rot_speed
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.pos)
        
    def break_apart(self):
        """Break into smaller asteroids."""
        if self.size > 1:
            new_asteroids = []
            for _ in range(2): # Create two smaller asteroids
                new_asteroids.append(Asteroid(self.size - 1, self.pos))
            return new_asteroids
        return []

# --- Game Setup ---
def game_loop():
    # Sprite groups
    all_sprites = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Initial asteroid spawn
    for _ in range(5):
        a = Asteroid(3)
        all_sprites.add(a)
        asteroids.add(a)

    score = 0
    lives = 3
    game_over = False
    running = True

    # --- Main Game Loop ---
    while running:
        # Keep loop running at the right speed
        clock.tick(60)

        # Process input (events)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bullet = player.shoot()
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                if event.key == pygame.K_r and game_over:
                    # Restart the game
                    game_loop()


        if not game_over:
            # Handle continuous key presses for movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player.rotate(-1)
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player.rotate(1)
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player.thrust()

            # Update
            all_sprites.update()

            # --- Collision Detection ---
            # Bullets hitting asteroids
            hits = pygame.sprite.groupcollide(asteroids, bullets, True, True, pygame.sprite.collide_circle)
            for hit_asteroid in hits:
                score += 10 * (4 - hit_asteroid.size) # More points for smaller asteroids
                new_asteroids = hit_asteroid.break_apart()
                for new_a in new_asteroids:
                    all_sprites.add(new_a)
                    asteroids.add(new_a)
            
            # If all asteroids are destroyed, spawn a new wave
            if not asteroids:
                for _ in range(5):
                    a = Asteroid(3)
                    all_sprites.add(a)
                    asteroids.add(a)

            # Player hitting asteroids
            player_hits = pygame.sprite.spritecollide(player, asteroids, True, pygame.sprite.collide_circle)
            if player_hits:
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Respawn player in center, temporary invulnerability could be added here
                    player.pos = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
                    player.vel = pygame.math.Vector2(0, 0)
                    player.angle = 0


        # Draw / Render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        
        # Draw UI
        draw_text(screen, f"Score: {score}", 24, SCREEN_WIDTH / 2, 10, WHITE)
        draw_text(screen, f"Lives: {lives}", 24, 60, 10, WHITE)

        if game_over:
            draw_text(screen, "GAME OVER", 64, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3, RED)
            draw_text(screen, "Press 'R' to Restart", 22, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, WHITE)

        # After drawing everything, flip the display
        pygame.display.flip()

    pygame.quit()

# --- Start the game ---
if __name__ == "__main__":
    game_loop()
