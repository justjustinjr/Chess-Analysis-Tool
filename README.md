# Chess Analysis Tool (CAT)

## Overview

The Chess Variations Analyzer is a tool that explores and generates chess game variations using the Stockfish engine. It recursively analyzes positions, selects top moves, and creates a merged PGN file for comprehensive study.

## Features

- Recursive analysis up to a specified depth.
- Selection of top moves using Stockfish.
- Time estimation for analysis.
- Merging of multiple PGN variations.
- Memoization for performance optimization.

## Configuration

Make sure you have downloaded (this)[https://drive.google.com/file/d/1O27-UqW9zm2HAs3X3bpBrGtBVYVhD_9_/view?usp=drive_link] specific version of stockfish.

Set the parameters in `main.py`:

```python
params = {
    'depth': 5,
    'n_top_moves': 3,
    'k_moves_played': 7,
    'time_limit': 0.2
}

moves = ['d2d4', 'f7f5']
```

These parameters initialize the board and control the analysis's depth and breadth

## Conclusion

Chess Analysis Tool (for any name suggestions or questions, hmu on discord @justjustinjr) is very useful at creating opening repertoires. I personally use this along with the chesstempo Opening Trainer to traing my openings, I will improve this program over time. Lastly, thank you to (permutationlock)[https://github.com/permutationlock] for his program that merges pgns together, I use an adapted version of it for this project. As I've stated, message me on discord @justjustinjr, I'm also in .gg/chess
