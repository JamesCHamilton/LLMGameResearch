# This was made with Gemini 2.5 Pro
import pygame
import random

# Initialize PyGame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
PINK = (255, 182, 193)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

# Font
font = pygame.font.Font(None, 36)

# Game screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Game clock
clock = pygame.time.Clock()

class Pacman(pygame.sprite.Sprite):
    """Pac-Man player class"""
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = 0
        self.change_y = 0
        self.mouth_open = True
        self.mouth_timer = 0
        self.direction = 0 # 0: right, 1: left, 2: up, 3: down

    def update(self, walls):
        """Update Pac-Man's position"""
        # Move left/right
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_x > 0:
                self.rect.right = block.rect.left
            else:
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        for block in block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            else:
                self.rect.top = block.rect.bottom

        # Animate mouth
        self.mouth_timer += 1
        if self.mouth_timer >= 5:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0
        
        self.image.fill((0,0,0,0)) # Clear surface
        if self.mouth_open:
            if self.direction == 0: # Right
                pygame.draw.arc(self.image, YELLOW, (0,0,20,20), 0.5, 6, 10)
            elif self.direction == 1: # Left
                pygame.draw.arc(self.image, YELLOW, (0,0,20,20), 3.6, 2.6, 10)
            elif self.direction == 2: # Up
                pygame.draw.arc(self.image, YELLOW, (0,0,20,20), 2, 4.2, 10)
            elif self.direction == 3: # Down
                pygame.draw.arc(self.image, YELLOW, (0,0,20,20), 5.2, 1.1, 10)
        else:
             pygame.draw.circle(self.image, YELLOW, (10, 10), 10)


class Ghost(pygame.sprite.Sprite):
    """Ghost class"""
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface([20, 20], pygame.SRCALPHA)
        pygame.draw.rect(self.image, color, [0, 10, 20, 10])
        pygame.draw.circle(self.image, color, (10, 10), 10)
        # Eyes
        pygame.draw.circle(self.image, WHITE, (7, 8), 3)
        pygame.draw.circle(self.image, WHITE, (13, 8), 3)
        pygame.draw.circle(self.image, BLACK, (7, 8), 1)
        pygame.draw.circle(self.image, BLACK, (13, 8), 1)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.change_x = random.choice([-2, 2])
        self.change_y = 0
        self.frightened = False
        self.frightened_timer = 0

    def update(self, walls):
        """Update ghost's position"""
        self.rect.x += self.change_x
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        if block_hit_list:
            if self.change_x > 0:
                self.rect.right = block_hit_list[0].rect.left
            else:
                self.rect.left = block_hit_list[0].rect.right
            self.change_x = random.choice([-2, 2, 0])
            self.change_y = random.choice([-2, 2]) if self.change_x == 0 else 0


        self.rect.y += self.change_y
        block_hit_list = pygame.sprite.spritecollide(self, walls, False)
        if block_hit_list:
            if self.change_y > 0:
                self.rect.bottom = block_hit_list[0].rect.top
            else:
                self.rect.top = block_hit_list[0].rect.bottom
            self.change_y = random.choice([-2, 2, 0])
            self.change_x = random.choice([-2, 2]) if self.change_y == 0 else 0
        
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False
                # Revert to original color (this part needs the original color stored)


class Wall(pygame.sprite.Sprite):
    """Wall class"""
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Pellet(pygame.sprite.Sprite):
    """Pellet class"""
    def __init__(self, x, y, is_power=False):
        super().__init__()
        self.is_power = is_power
        if self.is_power:
            self.image = pygame.Surface([10, 10])
            self.image.fill(WHITE)
        else:
            self.image = pygame.Surface([4, 4])
            self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

