import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Constants
TILE_SIZE = 24
MAZE_WIDTH, MAZE_HEIGHT = 19, 21
WIDTH, HEIGHT = MAZE_WIDTH * TILE_SIZE, MAZE_HEIGHT * TILE_SIZE
FPS = 60
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
PINK = (255, 105, 180)
RED = (255, 0, 0)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

# Simple maze layout (1=wall, 0=pellet, 2=empty)
MAZE = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,1,2,1,0,1,2,1,0,1,2,1,0,1,2,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,1,2,1,0,0,0,0,0,0,0,0,0,1,2,1,0,1],
    [1,0,1,1,1,1,1,1,1,2,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,0,1,1,2,1,1,0,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,0,1],
    [1,0,1,2,1,0,1,2,1,0,1,2,1,0,1,2,1,0,1],
    [1,0,1,1,1,0,1,1,1,0,1,1,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

# Pac-Man and ghost starting positions
PACMAN_START = (9, 15)
GHOST_STARTS = [(9, 7), (8, 7), (10, 7), (9, 8)]
GHOST_COLORS = [RED, PINK, CYAN, ORANGE]

class Pacman:
    def __init__(self):
        self.x, self.y = PACMAN_START
        self.dir = (0, 0)
        self.next_dir = (0, 0)
        self.score = 0
        self.alive = True
    def move(self):
        nx, ny = self.x + self.next_dir[0], self.y + self.next_dir[1]
        if MAZE[ny][nx] != 1:
            self.dir = self.next_dir
        nx, ny = self.x + self.dir[0], self.y + self.dir[1]
        if MAZE[ny][nx] != 1:
            self.x, self.y = nx, ny
        # Wrap around
        self.x %= MAZE_WIDTH
        self.y %= MAZE_HEIGHT
    def draw(self):
        px, py = self.x * TILE_SIZE + TILE_SIZE//2, self.y * TILE_SIZE + TILE_SIZE//2
        pygame.draw.circle(screen, YELLOW, (px, py), TILE_SIZE//2-2)

class Ghost:
    def __init__(self, x, y, color):
        self.x, self.y = x, y
        self.color = color
        self.dir = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
    def move(self):
        # Try to move in current direction, else pick a new one
        nx, ny = self.x + self.dir[0], self.y + self.dir[1]
        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and MAZE[ny][nx] != 1:
            self.x, self.y = nx, ny
        else:
            dirs = [(1,0),(-1,0),(0,1),(0,-1)]
            random.shuffle(dirs)
            for d in dirs:
                nx, ny = self.x + d[0], self.y + d[1]
                if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and MAZE[ny][nx] != 1:
                    self.dir = d
                    break
    def draw(self):
        px, py = self.x * TILE_SIZE + TILE_SIZE//2, self.y * TILE_SIZE + TILE_SIZE//2
        pygame.draw.circle(screen, self.color, (px, py), TILE_SIZE//2-2)

def draw_maze():
    for y, row in enumerate(MAZE):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, BLUE, (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == 0:
                pygame.draw.circle(screen, WHITE, (x*TILE_SIZE+TILE_SIZE//2, y*TILE_SIZE+TILE_SIZE//2), 4)

def main():
    pacman = Pacman()
    ghosts = [Ghost(x, y, color) for (x, y), color in zip(GHOST_STARTS, GHOST_COLORS)]
    pellets = sum(row.count(0) for row in MAZE)
    running = True
    game_over = False
    win = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_LEFT:
                    pacman.next_dir = (-1, 0)
                if event.key == pygame.K_RIGHT:
                    pacman.next_dir = (1, 0)
                if event.key == pygame.K_UP:
                    pacman.next_dir = (0, -1)
                if event.key == pygame.K_DOWN:
                    pacman.next_dir = (0, 1)
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()
                    return
        if not game_over:
            pacman.move()
            for ghost in ghosts:
                ghost.move()
            # Eat pellet
            if MAZE[pacman.y][pacman.x] == 0:
                MAZE[pacman.y][pacman.x] = 2
                pacman.score += 10
                pellets -= 1
            # Ghost collision
            for ghost in ghosts:
                if ghost.x == pacman.x and ghost.y == pacman.y:
                    pacman.alive = False
                    game_over = True
            # Win condition
            if pellets == 0:
                win = True
                game_over = True
        screen.fill(BLACK)
        draw_maze()
        pacman.draw()
        for ghost in ghosts:
            ghost.draw()
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT-40))
        if game_over:
            if win:
                msg = font.render("You Win! Press R to Restart", True, WHITE)
            else:
                msg = font.render("Game Over! Press R to Restart", True, WHITE)
            screen.blit(msg, (WIDTH//2 - msg.get_width()//2, HEIGHT//2))
        pygame.display.flip()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
