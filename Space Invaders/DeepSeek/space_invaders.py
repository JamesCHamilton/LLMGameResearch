import pygame
import sys
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Colors
BACKGROUND = (10, 10, 40)
PLAYER_COLOR = (70, 200, 255)
ENEMY_COLORS = [
    (220, 60, 60),    # Red
    (255, 140, 0),    # Orange
    (255, 215, 0),    # Yellow
    (50, 205, 50),    # Green
    (30, 144, 255),   # Blue
]
BULLET_COLOR = (255, 255, 200)
BARRIER_COLOR = (0, 180, 120)
TEXT_COLOR = (220, 220, 255)
EXPLOSION_COLOR = (255, 215, 0)
STAR_COLORS = [(200, 200, 255), (255, 255, 200), (200, 255, 200)]

# Game constants
PLAYER_SPEED = 6
ENEMY_ROWS = 5
ENEMY_COLS = 10
ENEMY_SPEED_X = 1
ENEMY_SPEED_Y = 30
BULLET_SPEED = 7
ENEMY_BULLET_SPEED = 5
BARRIER_COUNT = 4
BARRIER_WIDTH = 100
BARRIER_HEIGHT = 50
BARRIER_DAMAGE_COLOR = (180, 60, 40)

# Game state
class GameState:
    START = 0
    PLAYING = 1
    GAME_OVER = 2
    LEVEL_COMPLETE = 3

# Player class
class Player:
    def __init__(self):
        self.width = 50
        self.height = 40
        self.x = WIDTH // 2 - self.width // 2
        self.y = HEIGHT - 80
        self.speed = PLAYER_SPEED
        self.color = PLAYER_COLOR
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.bullets = []
        self.last_shot = 0
        self.shoot_delay = 500  # milliseconds
        self.lives = 3
        self.score = 0
        self.level = 1
    
    def draw(self):
        # Draw player ship
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y + 20, self.width, 20))
        pygame.draw.polygon(screen, self.color, [
            (self.rect.centerx, self.rect.y),
            (self.rect.x, self.rect.y + 30),
            (self.rect.right, self.rect.y + 30)
        ])
        
        # Draw cockpit
        pygame.draw.circle(screen, (180, 240, 255), (self.rect.centerx, self.rect.y + 15), 8)
    
    def move(self, direction):
        if direction == "left" and self.rect.left > 0:
            self.rect.x -= self.speed
        if direction == "right" and self.rect.right < WIDTH:
            self.rect.x += self.speed
    
    def shoot(self, current_time):
        if current_time - self.last_shot > self.shoot_delay:
            self.bullets.append(Bullet(self.rect.centerx, self.rect.y, -BULLET_SPEED, BULLET_COLOR))
            self.last_shot = current_time
            return True
        return False

