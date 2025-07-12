### THIS WAS MADE BY CURSOR WITHOUT PROMPTING IT TO DO SO 

# Breakout Game

A classic Breakout game implementation using Pygame.

## Features

- Classic Breakout gameplay with paddle, ball, and bricks
- Smooth ball physics with realistic bouncing
- Multiple colored brick rows
- Score tracking and lives system
- Pause functionality
- Game over and win states
- Restart capability

## Installation

1. Make sure you have Python 3.6+ installed
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Play

Run the game:
```bash
python breakout.py
```

### Controls

- **Arrow Keys** or **A/D**: Move paddle left/right
- **SPACE**: Pause/Resume game
- **R**: Restart game (when game over or won)
- **ESC**: Quit game

### Game Rules

- Use the paddle to keep the ball from falling below the screen
- Break all the bricks to win
- You have 3 lives
- Each brick destroyed gives you 10 points
- The ball bounces at different angles depending on where it hits the paddle

### Game States

- **Playing**: Normal gameplay
- **Paused**: Game is paused (press SPACE to continue)
- **Game Over**: You've lost all lives (press R to restart)
- **Won**: All bricks destroyed (press R to play again)

## Game Mechanics

- **Ball Physics**: The ball bounces realistically off walls, paddle, and bricks
- **Paddle Control**: Smooth paddle movement with boundary detection
- **Collision Detection**: Precise collision detection for all game objects
- **Scoring System**: Points awarded for each brick destroyed
- **Lives System**: Lose a life when the ball falls below the screen

Enjoy the game! 