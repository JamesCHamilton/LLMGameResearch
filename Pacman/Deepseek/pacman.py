import pygame
import random
import math

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 650
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = (HEIGHT - 50) // GRID_SIZE  # Extra space at bottom for score
PACMAN_SPEED = 2
GHOST_SPEED = 1

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man")
clock = pygame.time.Clock()

# Font
font = pygame.font.SysFont('Arial', 24)

# Game variables
score = 0
lives = 3
game_over = False
game_won = False

# Maze layout (1 = wall, 0 = path, 2 = pellet, 3 = power pellet)
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
    [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Pacman:
    def __init__(self):
        self.x = 14
        self.y = 23
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        self.speed = PACMAN_SPEED
        self.radius = GRID_SIZE // 2 - 2
        self.mouth_angle = 0
        self.mouth_opening = 5
        self.mouth_direction = 1
        self.color = YELLOW
        
    def move(self):
        # Check if next direction is possible
        next_x = round(self.x + self.next_direction[0])
        next_y = round(self.y + self.next_direction[1])
        
        if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze):
            if maze[next_y][next_x] != 1:
                self.direction = self.next_direction
        
        # Move in current direction if possible
        next_x = round(self.x + self.direction[0])
        next_y = round(self.y + self.direction[1])
        
        if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze):
            if maze[next_y][next_x] != 1:
                self.x += self.direction[0] * self.speed / 10
                self.y += self.direction[1] * self.speed / 10
                
                # Wrap around the tunnel
                if self.x < 0:
                    self.x = len(maze[0]) - 1
                elif self.x >= len(maze[0]):
                    self.x = 0
        
        # Animate mouth
        self.mouth_angle += self.mouth_direction * self.mouth_opening
        if self.mouth_angle > 45 or self.mouth_angle < 0:
            self.mouth_direction *= -1
    
    def draw(self):
        # Calculate screen position
        screen_x = self.x * GRID_SIZE + GRID_SIZE // 2
        screen_y = self.y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw Pac-Man
        start_angle = self.mouth_angle
        end_angle = 360 - self.mouth_angle
        
        # Determine the direction for the mouth
        if self.direction == RIGHT:
            start_angle += 0
            end_angle += 0
        elif self.direction == LEFT:
            start_angle += 180
            end_angle += 180
        elif self.direction == UP:
            start_angle += 90
            end_angle += 90
        elif self.direction == DOWN:
            start_angle += 270
            end_angle += 270
        
        pygame.draw.arc(screen, self.color, 
                       (screen_x - self.radius, screen_y - self.radius, 
                        self.radius * 2, self.radius * 2),
                       math.radians(start_angle), math.radians(end_angle), self.radius)
        pygame.draw.circle(screen, self.color, (int(screen_x), int(screen_y)), self.radius)
        
        # Draw a small triangle for the mouth effect
        if self.direction == RIGHT:
            points = [
                (screen_x, screen_y),
                (screen_x + self.radius, screen_y - self.radius * math.sin(math.radians(self.mouth_angle))),
                (screen_x + self.radius, screen_y + self.radius * math.sin(math.radians(self.mouth_angle)))
            ]
        elif self.direction == LEFT:
            points = [
                (screen_x, screen_y),
                (screen_x - self.radius, screen_y - self.radius * math.sin(math.radians(self.mouth_angle))),
                (screen_x - self.radius, screen_y + self.radius * math.sin(math.radians(self.mouth_angle)))
            ]
        elif self.direction == UP:
            points = [
                (screen_x, screen_y),
                (screen_x - self.radius * math.sin(math.radians(self.mouth_angle)), screen_y - self.radius),
                (screen_x + self.radius * math.sin(math.radians(self.mouth_angle)), screen_y - self.radius)
            ]
        elif self.direction == DOWN:
            points = [
                (screen_x, screen_y),
                (screen_x - self.radius * math.sin(math.radians(self.mouth_angle)), screen_y + self.radius),
                (screen_x + self.radius * math.sin(math.radians(self.mouth_angle)), screen_y + self.radius)
            ]
        else:
            points = []
        
        if points:
            pygame.draw.polygon(screen, BLACK, points)

