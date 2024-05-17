# Othello Board Game

This repository contains a Python implementation of the Othello board game with a Human vs. Computer mode. The computer utilizes the alpha-beta pruning algorithm to decide on moves, with three different difficulty levels available: easy, medium, and hard.

## Table of Contents

- [About the Game](#about-the-game)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Rules](#game-rules)
- [License](#license)

## About the Game

Othello is a strategy board game for two players, played on an 8×8 uncheckered board. Players take turns placing disks on the board with their assigned color facing up. After a play is made, any disks of the opponent's color that lie in a straight line bounded by the one just played and another one in the current player's color are turned over.

## Features

- Human vs. Computer mode
- Alpha-beta pruning algorithm for computer moves
- Three difficulty levels:
  - Easy (depth 1)
  - Medium (depth 3)
  - Hard (depth 5)
- Graphical User Interface (GUI) using Tkinter
- Valid move highlighting for human player

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/othello-game.git
    ```

2. Change into the project directory:
    ```sh
    cd othello-game
    ```

3. Install the required dependencies (Tkinter is typically included with Python, but you can install it via your package manager if necessary).

## Usage

To start the game, run the `main.py` file:
```sh
python main.py
```

When the game starts, you will be prompted to choose the difficulty level. The game will then proceed with the computer playing as Black and the human player as White. Use the GUI to make your moves by clicking on the valid squares highlighted in red.

## Game Rules

1. **Initial Setup**:
   - The game begins with two black disks and two white disks at the center of the board.
   - Black always moves first.

2. **Making a Move**:
   - Players must place their disk on an empty square adjacent to an opponent's piece.
   - The move must outflank one or more of the opponent's disks, which are then flipped to the player's color.

3. **Skipping Turns**:
   - If a player cannot outflank and flip at least one opposing disk, they miss their turn.

4. **End of the Game**:
   - The game ends when no more legal moves are available for either player.
   - The player with the majority of disks in their color wins.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Enjoy playing Othello! If you have any questions or encounter any issues, please open an issue on GitHub.
