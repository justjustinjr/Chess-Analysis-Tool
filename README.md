# Chess Variations Analyzer

## Overview

The Chess Variations Analyzer is a tool that explores and generates chess game variations using the Stockfish engine. It recursively analyzes positions, selects top moves, and creates a merged PGN file for comprehensive study.

## Features

- Recursive analysis up to a specified depth.
- Selection of top moves using Stockfish.
- Time estimation for analysis.
- Merging of multiple PGN variations.
- Memoization for performance optimization.

## Examples

### Configuration

Set parameters in `main.py`:

```python
params = {
    'depth': 5,
    'n_top_moves': 3,
    'k_moves_played': 7,
    'time_limit': 0.2
}
moves = ['d2d4', 'f7f5']
