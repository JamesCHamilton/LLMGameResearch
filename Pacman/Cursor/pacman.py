import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Screen dimensions and grid
TILE_SIZE = 24
GRID_WIDTH, GRID_HEIGHT = 28, 31
WIDTH, HEIGHT = TILE_SIZE * GRID_WIDTH, TILE_SIZE * GRID_HEIGHT
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Pac-Man')

# Colors
BLACK = (0, 0, 0)
BLUE = (33, 33, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)

# Fonts
FONT = pygame.font.SysFont('Arial', 24)
GAME_OVER_FONT = pygame.font.SysFont('Arial', 64)

# Simple maze layout (1=wall, 0=pellet, 2=empty)
MAZE = [
    [1]*28,
    [1]+[0]*26+[1],
    [1]+[0]+[1]*24+[0]+[1],
    [1]+[0]+[1]+[0]*22+[1]+[0]+[1],
    [1]+[0]+[1]+[0]+[1]*20+[0]+[1]+[0]+[1],
    [1]+[0]+[1]+[0]+[1]+[0]*18+[1]+[0]+[1]+[0]+[1],
    [1]+[0]+[1]+[0]+[1]+[0]+[1]*16+[0]+[1]+[0]+[1]+[0]+[1],
    [1]+[0]*26+[1],
    [1]*28,
] + [[1]+[0]*26+[1] for _ in range(22)] + [
    [1]*28
]
# Pad maze to 31 rows
while len(MAZE) < 31:
    MAZE.append([1]+[0]*26+[1])

# Pac-Man class
def find_start():
    for y, row in enumerate(MAZE):
        for x, val in enumerate(row):
            if val == 0:
                return x, y
    return 1, 1

class PacMan:
    def __init__(self):
        self.x, self.y = find_start()
        self.dir: tuple[int, int] = (0, 0)
        self.next_dir: tuple[int, int] = (0, 0)
        self.score = 0
        self.alive = True

    def move(self):
        # Try to turn if possible
        nx, ny = self.x + self.next_dir[0], self.y + self.next_dir[1]
        if self.can_move(nx, ny):
            self.dir = self.next_dir
        # Move in current direction
        nx, ny = self.x + self.dir[0], self.y + self.dir[1]
        if self.can_move(nx, ny):
            self.x, self.y = nx, ny
        # Eat pellet
        if MAZE[self.y][self.x] == 0:
            MAZE[self.y][self.x] = 2
            self.score += 10

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and MAZE[y][x] != 1

    def draw(self, surface):
        px, py = self.x * TILE_SIZE + TILE_SIZE//2, self.y * TILE_SIZE + TILE_SIZE//2
        pygame.draw.circle(surface, YELLOW, (px, py), TILE_SIZE//2-2)

# Ghost class
class Ghost:
    def __init__(self, color=PINK):
        self.x, self.y = GRID_WIDTH//2, GRID_HEIGHT//2
        self.color = color
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def move(self):
        # Try to move in current direction
        nx, ny = self.x + self.dir[0], self.y + self.dir[1]
        if self.can_move(nx, ny):
            self.x, self.y = nx, ny
        else:
            # Pick a new random direction
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            random.shuffle(dirs)
            for d in dirs:
                nx, ny = self.x + d[0], self.y + d[1]
                if self.can_move(nx, ny):
                    self.dir = d
                    self.x, self.y = nx, ny
                    break

    def can_move(self, x, y):
        return 0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT and MAZE[y][x] != 1

    def draw(self, surface):
        px, py = self.x * TILE_SIZE + TILE_SIZE//2, self.y * TILE_SIZE + TILE_SIZE//2
        pygame.draw.circle(surface, self.color, (px, py), TILE_SIZE//2-2)

# Draw maze
def draw_maze(surface):
    for y, row in enumerate(MAZE):
        for x, val in enumerate(row):
            px, py = x * TILE_SIZE, y * TILE_SIZE
            if val == 1:
                pygame.draw.rect(surface, BLUE, (px, py, TILE_SIZE, TILE_SIZE))
            elif val == 0:
                pygame.draw.circle(surface, WHITE, (px+TILE_SIZE//2, py+TILE_SIZE//2), 4)

# Game loop
clock = pygame.time.Clock()
pacman = PacMan()
ghost = Ghost()
game_over = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if not game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.next_dir = (0, -1)
            elif event.key == pygame.K_DOWN:
                pacman.next_dir = (0, 1)
            elif event.key == pygame.K_LEFT:
                pacman.next_dir = (-1, 0)
            elif event.key == pygame.K_RIGHT:
                pacman.next_dir = (1, 0)

    if not game_over:
        pacman.move()
        ghost.move()
        # Check collision
        if pacman.x == ghost.x and pacman.y == ghost.y:
            game_over = True
        # Check win (all pellets eaten)
        if all(val != 0 for row in MAZE for val in row):
            game_over = True

    # Draw everything
    SCREEN.fill(BLACK)
    draw_maze(SCREEN)
    pacman.draw(SCREEN)
    ghost.draw(SCREEN)
    # Draw score
    score_text = FONT.render(f'Score: {pacman.score}', True, WHITE)
    SCREEN.blit(score_text, (10, HEIGHT-30))
    # Draw game over
    if game_over:
        over_text = GAME_OVER_FONT.render('Game Over!', True, YELLOW)
        SCREEN.blit(over_text, (WIDTH//2 - over_text.get_width()//2, HEIGHT//2 - 40))
    pygame.display.flip()
    clock.tick(10)

pygame.quit()
sys.exit() 