class Ghost:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.color = color
        self.name = name
        self.direction = (0, 0)
        self.speed = GHOST_SPEED
        self.radius = GRID_SIZE // 2 - 2
        self.target = (0, 0)
        self.frightened = False
        self.frightened_timer = 0
        self.frightened_color = BLUE
        self.eye_color = WHITE
        self.pupil_color = BLACK
        
    def move(self, pacman):
        # Simple AI: move toward Pac-Man
        if not self.frightened:
            # Different behavior for each ghost
            if self.name == "Blinky":  # Red ghost - chases directly
                self.target = (round(pacman.x), round(pacman.y))
            elif self.name == "Pinky":  # Pink ghost - targets 4 tiles ahead of Pac-Man
                if pacman.direction == RIGHT:
                    self.target = (round(pacman.x) + 4, round(pacman.y))
                elif pacman.direction == LEFT:
                    self.target = (round(pacman.x) - 4, round(pacman.y))
                elif pacman.direction == UP:
                    self.target = (round(pacman.x), round(pacman.y) - 4)
                elif pacman.direction == DOWN:
                    self.target = (round(pacman.x), round(pacman.y) + 4)
                else:
                    self.target = (round(pacman.x), round(pacman.y))
            elif self.name == "Inky":  # Cyan ghost - complex behavior
                # Inky uses Blinky's position as reference
                blinky_vector = (round(pacman.x) - round(blinky.x), round(pacman.y) - round(blinky.y))
                self.target = (round(pacman.x) + blinky_vector[0], round(pacman.y) + blinky_vector[1])
            elif self.name == "Clyde":  # Orange ghost - runs away when close
                distance = math.sqrt((round(pacman.x) - round(self.x))**2 + (round(pacman.y) - round(self.y))**2)
                if distance > 8:
                    self.target = (round(pacman.x), round(pacman.y))
                else:
                    self.target = (0, len(maze))  # Bottom left corner
        else:
            # Frightened mode - random movement
            if random.random() < 0.1 or self.direction == (0, 0):
                self.target = (random.randint(0, len(maze[0]) - 1), random.randint(0, len(maze) - 1))
        
        # Find possible directions
        possible_directions = []
        for direction in [UP, DOWN, LEFT, RIGHT]:
            # Don't allow 180-degree turns (except when frightened)
            if not self.frightened and direction == (-self.direction[0], -self.direction[1]):
                continue
                
            next_x = round(self.x + direction[0])
            next_y = round(self.y + direction[1])
            
            # Wrap around
            if next_x < 0:
                next_x = len(maze[0]) - 1
            elif next_x >= len(maze[0]):
                next_x = 0
                
            if 0 <= next_y < len(maze):
                if maze[next_y][next_x] != 1:
                    possible_directions.append(direction)
        
        if possible_directions:
            # Choose direction that minimizes distance to target
            best_distance = float('inf')
            best_direction = self.direction  # Default to current direction
            
            for direction in possible_directions:
                next_x = round(self.x + direction[0])
                next_y = round(self.y + direction[1])
                
                # Wrap around
                if next_x < 0:
                    next_x = len(maze[0]) - 1
                elif next_x >= len(maze[0]):
                    next_x = 0
                
                distance = math.sqrt((next_x - self.target[0])**2 + (next_y - self.target[1])**2)
                
                if distance < best_distance:
                    best_distance = distance
                    best_direction = direction
            
            self.direction = best_direction
        
        # Move in current direction
        self.x += self.direction[0] * self.speed / 10
        self.y += self.direction[1] * self.speed / 10
        
        # Wrap around the tunnel
        if self.x < 0:
            self.x = len(maze[0]) - 1
        elif self.x >= len(maze[0]):
            self.x = 0
        
        # Update frightened timer
        if self.frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.frightened = False
    
    def draw(self):
        # Calculate screen position
        screen_x = self.x * GRID_SIZE + GRID_SIZE // 2
        screen_y = self.y * GRID_SIZE + GRID_SIZE // 2
        
        # Draw ghost body
        if self.frightened:
            body_color = self.frightened_color
        else:
            body_color = self.color
        
        pygame.draw.circle(screen, body_color, (int(screen_x), int(screen_y - self.radius // 2)), self.radius)
        pygame.draw.rect(screen, body_color, (int(screen_x - self.radius), int(screen_y - self.radius // 2), 
                                           self.radius * 2, self.radius))
        
        # Draw ghost bottom
        for i in range(3):
            pygame.draw.circle(screen, body_color, 
                              (int(screen_x - self.radius + i * self.radius), int(screen_y + self.radius // 2)), 
                              self.radius // 2)
            pygame.draw.circle(screen, body_color, 
                              (int(screen_x - self.radius // 2 + i * self.radius), int(screen_y + self.radius // 2)), 
                              self.radius // 2)
        
        # Draw eyes
        eye_offset = self.radius // 3
        pygame.draw.circle(screen, self.eye_color, (int(screen_x - eye_offset), int(screen_y - eye_offset)), self.radius // 3)
        pygame.draw.circle(screen, self.eye_color, (int(screen_x + eye_offset), int(screen_y - eye_offset)), self.radius // 3)
        
        # Draw pupils
        pupil_offset = self.radius // 6
        if self.direction == RIGHT:
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x - eye_offset + pupil_offset), int(screen_y - eye_offset)), self.radius // 6)
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x + eye_offset + pupil_offset), int(screen_y - eye_offset)), self.radius // 6)
        elif self.direction == LEFT:
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x - eye_offset - pupil_offset), int(screen_y - eye_offset)), self.radius // 6)
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x + eye_offset - pupil_offset), int(screen_y - eye_offset)), self.radius // 6)
        elif self.direction == UP:
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x - eye_offset), int(screen_y - eye_offset - pupil_offset)), self.radius // 6)
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x + eye_offset), int(screen_y - eye_offset - pupil_offset)), self.radius // 6)
        elif self.direction == DOWN:
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x - eye_offset), int(screen_y - eye_offset + pupil_offset)), self.radius // 6)
            pygame.draw.circle(screen, self.pupil_color, 
                             (int(screen_x + eye_offset), int(screen_y - eye_offset + pupil_offset)), self.radius // 6)

def draw_maze():
    for y in range(len(maze)):
        for x in range(len(maze[0])):
            if maze[y][x] == 1:  # Wall
                pygame.draw.rect(screen, BLUE, 
                               (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)
                # Draw thicker walls for better visibility
                if y > 0 and maze[y-1][x] == 1:
                    pygame.draw.line(screen, BLUE, 
                                    (x * GRID_SIZE, y * GRID_SIZE),
                                    ((x + 1) * GRID_SIZE, y * GRID_SIZE), 3)
                if x > 0 and maze[y][x-1] == 1:
                    pygame.draw.line(screen, BLUE, 
                                    (x * GRID_SIZE, y * GRID_SIZE),
                                    (x * GRID_SIZE, (y + 1) * GRID_SIZE), 3)
            elif maze[y][x] == 2:  # Pellet
                pygame.draw.circle(screen, WHITE, 
                                 (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 
                                 2)
            elif maze[y][x] == 3:  # Power pellet
                pygame.draw.circle(screen, WHITE, 
                                 (x * GRID_SIZE + GRID_SIZE // 2, y * GRID_SIZE + GRID_SIZE // 2), 
                                 5)

def check_collision():
    global score, lives, game_over
    
    # Check pellet collection
    pacman_grid_x = round(pacman.x)
    pacman_grid_y = round(pacman.y)
    
    if 0 <= pacman_grid_x < len(maze[0]) and 0 <= pacman_grid_y < len(maze):
        if maze[pacman_grid_y][pacman_grid_x] == 2:
            maze[pacman_grid_y][pacman_grid_x] = 0
            score += 10
        elif maze[pacman_grid_y][pacman_grid_x] == 3:
            maze[pacman_grid_y][pacman_grid_x] = 0
            score += 50
            # Make ghosts frightened
            for ghost in ghosts:
                ghost.frightened = True
                ghost.frightened_timer = 500  # About 10 seconds at 50 FPS
    
    # Check if all pellets are eaten
    pellets_left = sum(row.count(2) + row.count(3) for row in maze)
    if pellets_left == 0:
        global game_won
        game_won = True
        game_over = True
    
    # Check ghost collisions
    for ghost in ghosts:
        distance = math.sqrt((pacman.x - ghost.x)**2 + (pacman.y - ghost.y)**2)
        if distance < 0.8:  # Collision threshold
            if ghost.frightened:
                # Eat the ghost
                ghost.x = ghost.initial_x
                ghost.y = ghost.initial_y
                ghost.frightened = False
                score += 200
            else:
                # Lose a life
                lives -= 1
                if lives <= 0:
                    game_over = True
                else:
                    # Reset positions
                    pacman.x = 14
                    pacman.y = 23
                    pacman.direction = (0, 0)
                    pacman.next_direction = (0, 0)
                    for ghost in ghosts:
                        ghost.x = ghost.initial_x
                        ghost.y = ghost.initial_y
                        ghost.direction = (0, 0)

def draw_game_info():
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, HEIGHT - 40))
    
    # Draw lives
    for i in range(lives):
        pygame.draw.circle(screen, YELLOW, (30 + i * 30, HEIGHT - 20), 10)
    
    # Draw game over or win message
    if game_over:
        if game_won:
            message = font.render("YOU WIN! Press R to restart", True, WHITE)
        else:
            message = font.render("GAME OVER! Press R to restart", True, WHITE)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2))

