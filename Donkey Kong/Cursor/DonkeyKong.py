import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
PINK = (255, 192, 203)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 25
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 3
        self.jump_power = 15
        self.on_ground = False
        self.on_ladder = False
        self.gravity = 0.8
        self.max_fall_speed = 10
        
    def update(self, platforms, ladders):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        self.vel_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel_x = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel_x = self.speed
            
        # Check if on ladder
        self.on_ladder = False
        for ladder in ladders:
            if (self.x + self.width/2 >= ladder.x and 
                self.x + self.width/2 <= ladder.x + ladder.width and
                self.y + self.height >= ladder.y and 
                self.y <= ladder.y + ladder.height):
                self.on_ladder = True
                break
        
        # Vertical movement
        if self.on_ladder:
            self.vel_y = 0
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vel_y = -self.speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vel_y = self.speed
        else:
            # Apply gravity
            if not self.on_ground:
                self.vel_y += self.gravity
                if self.vel_y > self.max_fall_speed:
                    self.vel_y = self.max_fall_speed
            
            # Jump
            if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
                self.vel_y = -self.jump_power
                self.on_ground = False
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check platform collisions
        self.on_ground = False
        for platform in platforms:
            if (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y):
                
                # Landing on top of platform
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    self.on_ground = True
                # Hitting platform from below
                elif self.vel_y < 0 and self.y > platform.y:
                    self.y = platform.y + platform.height
                    self.vel_y = 0
                # Side collisions
                elif self.vel_x > 0:
                    self.x = platform.x - self.width
                elif self.vel_x < 0:
                    self.x = platform.x + platform.width
        
        # Keep player on screen
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        
        # Check if player fell off screen
        if self.y > SCREEN_HEIGHT:
            return True  # Player died
        
        return False
    
    def draw(self, screen):
        # Draw Mario (simple red rectangle with blue overalls)
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLUE, (self.x + 2, self.y + 8, self.width - 4, self.height - 8))

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))

class Ladder:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def draw(self, screen):
        # Draw ladder rungs
        for i in range(0, self.height, 15):
            pygame.draw.rect(screen, BROWN, (self.x, self.y + i, self.width, 3))
        # Draw ladder sides
        pygame.draw.rect(screen, BROWN, (self.x, self.y, 3, self.height))
        pygame.draw.rect(screen, BROWN, (self.x + self.width - 3, self.y, 3, self.height))

class Barrel:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 15
        self.height = 15
        self.vel_x = 2
        self.vel_y = 0
        self.gravity = 0.5
        self.bounce = -8
        self.on_platform = False
        
    def update(self, platforms):
        # Apply gravity
        self.vel_y += self.gravity
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Check platform collisions
        self.on_platform = False
        for platform in platforms:
            if (self.x < platform.x + platform.width and
                self.x + self.width > platform.x and
                self.y < platform.y + platform.height and
                self.y + self.height > platform.y):
                
                if self.vel_y > 0 and self.y < platform.y:
                    self.y = platform.y - self.height
                    self.vel_y = self.bounce
                    self.on_platform = True
                    # Randomly change direction sometimes
                    if random.random() < 0.3:
                        self.vel_x = -self.vel_x
        
        # Remove if off screen
        if self.y > SCREEN_HEIGHT + 50:
            return True
        return False
    
    def draw(self, screen):
        pygame.draw.ellipse(screen, ORANGE, (self.x, self.y, self.width, self.height))
        pygame.draw.ellipse(screen, BROWN, (self.x + 2, self.y + 2, self.width - 4, self.height - 4))

class Princess:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 25
        
    def draw(self, screen):
        pygame.draw.rect(screen, PINK, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, YELLOW, (self.x + 2, self.y, self.width - 4, 8))  # Hair