# Enemy class
class Enemy:
    def __init__(self, x, y, enemy_type):
        self.width = 40
        self.height = 40
        self.x = x
        self.y = y
        self.type = enemy_type
        self.color = ENEMY_COLORS[enemy_type]
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.alive = True
        self.value = (5 - enemy_type) * 10  # Higher enemies worth more
    
    def draw(self):
        if not self.alive:
            return
            
        # Draw enemy body
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.width, self.height), border_radius=10)
        
        # Draw enemy eyes
        eye_size = 8
        pygame.draw.circle(screen, (30, 30, 50), (self.rect.centerx - 10, self.rect.centery - 5), eye_size)
        pygame.draw.circle(screen, (30, 30, 50), (self.rect.centerx + 10, self.rect.centery - 5), eye_size)
        pygame.draw.circle(screen, (200, 230, 255), (self.rect.centerx - 8, self.rect.centery - 7), eye_size//2)
        pygame.draw.circle(screen, (200, 230, 255), (self.rect.centerx + 8, self.rect.centery - 7), eye_size//2)
        
        # Draw enemy mouth
        pygame.draw.arc(screen, (30, 30, 50), 
                        (self.rect.centerx - 10, self.rect.centery + 5, 20, 10),
                        0, math.pi, 2)
    
    def update(self, direction):
        if direction == "right":
            self.rect.x += ENEMY_SPEED_X
        elif direction == "left":
            self.rect.x -= ENEMY_SPEED_X
        elif direction == "down":
            self.rect.y += ENEMY_SPEED_Y
    
    def shoot(self, bullets):
        if random.random() < 0.002:  # Random chance to shoot
            bullets.append(Bullet(self.rect.centerx, self.rect.bottom, ENEMY_BULLET_SPEED, self.color))

# Bullet class
class Bullet:
    def __init__(self, x, y, speed, color):
        self.width = 4
        self.height = 15
        self.x = x - self.width // 2
        self.y = y
        self.speed = speed
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect, border_radius=2)
        pygame.draw.rect(screen, (255, 255, 255), 
                        (self.rect.x, self.rect.y, self.width, 4), 
                        border_radius=2)

# Barrier class
class Barrier:
    def __init__(self, x, y):
        self.width = BARRIER_WIDTH
        self.height = BARRIER_HEIGHT
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, self.width, self.height)
        self.health = 100
    
    def draw(self):
        # Draw barrier with damage effect
        pygame.draw.rect(screen, BARRIER_COLOR, self.rect, border_radius=5)
        
        # Draw damage cracks
        if self.health < 75:
            pygame.draw.line(screen, BARRIER_DAMAGE_COLOR, 
                            (self.rect.x + 20, self.rect.y + 10),
                            (self.rect.x + 40, self.rect.y + 30), 2)
        if self.health < 50:
            pygame.draw.line(screen, BARRIER_DAMAGE_COLOR, 
                            (self.rect.x + 60, self.rect.y + 15),
                            (self.rect.x + 80, self.rect.y + 35), 2)
        if self.health < 25:
            pygame.draw.line(screen, BARRIER_DAMAGE_COLOR, 
                            (self.rect.centerx, self.rect.y + 5),
                            (self.rect.centerx, self.rect.y + 45), 3)

# Particle effect for explosions
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.randint(20, 40)
    
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 1
        self.size = max(0, self.size - 0.1)
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.size))

# Star background
class Star:
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        self.size = random.uniform(0.5, 2.5)
        self.color = random.choice(STAR_COLORS)
        self.speed = random.uniform(0.2, 0.8)
    
    def update(self):
        self.y += self.speed
        if self.y > HEIGHT:
            self.y = 0
            self.x = random.randint(0, WIDTH)
    
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.size)

