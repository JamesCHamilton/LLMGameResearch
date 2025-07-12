import pygame
import random
import math
from typing import List, Tuple

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game settings
PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 1
ALIEN_DROP = 20
ALIEN_BULLET_SPEED = 3

class Player:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 30
        self.speed = PLAYER_SPEED
        self.health = 3
        self.bullets: List[Bullet] = []
        self.shoot_delay = 0
        
    def draw(self, screen):
        # Draw player ship
        pygame.draw.polygon(screen, GREEN, [
            (self.x, self.y + self.height),
            (self.x + self.width // 2, self.y),
            (self.x + self.width, self.y + self.height)
        ])
        # Draw health bar
        for i in range(self.health):
            pygame.draw.rect(screen, RED, (10 + i * 30, 10, 25, 10))
            
    def move(self, direction: int):
        new_x = self.x + direction * self.speed
        if 0 <= new_x <= SCREEN_WIDTH - self.width:
            self.x = new_x
            
    def shoot(self):
        if self.shoot_delay <= 0:
            bullet = Bullet(self.x + self.width // 2, self.y, -1)
            self.bullets.append(bullet)
            self.shoot_delay = 10
            
    def update(self):
        if self.shoot_delay > 0:
            self.shoot_delay -= 1
            
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < 0:
                self.bullets.remove(bullet)

class Alien:
    def __init__(self, x: int, y: int, alien_type: int = 0):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.alien_type = alien_type
        self.direction = 1
        self.shoot_delay = random.randint(30, 120)
        
    def draw(self, screen):
        # Draw different alien types
        if self.alien_type == 0:  # Top row - 10 points
            color = RED
            points = [(self.x + self.width//2, self.y), (self.x, self.y + self.height),
                     (self.x + self.width//4, self.y + self.height//2), 
                     (self.x + 3*self.width//4, self.y + self.height//2),
                     (self.x + self.width, self.y + self.height)]
        elif self.alien_type == 1:  # Middle rows - 20 points
            color = YELLOW
            points = [(self.x, self.y), (self.x + self.width, self.y),
                     (self.x + self.width//2, self.y + self.height)]
        else:  # Bottom rows - 30 points
            color = BLUE
            points = [(self.x, self.y), (self.x + self.width, self.y),
                     (self.x, self.y + self.height), (self.x + self.width, self.y + self.height)]
            
        pygame.draw.polygon(screen, color, points)
        
    def move(self, speed: int):
        self.x += speed * self.direction
        
    def should_shoot(self) -> bool:
        if self.shoot_delay <= 0:
            self.shoot_delay = random.randint(60, 180)
            return True
        self.shoot_delay -= 1
        return False

class Bullet:
    def __init__(self, x: int, y: int, direction: int):
        self.x = x
        self.y = y
        self.width = 3
        self.height = 10
        self.speed = BULLET_SPEED if direction == -1 else ALIEN_BULLET_SPEED
        self.direction = direction
        
    def draw(self, screen):
        color = GREEN if self.direction == -1 else RED
        pygame.draw.rect(screen, color, (self.x, self.y, self.width, self.height))
        
    def update(self):
        self.y += self.direction * self.speed
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Explosion:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.lifetime = 10
        
    def draw(self, screen):
        if self.lifetime > 0:
            size = 20 - self.lifetime * 2
            pygame.draw.circle(screen, WHITE, (self.x, self.y), size)
            self.lifetime -= 1

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.running = True
        self.score = 0
        self.level = 1
        
        # Game objects
        self.player = Player(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50)
        self.aliens: List[Alien] = []
        self.alien_bullets: List[Bullet] = []
        self.explosions: List[Explosion] = []
        
        # Game state
        self.alien_direction = 1
        self.alien_speed = ALIEN_SPEED
        self.game_over = False
        self.victory = False
        
        self.create_aliens()
        
    def create_aliens(self):
        self.aliens.clear()
        rows = 5
        cols = 11
        start_x = 50
        start_y = 50
        
        for row in range(rows):
            for col in range(cols):
                x = start_x + col * 60
                y = start_y + row * 50
                alien_type = row // 2  # Different types for different rows
                self.aliens.append(Alien(x, y, alien_type))
                
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not self.game_over and not self.victory:
                        self.player.shoot()
                elif event.key == pygame.K_r and (self.game_over or self.victory):
                    self.__init__()
                    
    def update(self):
        if self.game_over or self.victory:
            return
            
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)
            
        self.player.update()
        
        # Alien movement
        edge_hit = False
        for alien in self.aliens:
            alien.move(self.alien_speed * self.alien_direction)
            if alien.x <= 0 or alien.x + alien.width >= SCREEN_WIDTH:
                edge_hit = True
                
        if edge_hit:
            self.alien_direction *= -1
            for alien in self.aliens:
                alien.y += ALIEN_DROP
                
        # Alien shooting
        for alien in self.aliens:
            if alien.should_shoot():
                bullet = Bullet(alien.x + alien.width // 2, alien.y + alien.height, 1)
                self.alien_bullets.append(bullet)
                
        # Update alien bullets
        for bullet in self.alien_bullets[:]:
            bullet.update()
            if bullet.y > SCREEN_HEIGHT:
                self.alien_bullets.remove(bullet)
                
        # Update explosions
        for explosion in self.explosions[:]:
            explosion.draw(self.screen)
            if explosion.lifetime <= 0:
                self.explosions.remove(explosion)
                
        # Collision detection
        self.check_collisions()
        
        # Check win/lose conditions
        if len(self.aliens) == 0:
            self.victory = True
        elif any(alien.y + alien.height >= self.player.y for alien in self.aliens):
            self.game_over = True
        elif self.player.health <= 0:
            self.game_over = True
            
    def check_collisions(self):
        # Player bullets vs aliens
        for bullet in self.player.bullets[:]:
            bullet_rect = bullet.get_rect()
            for alien in self.aliens[:]:
                alien_rect = pygame.Rect(alien.x, alien.y, alien.width, alien.height)
                if bullet_rect.colliderect(alien_rect):
                    # Score based on alien type
                    if alien.alien_type == 0:
                        self.score += 10
                    elif alien.alien_type == 1:
                        self.score += 20
                    else:
                        self.score += 30
                        
                    self.aliens.remove(alien)
                    self.player.bullets.remove(bullet)
                    self.explosions.append(Explosion(alien.x + alien.width//2, alien.y + alien.height//2))
                    break
                    
        # Alien bullets vs player
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for bullet in self.alien_bullets[:]:
            bullet_rect = bullet.get_rect()
            if bullet_rect.colliderect(player_rect):
                self.player.health -= 1
                self.alien_bullets.remove(bullet)
                self.explosions.append(Explosion(self.player.x + self.player.width//2, self.player.y + self.player.height//2))
                break
                
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw stars (background)
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)
            
        # Draw game objects
        self.player.draw(self.screen)
        
        for alien in self.aliens:
            alien.draw(self.screen)
            
        for bullet in self.player.bullets:
            bullet.draw(self.screen)
            
        for bullet in self.alien_bullets:
            bullet.draw(self.screen)
            
        # Draw score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - 150, 10))
        
        # Draw level
        level_text = font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_text, (SCREEN_WIDTH - 150, 50))
        
        # Draw game over or victory screen
        if self.game_over:
            self.draw_game_over()
        elif self.victory:
            self.draw_victory()
            
        pygame.display.flip()
        
    def draw_game_over(self):
        font = pygame.font.Font(None, 72)
        text = font.render("GAME OVER", True, RED)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to restart", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def draw_victory(self):
        font = pygame.font.Font(None, 72)
        text = font.render("VICTORY!", True, GREEN)
        text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
        self.screen.blit(text, text_rect)
        
        font_small = pygame.font.Font(None, 36)
        restart_text = font_small.render("Press R to play again", True, WHITE)
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
        self.screen.blit(restart_text, restart_rect)
        
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run() 