class DonkeyKong:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 30
        self.barrel_timer = 0
        self.barrel_spawn_rate = 90  # frames between barrels
        
    def update(self):
        self.barrel_timer += 1
        if self.barrel_timer >= self.barrel_spawn_rate:
            self.barrel_timer = 0
            return True  # Spawn barrel
        return False
    
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        # Draw angry eyes
        pygame.draw.rect(screen, RED, (self.x + 8, self.y + 8, 4, 4))
        pygame.draw.rect(screen, RED, (self.x + 28, self.y + 8, 4, 4))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Donkey Kong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
        
    def reset_game(self):
        self.player = Player(50, SCREEN_HEIGHT - 100)
        self.barrels = []
        self.score = 0
        self.lives = 3
        
        # Create platforms (classic Donkey Kong level layout)
        self.platforms = [
            Platform(0, SCREEN_HEIGHT - 20, SCREEN_WIDTH, 20),  # Ground
            Platform(100, SCREEN_HEIGHT - 120, 600, 15),         # Level 1
            Platform(50, SCREEN_HEIGHT - 220, 600, 15),          # Level 2  
            Platform(100, SCREEN_HEIGHT - 320, 600, 15),         # Level 3
            Platform(50, SCREEN_HEIGHT - 420, 600, 15),          # Level 4
            Platform(100, SCREEN_HEIGHT - 520, 200, 15),         # Top platform
        ]
        
        # Create ladders
        self.ladders = [
            Ladder(150, SCREEN_HEIGHT - 135, 15, 100),
            Ladder(600, SCREEN_HEIGHT - 235, 15, 100),
            Ladder(200, SCREEN_HEIGHT - 335, 15, 100),
            Ladder(550, SCREEN_HEIGHT - 435, 15, 100),
            Ladder(250, SCREEN_HEIGHT - 535, 15, 100),
        ]
        
        # Create characters
        self.donkey_kong = DonkeyKong(150, SCREEN_HEIGHT - 550)
        self.princess = Princess(250, SCREEN_HEIGHT - 550)
        
    def check_collisions(self):
        # Check barrel-player collisions
        player_rect = pygame.Rect(self.player.x, self.player.y, self.player.width, self.player.height)
        for barrel in self.barrels[:]:
            barrel_rect = pygame.Rect(barrel.x, barrel.y, barrel.width, barrel.height)
            if player_rect.colliderect(barrel_rect):
                self.lives -= 1
                self.barrels.remove(barrel)
                if self.lives <= 0:
                    return "game_over"
                
        # Check if player reached princess
        princess_rect = pygame.Rect(self.princess.x, self.princess.y, self.princess.width, self.princess.height)
        if player_rect.colliderect(princess_rect):
            return "win"
            
        return None
    
    def run(self):
        running = True
        game_state = "playing"  # "playing", "game_over", "win"
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and game_state != "playing":
                        self.reset_game()
                        game_state = "playing"
            
            if game_state == "playing":
                # Update player
                if self.player.update(self.platforms, self.ladders):
                    self.lives -= 1
                    if self.lives <= 0:
                        game_state = "game_over"
                    else:
                        self.player = Player(50, SCREEN_HEIGHT - 100)
                
                # Update Donkey Kong and spawn barrels
                if self.donkey_kong.update():
                    self.barrels.append(Barrel(self.donkey_kong.x + 20, self.donkey_kong.y + 30))
                
                # Update barrels
                for barrel in self.barrels[:]:
                    if barrel.update(self.platforms):
                        self.barrels.remove(barrel)
                        self.score += 10
                
                # Check collisions
                collision_result = self.check_collisions()
                if collision_result:
                    game_state = collision_result
            
            # Draw everything
            self.screen.fill(BLACK)
            
            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen)
            
            # Draw ladders
            for ladder in self.ladders:
                ladder.draw(self.screen)
            
            # Draw characters
            self.player.draw(self.screen)
            self.donkey_kong.draw(self.screen)
            self.princess.draw(self.screen)
            
            # Draw barrels
            for barrel in self.barrels:
                barrel.draw(self.screen)
            
            # Draw UI
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
            self.screen.blit(score_text, (10, 10))
            self.screen.blit(lives_text, (10, 50))
            
            # Draw game state messages
            if game_state == "game_over":
                game_over_text = self.font.render("GAME OVER - Press R to restart", True, RED)
                text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(game_over_text, text_rect)
            elif game_state == "win":
                win_text = self.font.render("YOU WIN! - Press R to restart", True, GREEN)
                text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
                self.screen.blit(win_text, text_rect)
            
            # Draw instructions
            if game_state == "playing":
                instructions = [
                    "Arrow Keys/WASD: Move",
                    "Space/Up: Jump",
                    "Up/Down on ladders: Climb",
                    "Reach the Princess!"
                ]
                for i, instruction in enumerate(instructions):
                    text = pygame.font.Font(None, 24).render(instruction, True, WHITE)
                    self.screen.blit(text, (SCREEN_WIDTH - 200, 10 + i * 25))
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()  