def reset_game():
    global score, lives, game_over, game_won, maze
    
    # Reset game variables
    score = 0
    lives = 3
    game_over = False
    game_won = False
    
    # Reset maze (replace pellets)
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 3, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 3, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 2, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 2, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 2, 1],
        [1, 3, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 0, 0, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 3, 1],
        [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 2, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]
    
    # Reset characters
    pacman.x = 14
    pacman.y = 23
    pacman.direction = (0, 0)
    pacman.next_direction = (0, 0)
    
    for ghost in ghosts:
        ghost.x = ghost.initial_x
        ghost.y = ghost.initial_y
        ghost.direction = (0, 0)
        ghost.frightened = False
        ghost.frightened_timer = 0

# Create game objects
pacman = Pacman()

# Create ghosts
blinky = Ghost(14, 11, RED, "Blinky")
pinky = Ghost(14, 14, PINK, "Pinky")
inky = Ghost(12, 14, CYAN, "Inky")
clyde = Ghost(16, 14, ORANGE, "Clyde")

ghosts = [blinky, pinky, inky, clyde]

# Set initial positions for ghosts
for ghost in ghosts:
    ghost.initial_x = ghost.x
    ghost.initial_y = ghost.y

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.next_direction = UP
            elif event.key == pygame.K_DOWN:
                pacman.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                pacman.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                pacman.next_direction = RIGHT
            elif event.key == pygame.K_r and game_over:
                reset_game()
    
    if not game_over:
        # Update game state
        pacman.move()
        for ghost in ghosts:
            ghost.move(pacman)
        check_collision()
    
    # Draw everything
    screen.fill(BLACK)
    draw_maze()
    for ghost in ghosts:
        ghost.draw()
    pacman.draw()
    draw_game_info()
    
    # Update the display
    pygame.display.flip()
    
    # Cap the frame rate
    clock.tick(50)

pygame.quit()