# Chess Variations Analyzer

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Functions Explained](#functions-explained)
- [Limitations](#limitations)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Chess Variations Analyzer is a tool designed to explore and generate variations in chess games using the Stockfish engine. It recursively analyzes positions, selects top moves, and creates a merged PGN (Portable Game Notation) file that encapsulates all these variations. This is particularly useful for players and analysts looking to study different possibilities from a given board position.

## Features

- **Recursive Analysis**: Perform a recursive analysis of the board up to a specified depth.
- **Top Moves Selection**: Select the top moves based on evaluations from the Stockfish engine.
- **Time Estimation**: Estimate the time required for the analysis based on input parameters.
- **PGN Merging**: Merge multiple PGN variations into a single comprehensive PGN file.
- **Memoization**: Optimize performance by caching results of move evaluations.

## Installation

### Requirements

- Python 3.x
- `chess` library
- `numpy` library
- `scipy` library
- Stockfish engine executable

### Steps

1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/chess_variations.git
    cd chess_variations
    ```

2. **Install Dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Download Stockfish**:
    - Download the Stockfish engine from [official Stockfish site](https://stockfishchess.org/download/).
    - Place the Stockfish executable in the project directory and update the `PATH` variable in `main.py` with the correct path to your Stockfish executable.

## Usage

### Running the Program

To run the analysis, execute:
```sh
python main.py