def create_maze():
    """Create the maze layout"""
    wall_list = pygame.sprite.Group()
    pellet_list = pygame.sprite.Group()

    # Maze layout represented by a list of strings
    layout = [
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
        "W............WW............W",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "WPWWWW.WWWWW.WW.WWWWW.WWWWPW",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "W..........................W",
        "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
        "W.WWWW.WW.WWWWWWWW.WW.WWWW.W",
        "W......WW....WW....WW......W",
        "WWWWWW.WWWWW WW WWWWW.WWWWWW",
        "     W.WWWWW WW WWWWW.W     ",
        "     W.WW    G   WW.W     ",
        "WWWWWW.WW WWWWWW WW.WWWWWW",
        "W............P...........W",
        "WWWWWW.WW WWWWWW WW.WWWWWW",
        "     W.WW          WW.W     ",
        "     W.WW WWWWWWWW WW.W     ",
        "WWWWWW.WW WWWWWWWW WW.WWWWWW",
        "W............WW............W",
        "W.WWWW.WWWWW.WW.WWWWW.WWWW.W",
        "WP..WW................WW..PW",
        "WWW.WW.WW.WWWWWWWW.WW.WW.WWW",
        "W......WW....WW....WW......W",
        "W.WWWWWWWWWW.WW.WWWWWWWWWW.W",
        "W..........................W",
        "WWWWWWWWWWWWWWWWWWWWWWWWWWWW",
    ]

    # Create walls and pellets based on the layout
    for row_index, row in enumerate(layout):
        for col_index, char in enumerate(row):
            x = col_index * 20
            y = row_index * 20
            if char == 'W':
                wall_list.add(Wall(x, y, 20, 20))
            elif char == '.':
                pellet_list.add(Pellet(x + 10, y + 10))
            elif char == 'P':
                pellet_list.add(Pellet(x + 10, y + 10, is_power=True))

    return wall_list, pellet_list

def main():
    """Main game loop"""
    all_sprites_list = pygame.sprite.Group()
    wall_list, pellet_list = create_maze()
    all_sprites_list.add(wall_list)
    all_sprites_list.add(pellet_list)

    pacman = Pacman(280, 460)
    all_sprites_list.add(pacman)

    ghosts = pygame.sprite.Group()
    blinky = Ghost(280, 240, RED)
    pinky = Ghost(250, 240, PINK)
    inky = Ghost(310, 240, CYAN)
    clyde = Ghost(280, 210, ORANGE)
    ghosts.add(blinky, pinky, inky, clyde)
    all_sprites_list.add(ghosts)

    score = 0
    lives = 3
    game_over = False
    win = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.change_x = -3
                    pacman.change_y = 0
                    pacman.direction = 1
                elif event.key == pygame.K_RIGHT:
                    pacman.change_x = 3
                    pacman.change_y = 0
                    pacman.direction = 0
                elif event.key == pygame.K_UP:
                    pacman.change_x = 0
                    pacman.change_y = -3
                    pacman.direction = 2
                elif event.key == pygame.K_DOWN:
                    pacman.change_x = 0
                    pacman.change_y = 3
                    pacman.direction = 3

        # Update
        pacman.update(wall_list)
        ghosts.update(wall_list)

        # Collision with pellets
        pellet_hit_list = pygame.sprite.spritecollide(pacman, pellet_list, True)
        for pellet in pellet_hit_list:
            if pellet.is_power:
                score += 50
                for ghost in ghosts:
                    ghost.frightened = True
                    ghost.frightened_timer = 300 # 5 seconds at 60fps
            else:
                score += 10

        # Collision with ghosts
        ghost_hit_list = pygame.sprite.spritecollide(pacman, ghosts, False)
        for ghost in ghost_hit_list:
            if ghost.frightened:
                ghost.rect.x = 280
                ghost.rect.y = 240
                score += 200
            else:
                lives -= 1
                pacman.rect.x = 280
                pacman.rect.y = 460
                if lives == 0:
                    game_over = True

        if len(pellet_list) == 0:
            win = True
            game_over = True

        # Drawing
        screen.fill(BLACK)
        all_sprites_list.draw(screen)

        # Score and Lives
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, SCREEN_HEIGHT - 40))
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - 120, SCREEN_HEIGHT - 40))
        
        if game_over:
            if win:
                end_text = font.render("You Win!", True, GREEN)
            else:
                end_text = font.render("Game Over", True, RED)
            screen.blit(end_text, (SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
