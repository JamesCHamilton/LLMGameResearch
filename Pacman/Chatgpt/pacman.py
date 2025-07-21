import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 560, 620
TILE_SIZE = 20
FPS = 10
BLACK = (0, 0, 0)
BLUE = (33, 33, 222)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Map layout (1 = wall, 0 = dot path, 2 = empty path)
layout = [
    "1111111111111111111111111",
    "1000000000110000000000001",
    "1011111110110111111111101",
    "1011111110110111111111101",
    "1000000000000000000000001",
    "1011110111111110111111101",
    "1000000110000011000000001",
    "1111110110111101101111111",
    "0000010110000001101000000",
    "1111011110111110111101111",
    "100000000000P000000000001",
    "1111011111110111111101111",
    "0000010000000000001000000",
    "1111110111111111011111111",
    "1000000110000011000000001",
    "1011110110111101101111101",
    "1000000000110000000000001",
    "1011111110110111111111101",
    "1000000000000000000000001",
    "1111111111111111111111111",
]

ROWS = len(layout)
COLS = len(layout[0])

# Setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# Pac-Man Class
class Pacman:
    def __init__(self):
        for y, row in enumerate(layout):
            for x, tile in enumerate(row):
                if tile == "P":
                    self.x, self.y = x, y
        self.dx = 0
        self.dy = 0
        self.score = 0

    def move(self):
        if self.can_move(self.dx, self.dy):
            self.x += self.dx
            self.y += self.dy
            if layout[self.y][self.x] == "0":
                self.score += 10
                row = list(layout[self.y])
                row[self.x] = "2"
                layout[self.y] = ''.join(row)

    def can_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        if layout[new_y][new_x] != "1":
            return True
        return False

    def draw(self):
        pygame.draw.circle(screen, YELLOW, (self.x * TILE_SIZE + TILE_SIZE // 2, self.y * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 2)

# Draw Map
def draw_map():
    for y, row in enumerate(layout):
        for x, tile in enumerate(row):
            if tile == "1":
                pygame.draw.rect(screen, BLUE, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile == "0":
                pygame.draw.circle(screen, WHITE, (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2), 3)

# Game Loop
def main():
    pacman = Pacman()

    while True:
        screen.fill(BLACK)

        # Handle Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    pacman.dx, pacman.dy = -1, 0
                elif event.key == pygame.K_RIGHT:
                    pacman.dx, pacman.dy = 1, 0
                elif event.key == pygame.K_UP:
                    pacman.dx, pacman.dy = 0, -1
                elif event.key == pygame.K_DOWN:
                    pacman.dx, pacman.dy = 0, 1

        pacman.move()
        draw_map()
        pacman.draw()

        # Score
        score_text = font.render(f"Score: {pacman.score}", True, WHITE)
        screen.blit(score_text, (10, HEIGHT - 40))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
