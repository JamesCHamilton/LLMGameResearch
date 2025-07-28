import pygame
import sys
import random

# Initialize pygame
pygame.init()

WIDTH, HEIGHT = 480, 600
TILE = 24
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)
PINK = (255, 105, 180)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Donkey Kong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)

# Level layout: 1=platform, 2=ladder, 0=empty
LEVEL = [
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,2,0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,2,0,0,0,0,0,2,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]
LEVEL_HEIGHT = len(LEVEL)
LEVEL_WIDTH = len(LEVEL[0])

PLAYER_START = (1, LEVEL_HEIGHT-2)
GOAL_POS = (LEVEL_WIDTH-2, 1)
KONG_POS = (1, 1)

class Player:
    def __init__(self):
        self.x, self.y = PLAYER_START
        self.px, self.py = self.x * TILE, self.y * TILE
        self.vx, self.vy = 0, 0
        self.on_ground = False
        self.climbing = False
        self.lives = 3
    def move(self, dx, dy):
        if dx != 0:
            nx = self.x + dx
            if 0 <= nx < LEVEL_WIDTH and LEVEL[self.y][nx] == 1:
                self.x = nx
        if dy != 0:
            ny = self.y + dy
            if 0 <= ny < LEVEL_HEIGHT and LEVEL[ny][self.x] == 2:
                self.y = ny
    def update(self, keys):
        self.on_ground = LEVEL[self.y][self.x] == 1
        self.climbing = LEVEL[self.y][self.x] == 2
        if keys[pygame.K_LEFT]:
            self.move(-1, 0)
        if keys[pygame.K_RIGHT]:
            self.move(1, 0)
        if keys[pygame.K_UP]:
            self.move(0, -1)
        if keys[pygame.K_DOWN]:
            self.move(0, 1)
        self.px, self.py = self.x * TILE, self.y * TILE
    def draw(self):
        pygame.draw.rect(screen, YELLOW, (self.px+4, self.py+4, TILE-8, TILE-8))

class Barrel:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.px, self.py = self.x * TILE, self.y * TILE
        self.dir = 1
    def update(self):
        # Move horizontally until ladder, then maybe drop
        if 0 <= self.x+self.dir < LEVEL_WIDTH and LEVEL[self.y][self.x+self.dir] == 1:
            self.x += self.dir
        elif 0 <= self.x+self.dir < LEVEL_WIDTH and LEVEL[self.y][self.x+self.dir] == 2 and random.random() < 0.2:
            self.y += 1
        else:
            self.dir *= -1
        self.px, self.py = self.x * TILE, self.y * TILE
    def draw(self):
        pygame.draw.circle(screen, BROWN, (self.px+TILE//2, self.py+TILE//2), TILE//3)

def draw_level():
    for y, row in enumerate(LEVEL):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, BLUE, (x*TILE, y*TILE, TILE, TILE))
            elif tile == 2:
                pygame.draw.rect(screen, WHITE, (x*TILE+TILE//3, y*TILE, TILE//3, TILE))

def main():
    player = Player()
    barrels = []
    barrel_timer = 0
    running = True
    game_over = False
    win = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_r:
                    main()
                    return
        if not game_over:
            keys = pygame.key.get_pressed()
            player.update(keys)
            # Spawn barrels
            barrel_timer += 1
            if barrel_timer > 60:
                barrels.append(Barrel(*KONG_POS))
                barrel_timer = 0
            for barrel in barrels[:]:
                barrel.update()
                # Collision with player
                if abs(barrel.x - player.x) < 1 and abs(barrel.y - player.y) < 1:
                    player.lives -= 1
                    barrels.remove(barrel)
                    if player.lives <= 0:
                        game_over = True
            # Win condition
            if player.x == GOAL_POS[0] and player.y == GOAL_POS[1]:
                win = True
                game_over = True
        screen.fill(BLACK)
        draw_level()
        # Draw Donkey Kong
        pygame.draw.rect(screen, RED, (KONG_POS[0]*TILE+2, KONG_POS[1]*TILE+2, TILE-4, TILE-4))
        # Draw goal (Pauline)
        pygame.draw.rect(screen, PINK, (GOAL_POS[0]*TILE+4, GOAL_POS[1]*TILE+4, TILE-8, TILE-8))
        player.draw()
        for barrel in barrels:
            barrel.draw()
        lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
        screen.blit(lives_text, (10, HEIGHT-40))
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
