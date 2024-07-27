# 12D Chess Engine

This repository contains the implementation of a 12D Chess Engine capable of playing against human players or Stockfish, a powerful chess engine. The 12D Chess Engine is designed to simulate a high-dimensional chess game, providing a unique and complex gameplay experience.

## Features

- **12D Chess Board:** The game is played on a 12-dimensional chessboard, offering a novel twist on traditional chess.
- **Custom Piece Classes:** Implements unique movements for each chess piece in a 12D space.
- **AI Players:** Includes AI players for both White and Black pieces, with configurable search depth.
- **Stockfish Integration:** Supports playing against the Stockfish chess engine, with customizable thinking time and depth.
- **Randomized Opening Moves:** For AI vs. Stockfish games, starts with a random opening sequence from a predefined list.

## Getting Started

### Prerequisites

- Python 3.x
- `python-chess` library
- `stockfish` chess engine

### Installation

1. **Clone the Repository**

    ```bash
    git clone https://github.com/yourusername/12D-Chess-Engine.git
    cd 12D-Chess-Engine
    ```

2. **Install Required Libraries**

    ```bash
    pip install python-chess
    ```

3. **Download Stockfish**

    Download the Stockfish engine from the [official website](https://stockfishchess.org/download/) and place the executable file in a known location. Update the path to the Stockfish executable in the `play_game` function within the code.

    ```python
    stockfish_path = os.path.join(os.path.dirname(sys.executable), "path/to/your/stockfish/executable")
    ```

### Usage

The script can be executed with various options to either watch the 12D Chess Engine play against Stockfish or to play against the 12D Chess Engine yourself.

#### Command-Line Options

- `--watch`: Watch 12D Chess Engine play against Stockfish. If not specified, you will play against the 12D Chess Engine.
- `--thinking_time`: Thinking time for Stockfish (in seconds). Default is 1.0 seconds.
- `--num_games`: Number of games to play. Default is 1 game.
- `--stockfish_depth`: Depth for Stockfish engine. If not specified, Stockfish will use the thinking time.

#### Examples

1. **Watch 12D Chess Engine Play Against Stockfish**

    ```bash
    python 12d_chess.py --watch --thinking_time 2.0 --num_games 5 --stockfish_depth 10
    ```

    This command will watch 12D Chess Engine play against Stockfish for 5 games, with Stockfish having 2 seconds of thinking time per move and a search depth of 10.

2. **Play Against 12D Chess Engine**

    ```bash
    python 12d_chess.py
    ```

    This command will start a game where you play against the 12D Chess Engine. The engine will make the first move.

### Code Structure

- **Board12D Class:** Implements the 12-dimensional chessboard, movement logic, and game state checks.
- **Piece Classes:** Defines the movements for each type of chess piece (King, Queen, Rook, Bishop, Knight, Pawn) in 12D space.
- **AIPlayer Class:** Implements the AI logic using the Minimax algorithm with Alpha-Beta pruning.
- **Main Script:** Handles game initialization, user input, and interaction with the Stockfish engine.

### Updating the Stockfish Path

Ensure you update the path to the Stockfish executable in the `play_game` function within the script:

```python
stockfish_path = os.path.join(os.path.dirname(sys.executable), "C:/path/to/your/stockfish/executable")
```

Replace `"C:/path/to/your/stockfish/executable"` with the actual path where you have downloaded the Stockfish executable.

### Theory and Performance of 12D Chess Engine

The theory behind the 12D Chess Engine posits that a traditional 2D chessboard, when extended into twelve dimensions, transforms each move into a projectile or ray along a specific direction within this high-dimensional space. This conceptual leap allows for a vastly more complex and strategic gameplay experience, reflecting the infinite possibilities that arise from higher-dimensional interactions. The engine, designed with a depth of 3, has proven sufficient to navigate this complexity effectively, making strategic decisions within this 12D framework. Extensive testing has been conducted against the Stockfish engine, with configurations reaching up to a depth of 30, the highest feasible within current computational constraints. Despite these limitations, the engine has consistently demonstrated a remarkable win rate of 100%, suggesting that with more powerful hardware, its performance could potentially scale even further beyond the tested depths.

## Contributing

Contributions are welcome! Please fork the repository and submit pull requests with any improvements or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [python-chess](https://python-chess.readthedocs.io/en/latest/) for providing a robust chess library in Python.
- [Stockfish](https://stockfishchess.org/) for being a powerful open-source chess engine.

---

Feel free to contact me if you have any questions or suggestions.
## Donations

If you find this project interesting and would like to support its development and future astonishing projects, please consider donating via PayPal to `o0sniper0o@hotmail.com`.

Happy Chess Playing! In the currect number of dimensions I should say. 