# Game class
class SpaceInvaders:
    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.barriers = []
        self.enemy_bullets = []
        self.particles = []
        self.stars = []
        self.game_state = GameState.START
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 28)
        self.title_font = pygame.font.SysFont(None, 72)
        self.enemy_direction = "right"
        self.enemy_move_counter = 0
        self.enemy_move_delay = 30  # frames per move
        self.create_stars(100)
        self.create_barriers()
        self.reset_level()
    
    def create_stars(self, count):
        self.stars = [Star() for _ in range(count)]
    
    def create_barriers(self):
        spacing = WIDTH // (BARRIER_COUNT + 1)
        for i in range(BARRIER_COUNT):
            self.barriers.append(Barrier(spacing * (i+1) - BARRIER_WIDTH//2, HEIGHT - 150))
    
    def reset_level(self):
        self.enemies = []
        self.enemy_bullets = []
        self.player.bullets = []
        
        # Create enemies in grid pattern
        start_x = 100
        start_y = 80
        spacing_x = 60
        spacing_y = 50
        
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                enemy_type = min(row, len(ENEMY_COLORS)-1)
                self.enemies.append(Enemy(start_x + col * spacing_x, 
                                         start_y + row * spacing_y, 
                                         enemy_type))
        
        self.enemy_direction = "right"
        self.enemy_move_counter = 0
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if self.game_state == GameState.START:
                        self.game_state = GameState.PLAYING
                    elif self.game_state == GameState.PLAYING:
                        self.player.shoot(pygame.time.get_ticks())
                    elif self.game_state == GameState.GAME_OVER or self.game_state == GameState.LEVEL_COMPLETE:
                        self.__init__()  # Reset game
                
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    
    def update(self):
        if self.game_state != GameState.PLAYING:
            return
        
        # Move player with keyboard
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move("left")
        if keys[pygame.K_RIGHT]:
            self.player.move("right")
        if keys[pygame.K_SPACE]:
            self.player.shoot(pygame.time.get_ticks())
        
        # Update stars
        for star in self.stars:
            star.update()
        
        # Move enemies
        self.enemy_move_counter += 1
        if self.enemy_move_counter >= self.enemy_move_delay:
            self.enemy_move_counter = 0
            
            # Change direction if any enemy hits the edge
            change_direction = False
            for enemy in self.enemies:
                if enemy.alive:
                    if (self.enemy_direction == "right" and enemy.rect.right >= WIDTH - 10) or \
                       (self.enemy_direction == "left" and enemy.rect.left <= 10):
                        change_direction = True
                        break
            
            if change_direction:
                self.enemy_direction = "down"
                for enemy in self.enemies:
                    if enemy.alive:
                        enemy.update(self.enemy_direction)
                self.enemy_direction = "right" if self.enemy_direction == "left" else "left"
            else:
                for enemy in self.enemies:
                    if enemy.alive:
                        enemy.update(self.enemy_direction)
        
        # Update bullets
        for bullet in self.player.bullets[:]:
            bullet.update()
            if bullet.rect.bottom < 0:
                self.player.bullets.remove(bullet)
        
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.rect.top > HEIGHT:
                self.enemy_bullets.remove(bullet)
        
        # Enemy shooting
        for enemy in self.enemies:
            if enemy.alive:
                enemy.shoot(self.enemy_bullets)
        
        # Collision detection: Player bullets with enemies
        for bullet in self.player.bullets[:]:
            for enemy in self.enemies:
                if enemy.alive and bullet.rect.colliderect(enemy.rect):
                    # Create explosion particles
                    for _ in range(20):
                        self.particles.append(Particle(
                            enemy.rect.centerx, enemy.rect.centery,
                            enemy.color
                        ))
                    
                    enemy.alive = False
                    self.player.score += enemy.value
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    break
        
        # Collision detection: Enemy bullets with player
        for bullet in self.enemy_bullets[:]:
            if bullet.rect.colliderect(self.player.rect):
                self.enemy_bullets.remove(bullet)
                self.player.lives -= 1
                
                # Create explosion particles
                for _ in range(30):
                    self.particles.append(Particle(
                        self.player.rect.centerx, self.player.rect.centery,
                        EXPLOSION_COLOR
                    ))
                
                if self.player.lives <= 0:
                    self.game_state = GameState.GAME_OVER
                break
        
        # Collision detection: Bullets with barriers
        for barrier in self.barriers:
            for bullet in self.player.bullets[:]:
                if bullet.rect.colliderect(barrier.rect):
                    barrier.health -= 10
                    if barrier.health <= 0:
                        barrier.health = 0
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
            
            for bullet in self.enemy_bullets[:]:
                if bullet.rect.colliderect(barrier.rect):
                    barrier.health -= 10
                    if barrier.health <= 0:
                        barrier.health = 0
                    if bullet in self.enemy_bullets:
                        self.enemy_bullets.remove(bullet)
        
        # Check if any enemy reached the bottom
        for enemy in self.enemies:
            if enemy.alive and enemy.rect.bottom > HEIGHT - 100:
                self.game_state = GameState.GAME_OVER
        
        # Check if all enemies are destroyed
        if all(not enemy.alive for enemy in self.enemies):
            self.player.level += 1
            self.player.score += 500
            self.game_state = GameState.LEVEL_COMPLETE
        
        # Update particles
        for particle in self.particles[:]:
            particle.update()
            if particle.life <= 0:
                self.particles.remove(particle)
    
    def draw(self):
        # Draw background
        screen.fill(BACKGROUND)
        
        # Draw stars
        for star in self.stars:
            star.draw()
        
        # Draw barriers
        for barrier in self.barriers:
            if barrier.health > 0:
                barrier.draw()
        
        # Draw enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw()
        
        # Draw player
        self.player.draw()
        
        # Draw bullets
        for bullet in self.player.bullets:
            bullet.draw()
        for bullet in self.enemy_bullets:
            bullet.draw()
        
        # Draw particles
        for particle in self.particles:
            particle.draw()
        
        # Draw HUD
        score_text = self.font.render(f"Score: {self.player.score}", True, TEXT_COLOR)
        lives_text = self.font.render(f"Lives: {self.player.lives}", True, TEXT_COLOR)
        level_text = self.font.render(f"Level: {self.player.level}", True, TEXT_COLOR)
        screen.blit(score_text, (20, 15))
        screen.blit(lives_text, (WIDTH - lives_text.get_width() - 20, 15))
        screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, 15))
        
        # Draw game state messages
        if self.game_state == GameState.START:
            self.draw_start_screen()
        elif self.game_state == GameState.GAME_OVER:
            self.draw_game_over()
        elif self.game_state == GameState.LEVEL_COMPLETE:
            self.draw_level_complete()
    
    def draw_start_screen(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 30, 200))
        screen.blit(overlay, (0, 0))
        
        title = self.title_font.render("SPACE INVADERS", True, (255, 215, 0))
        start_text = self.font.render("Press SPACE to Start", True, TEXT_COLOR)
        controls = self.small_font.render("Use LEFT/RIGHT arrows to move, SPACE to shoot", True, TEXT_COLOR)
        
        # Draw alien examples
        for i, color in enumerate(ENEMY_COLORS):
            pygame.draw.circle(screen, color, (WIDTH//2 - 150 + i*60, HEIGHT//2 + 30), 20)
            value_text = self.small_font.render(f"{ (5 - i) * 10 }", True, TEXT_COLOR)
            screen.blit(value_text, (WIDTH//2 - 150 + i*60 - value_text.get_width()//2, HEIGHT//2 + 60))
        
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//4))
        screen.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2))
        screen.blit(controls, (WIDTH//2 - controls.get_width()//2, HEIGHT - 100))
    
    def draw_game_over(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((30, 0, 0, 200))
        screen.blit(overlay, (0, 0))
        
        game_over = self.title_font.render("GAME OVER", True, (220, 60, 60))
        score_text = self.font.render(f"Final Score: {self.player.score}", True, TEXT_COLOR)
        restart = self.font.render("Press SPACE to Restart", True, TEXT_COLOR)
        
        screen.blit(game_over, (WIDTH//2 - game_over.get_width()//2, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(restart, (WIDTH//2 - restart.get_width()//2, HEIGHT//2 + 60))
    
    def draw_level_complete(self):
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 30, 0, 200))
        screen.blit(overlay, (0, 0))
        
        level_complete = self.title_font.render("LEVEL COMPLETE!", True, (50, 205, 50))
        score_text = self.font.render(f"Score: {self.player.score}  Level: {self.player.level}", True, TEXT_COLOR)
        next_level = self.font.render("Press SPACE for Next Level", True, TEXT_COLOR)
        
        screen.blit(level_complete, (WIDTH//2 - level_complete.get_width()//2, HEIGHT//2 - 60))
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2))
        screen.blit(next_level, (WIDTH//2 - next_level.get_width()//2, HEIGHT//2 + 60))

# Main game loop
def main():
    clock = pygame.time.Clock()
    game = SpaceInvaders()
    
    while True:
        game.handle_events()
        game.update()
        game.draw()
        
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()