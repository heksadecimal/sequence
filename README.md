# Sequence 

Sequence is an abstract strategy board-and-card game.

## Requirements

Use the package manager pip to install following packages :-

- Pyqt6
```bash
pip install pyqt6
```

- Pyqt6-charts
```bash
pip install pyqt6-charts
```

## How to play

### Game Rules

- Each card is pictured twice on the game board, and Jacks (while necessary for game strategy) do not appear on the board.

- The player chooses a card from their hand, and places a chip on one of the corresponding spaces of the game board (Example: they choose Ace of Diamonds from their hand and place a chip on the Ace of Diamonds on the board). 

- Jacks have special powers.

- Two-Eyed Jacks can represent any card and may be used to place a chip on any open space on the board.

- One-Eyed Jacks can remove an opponent's token from a space.

### Strategy

- Each corner of the board has a "Free" space that all players can use to their advantage. This space acts as if it has a chip of each color on it at all times. 

- To form rows, chips may be placed vertically, horizontally or diagonally. Each complete row of five (or four and a free corner space) is counted as a sequence. Sequences of the same color may intersect, but only at a single position. 

### Winning 

- The game ends when a player completes 2 sequences.


