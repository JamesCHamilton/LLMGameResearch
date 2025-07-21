import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pac-Man")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
BLUE = (0, 0, 255) # For frightened ghosts

# Game settings
TILE_SIZE = 20
PACMAN_SPEED = 5
GHOST_SPEED = 4
FONT_SIZE = 30

# Maze layout (0: path, 1: wall, 2: pellet, 3: power pellet, 4: ghost home)
# The maze is designed to fit within the screen dimensions.
# Each number represents a TILE_SIZE x TILE_SIZE block.
# The maze is padded with walls to ensure Pac-Man stays within bounds.
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 3, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 3, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 2, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Calculate maze dimensions in pixels
MAZE_WIDTH_PX = len(maze[0]) * TILE_SIZE
MAZE_HEIGHT_PX = len(maze) * TILE_SIZE

# Calculate offset to center the maze
OFFSET_X = (SCREEN_WIDTH - MAZE_WIDTH_PX) // 2
OFFSET_Y = (SCREEN_HEIGHT - MAZE_HEIGHT_PX) // 2

# Pac-Man class
class PacMan(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.dx = 0
        self.dy = 0
        self.score = 0
        self.lives = 3
        self.start_pos = (x, y) # Store initial position for resetting
        self.mouth_open = True
        self.mouth_timer = 0
        self.mouth_interval = 10 # Frames between mouth open/close

    def update(self):
        # Update mouth animation
        self.mouth_timer += 1
        if self.mouth_timer >= self.mouth_interval:
            self.mouth_open = not self.mouth_open
            self.mouth_timer = 0

        # Calculate new position
        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy

        # Check for wall collisions
        # Get the maze coordinates for the current position
        current_maze_x = (self.rect.centerx - OFFSET_X) // TILE_SIZE
        current_maze_y = (self.rect.centery - OFFSET_Y) // TILE_SIZE

        # Check the tile Pac-Man is moving into
        target_maze_x = (new_x + self.image.get_width() // 2 - OFFSET_X) // TILE_SIZE
        target_maze_y = (new_y + self.image.get_height() // 2 - OFFSET_Y) // TILE_SIZE

        can_move_x = True
        if self.dx != 0:
            # Check if the next tile in X direction is a wall
            if 0 <= target_maze_x < len(maze[0]) and 0 <= current_maze_y < len(maze):
                if maze[current_maze_y][target_maze_x] == 1:
                    can_move_x = False

        can_move_y = True
        if self.dy != 0:
            # Check if the next tile in Y direction is a wall
            if 0 <= current_maze_x < len(maze[0]) and 0 <= target_maze_y < len(maze):
                if maze[target_maze_y][current_maze_x] == 1:
                    can_move_y = False

        if can_move_x:
            self.rect.x = new_x
        else:
            self.dx = 0 # Stop movement if hit a wall

        if can_move_y:
            self.rect.y = new_y
        else:
            self.dy = 0 # Stop movement if hit a wall

        # Keep Pac-Man within maze bounds (this is a fallback, wall collision should handle most)
        self.rect.left = max(OFFSET_X, self.rect.left)
        self.rect.right = min(OFFSET_X + MAZE_WIDTH_PX, self.rect.right)
        self.rect.top = max(OFFSET_Y, self.rect.top)
        self.rect.bottom = min(OFFSET_Y + MAZE_HEIGHT_PX, self.rect.bottom)

    def draw(self, surface):
        if self.mouth_open:
            # Draw open mouth
            pygame.draw.circle(surface, YELLOW, self.rect.center, TILE_SIZE // 2 - 2)
            # Determine angle for mouth opening based on direction
            if self.dx > 0: # Right
                start_angle = 0.75 * 3.14159 # 135 degrees
                end_angle = 1.25 * 3.14159 # 225 degrees
            elif self.dx < 0: # Left
                start_angle = -0.25 * 3.14159 # -45 degrees
                end_angle = 0.25 * 3.14159 # 45 degrees
            elif self.dy > 0: # Down
                start_angle = 0.25 * 3.14159 # 45 degrees
                end_angle = 0.75 * 3.14159 # 135 degrees
            elif self.dy < 0: # Up
                start_angle = 1.25 * 3.14159 # 225 degrees
                end_angle = 1.75 * 3.14159 # 315 degrees
            else: # Default (facing right or last direction)
                start_angle = 0.75 * 3.14159
                end_angle = 1.25 * 3.14159

            pygame.draw.arc(surface, BLACK, self.rect, start_angle, end_angle, TILE_SIZE // 2)
            pygame.draw.polygon(surface, BLACK, [self.rect.center, self.rect.topleft, self.rect.bottomleft]) # Simple triangle for mouth
            # Fill the "mouth" part with black to make it look open
            center_x, center_y = self.rect.center
            radius = TILE_SIZE // 2 - 2
            # Calculate points for the triangle that forms the mouth
            # This is a simplification; a true Pac-Man mouth would use more complex geometry.
            # For simplicity, we'll draw a black triangle from the center towards the direction of movement.
            if self.dx > 0: # Right
                mouth_points = [self.rect.center, (center_x + radius, center_y - radius), (center_x + radius, center_y + radius)]
            elif self.dx < 0: # Left
                mouth_points = [self.rect.center, (center_x - radius, center_y - radius), (center_x - radius, center_y + radius)]
            elif self.dy > 0: # Down
                mouth_points = [self.rect.center, (center_x - radius, center_y + radius), (center_x + radius, center_y + radius)]
            elif self.dy < 0: # Up
                mouth_points = [self.rect.center, (center_x - radius, center_y - radius), (center_x + radius, center_y - radius)]
            else: # Default (no movement, draw mouth facing right)
                mouth_points = [self.rect.center, (center_x + radius, center_y - radius), (center_x + radius, center_y + radius)]
            pygame.draw.polygon(surface, BLACK, mouth_points)
        else:
            # Draw closed mouth (full circle)
            pygame.draw.circle(surface, YELLOW, self.rect.center, TILE_SIZE // 2 - 2)

    def reset_position(self):
        self.rect.center = self.start_pos
        self.dx = 0
        self.dy = 0

# Ghost class
class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, color, name):
        super().__init__()
        self.image = pygame.Surface((TILE_SIZE - 4, TILE_SIZE - 4), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.color = color
        self.name = name
        self.dx = 0
        self.dy = 0
        self.is_frightened = False
        self.frightened_timer = 0
        self.start_pos = (x, y) # Store initial position for resetting
        self.target = None # For more advanced ghost AI

    def update(self, pacman_pos, maze_data):
        if self.is_frightened:
            self.frightened_timer -= 1
            if self.frightened_timer <= 0:
                self.is_frightened = False
            # Frightened ghosts move randomly or away from Pac-Man
            self.move_randomly(maze_data)
        else:
            # Basic ghost AI: try to move towards Pac-Man
            self.chase_pacman(pacman_pos, maze_data)

        # Update position
        new_x = self.rect.x + self.dx
        new_y = self.rect.y + self.dy

        # Collision detection with walls for ghosts
        current_maze_x = (self.rect.centerx - OFFSET_X) // TILE_SIZE
        current_maze_y = (self.rect.centery - OFFSET_Y) // TILE_SIZE

        target_maze_x = (new_x + self.image.get_width() // 2 - OFFSET_X) // TILE_SIZE
        target_maze_y = (new_y + self.image.get_height() // 2 - OFFSET_Y) // TILE_SIZE

        can_move_x = True
        if self.dx != 0:
            if 0 <= target_maze_x < len(maze_data[0]) and 0 <= current_maze_y < len(maze_data):
                if maze_data[current_maze_y][target_maze_x] == 1:
                    can_move_x = False

        can_move_y = True
        if self.dy != 0:
            if 0 <= current_maze_x < len(maze_data[0]) and 0 <= target_maze_y < len(maze_data):
                if maze_data[target_maze_y][current_maze_x] == 1:
                    can_move_y = False

        if can_move_x:
            self.rect.x = new_x
        else:
            self.dx = 0

        if can_move_y:
            self.rect.y = new_y
        else:
            self.dy = 0

    def move_randomly(self, maze_data):
        # Simple random movement for now
        possible_moves = []
        current_maze_x = (self.rect.centerx - OFFSET_X) // TILE_SIZE
        current_maze_y = (self.rect.centery - OFFSET_Y) // TILE_SIZE

        # Check up
        if current_maze_y > 0 and maze_data[current_maze_y - 1][current_maze_x] != 1:
            possible_moves.append((0, -GHOST_SPEED))
        # Check down
        if current_maze_y < len(maze_data) - 1 and maze_data[current_maze_y + 1][current_maze_x] != 1:
            possible_moves.append((0, GHOST_SPEED))
        # Check left
        if current_maze_x > 0 and maze_data[current_maze_y][current_maze_x - 1] != 1:
            possible_moves.append((-GHOST_SPEED, 0))
        # Check right
        if current_maze_x < len(maze_data[0]) - 1 and maze_data[current_maze_y][current_maze_x + 1] != 1:
            possible_moves.append((GHOST_SPEED, 0))

        if possible_moves:
            self.dx, self.dy = random.choice(possible_moves)
        else:
            self.dx, self.dy = 0, 0 # Stop if no valid moves

    def chase_pacman(self, pacman_pos, maze_data):
        # Very basic chasing: move towards Pac-Man's general direction
        # This is not sophisticated pathfinding, just direct movement.
        target_x, target_y = pacman_pos

        current_x, current_y = self.rect.center

        # Try to move horizontally first, then vertically
        if abs(target_x - current_x) > abs(target_y - current_y):
            if target_x > current_x:
                self.dx = GHOST_SPEED
                self.dy = 0
            elif target_x < current_x:
                self.dx = -GHOST_SPEED
                self.dy = 0
            else: # Aligned horizontally, try vertical
                if target_y > current_y:
                    self.dy = GHOST_SPEED
                    self.dx = 0
                elif target_y < current_y:
                    self.dy = -GHOST_SPEED
                    self.dx = 0
                else: # At target, stop
                    self.dx = 0
                    self.dy = 0
        else: # Try to move vertically first, then horizontally
            if target_y > current_y:
                self.dy = GHOST_SPEED
                self.dx = 0
            elif target_y < current_y:
                self.dy = -GHOST_SPEED
                self.dx = 0
            else: # Aligned vertically, try horizontal
                if target_x > current_x:
                    self.dx = GHOST_SPEED
                    self.dy = 0
                elif target_x < current_x:
                    self.dx = -GHOST_SPEED
                    self.dy = 0
                else: # At target, stop
                    self.dx = 0
                    self.dy = 0

        # If the chosen direction leads to a wall, try another direction
        # This is a very simple wall avoidance. A real game would use pathfinding.
        current_maze_x = (self.rect.centerx - OFFSET_X) // TILE_SIZE
        current_maze_y = (self.rect.centery - OFFSET_Y) // TILE_SIZE

        next_x_tile = (self.rect.centerx + self.dx * 2 - OFFSET_X) // TILE_SIZE # Look a bit ahead
        next_y_tile = (self.rect.centery + self.dy * 2 - OFFSET_Y) // TILE_SIZE

        if 0 <= next_y_tile < len(maze_data) and 0 <= next_x_tile < len(maze_data[0]):
            if maze_data[next_y_tile][next_x_tile] == 1:
                # If next move hits a wall, try to change direction
                if self.dx != 0: # Was moving horizontally, try vertical
                    self.dx = 0
                    if target_y > current_y: self.dy = GHOST_SPEED
                    elif target_y < current_y: self.dy = -GHOST_SPEED
                elif self.dy != 0: # Was moving vertically, try horizontal
                    self.dy = 0
                    if target_x > current_x: self.dx = GHOST_SPEED
                    elif target_x < current_x: self.dx = -GHOST_SPEED

    def draw(self, surface):
        if self.is_frightened:
            # Draw frightened ghost (blue with white eyes)
            pygame.draw.circle(surface, BLUE, self.rect.center, TILE_SIZE // 2 - 2)
            # Draw eyes
            eye_radius = TILE_SIZE // 8
            pygame.draw.circle(surface, WHITE, (self.rect.centerx - eye_radius * 2, self.rect.centery - eye_radius), eye_radius)
            pygame.draw.circle(surface, WHITE, (self.rect.centerx + eye_radius * 2, self.rect.centery - eye_radius), eye_radius)
            pygame.draw.circle(surface, BLACK, (self.rect.centerx - eye_radius * 2, self.rect.centery - eye_radius), eye_radius // 2)
            pygame.draw.circle(surface, BLACK, (self.rect.centerx + eye_radius * 2, self.rect.centery - eye_radius), eye_radius // 2)
        else:
            # Draw regular ghost
            pygame.draw.circle(surface, self.color, self.rect.center, TILE_SIZE // 2 - 2)
            # Draw eyes
            eye_radius = TILE_SIZE // 8
            pygame.draw.circle(surface, WHITE, (self.rect.centerx - eye_radius * 2, self.rect.centery - eye_radius), eye_radius)
            pygame.draw.circle(surface, WHITE, (self.rect.centerx + eye_radius * 2, self.rect.centery - eye_radius), eye_radius)
            pygame.draw.circle(surface, BLACK, (self.rect.centerx - eye_radius * 2 + self.dx // 4, self.rect.centery - eye_radius + self.dy // 4), eye_radius // 2)
            pygame.draw.circle(surface, BLACK, (self.rect.centerx + eye_radius * 2 + self.dx // 4, self.rect.centery - eye_radius + self.dy // 4), eye_radius // 2)

    def reset_position(self):
        self.rect.center = self.start_pos
        self.dx = 0
        self.dy = 0
        self.is_frightened = False
        self.frightened_timer = 0

# Pellet class
class Pellet(pygame.sprite.Sprite):
    def __init__(self, x, y, is_power=False):
        super().__init__()
        self.is_power = is_power
        if self.is_power:
            self.image = pygame.Surface((TILE_SIZE // 2, TILE_SIZE // 2), pygame.SRCALPHA)
            pygame.draw.circle(self.image, WHITE, (TILE_SIZE // 4, TILE_SIZE // 4), TILE_SIZE // 4)
        else:
            self.image = pygame.Surface((TILE_SIZE // 4, TILE_SIZE // 4), pygame.SRCALPHA)
            pygame.draw.circle(self.image, WHITE, (TILE_SIZE // 8, TILE_SIZE // 8), TILE_SIZE // 8)
        self.rect = self.image.get_rect(center=(x, y))

# Game setup
def setup_game():
    global pacman, all_sprites, ghosts, pellets, total_pellets

    # Calculate initial Pac-Man position (center of a path tile)
    pacman_start_x = OFFSET_X + TILE_SIZE * 1 + TILE_SIZE // 2
    pacman_start_y = OFFSET_Y + TILE_SIZE * 1 + TILE_SIZE // 2
    pacman = PacMan(pacman_start_x, pacman_start_y)

    all_sprites = pygame.sprite.Group()
    ghosts = pygame.sprite.Group()
    pellets = pygame.sprite.Group()

    all_sprites.add(pacman)

    total_pellets = 0

    # Populate maze with pellets and set ghost starting positions
    ghost_start_positions = []
    for row_idx, row in enumerate(maze):
        for col_idx, tile_type in enumerate(row):
            center_x = OFFSET_X + col_idx * TILE_SIZE + TILE_SIZE // 2
            center_y = OFFSET_Y + row_idx * TILE_SIZE + TILE_SIZE // 2

            if tile_type == 2: # Pellet
                pellets.add(Pellet(center_x, center_y, is_power=False))
                total_pellets += 1
            elif tile_type == 3: # Power Pellet
                pellets.add(Pellet(center_x, center_y, is_power=True))
                total_pellets += 1
            elif tile_type == 4: # Ghost home (placeholder, actual ghost positions are hardcoded for now)
                pass # No pellet here

    # Initial ghost positions (adjust these to be within the maze paths)
    # These coordinates need to be carefully chosen to be on walkable paths.
    ghost_start_positions.append((OFFSET_X + TILE_SIZE * 18 + TILE_SIZE // 2, OFFSET_Y + TILE_SIZE * 7 + TILE_SIZE // 2)) # Blinky (Red)
    ghost_start_positions.append((OFFSET_X + TILE_SIZE * 19 + TILE_SIZE // 2, OFFSET_Y + TILE_SIZE * 7 + TILE_SIZE // 2)) # Pinky (Pink)
    ghost_start_positions.append((OFFSET_X + TILE_SIZE * 20 + TILE_SIZE // 2, OFFSET_Y + TILE_SIZE * 7 + TILE_SIZE // 2)) # Inky (Cyan)
    ghost_start_positions.append((OFFSET_X + TILE_SIZE * 21 + TILE_SIZE // 2, OFFSET_Y + TILE_SIZE * 7 + TILE_SIZE // 2)) # Clyde (Orange)

    ghosts.add(Ghost(ghost_start_positions[0][0], ghost_start_positions[0][1], RED, "Blinky"))
    ghosts.add(Ghost(ghost_start_positions[1][0], ghost_start_positions[1][1], PINK, "Pinky"))
    ghosts.add(Ghost(ghost_start_positions[2][0], ghost_start_positions[2][1], CYAN, "Inky"))
    ghosts.add(Ghost(ghost_start_positions[3][0], ghost_start_positions[3][1], ORANGE, "Clyde"))

    for ghost in ghosts:
        all_sprites.add(ghost)

# Draw the maze
def draw_maze(surface, maze_data):
    for row_idx, row in enumerate(maze_data):
        for col_idx, tile_type in enumerate(row):
            x = OFFSET_X + col_idx * TILE_SIZE
            y = OFFSET_Y + row_idx * TILE_SIZE
            if tile_type == 1: # Wall
                pygame.draw.rect(surface, BLUE, (x, y, TILE_SIZE, TILE_SIZE), 2) # Draw wall outline

# Display score and lives
def draw_hud(surface, score, lives):
    font = pygame.font.Font(None, FONT_SIZE)
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    surface.blit(score_text, (10, 10))
    surface.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 10, 10))

# Game over screen
def game_over_screen(surface, score, win=False):
    font = pygame.font.Font(None, FONT_SIZE * 2)
    message = "GAME OVER!"
    color = RED
    if win:
        message = "YOU WIN!"
        color = YELLOW

    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    surface.blit(text, text_rect)

    score_text = font.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))
    surface.blit(score_text, score_rect)

    restart_text = pygame.font.Font(None, FONT_SIZE).render("Press R to Restart or Q to Quit", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100))
    surface.blit(restart_text, restart_rect)

    pygame.display.flip()

    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True # Restart game
                if event.key == pygame.K_q:
                    pygame.quit()
                    exit()
        pygame.time.Clock().tick(30) # Limit frame rate while waiting for input

# Main game loop
def game_loop():
    setup_game()
    running = True
    game_over = False
    game_won = False
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        pacman.dx = -PACMAN_SPEED
                        pacman.dy = 0
                    elif event.key == pygame.K_RIGHT:
                        pacman.dx = PACMAN_SPEED
                        pacman.dy = 0
                    elif event.key == pygame.K_UP:
                        pacman.dy = -PACMAN_SPEED
                        pacman.dx = 0
                    elif event.key == pygame.K_DOWN:
                        pacman.dy = PACMAN_SPEED
                        pacman.dx = 0

        if not game_over:
            # Update Pac-Man
            pacman.update()

            # Pellet collision
            pellet_hits = pygame.sprite.spritecollide(pacman, pellets, True)
            for pellet in pellet_hits:
                if pellet.is_power:
                    pacman.score += 50
                    # Frighten ghosts
                    for ghost in ghosts:
                        ghost.is_frightened = True
                        ghost.frightened_timer = 300 # Frightened for 5 seconds (300 frames at 60 FPS)
                else:
                    pacman.score += 10

            # Update ghosts
            for ghost in ghosts:
                ghost.update(pacman.rect.center, maze)

            # Ghost collision
            ghost_hits = pygame.sprite.spritecollide(pacman, ghosts, False)
            for ghost in ghost_hits:
                if ghost.is_frightened:
                    pacman.score += 200 # Score for eating frightened ghost
                    ghost.reset_position() # Send ghost back to starting point
                    ghost.is_frightened = False # Ghost is no longer frightened
                else:
                    # Pac-Man hit by a regular ghost
                    pacman.lives -= 1
                    if pacman.lives <= 0:
                        game_over = True
                    else:
                        # Reset positions after losing a life
                        pacman.reset_position()
                        for g in ghosts:
                            g.reset_position()

            # Check for win condition
            if not pellets: # All pellets eaten
                game_over = True
                game_won = True

        # Drawing
        screen.fill(BLACK)
        draw_maze(screen, maze)
        pellets.draw(screen) # Draw all pellets
        pacman.draw(screen) # Draw Pac-Man
        for ghost in ghosts: # Draw all ghosts
            ghost.draw(screen)
        draw_hud(screen, pacman.score, pacman.lives)

        pygame.display.flip()

        if game_over:
            if game_over_screen(screen, pacman.score, game_won):
                # Restart game
                game_loop()
                return # Exit current game loop
            else:
                running = False # Quit game

        clock.tick(60) # Limit to 60 FPS

    pygame.quit()
    exit()

if __name__ == "__main__":
    game_loop()
