# Chess Analysis Tool (CAT)

## Overview

This tool is designed for chess enthusiasts who want to analyze chess positions deeply and explore different possible continuations of a game. Using the powerful Stockfish engine, the tool helps you to understand various potential moves and their outcomes, providing a comprehensive view of possible game variations. It is a great resource for assisting with the developement of chess repertoires and saves countless of hours of sitting at a computer trying to analyze positions with an engine.

## Features

- Recursive analysis up to a specified depth.
- Selection of top moves using Stockfish.
- Time estimation for analysis.
- Merging of multiple PGN variations.
- Memoization for performance optimization.

## Configuration
Download git [here](https://git-scm.com/downloads) and open powershell and run these commands (ensure you have python 3.11 or higher installed on your system):

```sh
git clone https://github.com/your-repo/chess-analysis-tool.git
cd chess-analysis-tool
```
Then install the necessary packages:

```sh
pip install numpy scipy chess
```
Finally:

Make sure you have downloaded [this](https://drive.google.com/file/d/1O27-UqW9zm2HAs3X3bpBrGtBVYVhD_9_/view?usp=drive_link) specific version of stockfish. Once downloaded, copy the file path of the executable and update the path variable at the top of the script:

```python
from functools import lru_cache
import io
from time import time

import chess
import chess.engine
import chess.pgn
import numpy as np
from scipy.interpolate import interp1d


# Path to the Stockfish engine executable
STOCKFISH_PATH = r'path\to\stockfish'
engine = chess.engine.SimpleEngine.popen_uci(STOCKFISH_PATH)
```

After which you can run the python file and use the script!

```sh
python main.py
```

## Conclusion

Chess Analysis Tool (for any name suggestions or questions, hmu on discord @justjustinjr) is very useful at creating opening repertoires. I personally use this along with the chesstempo Opening Trainer to traing my openings, I will improve this program over time. Lastly, thank you to [permutationlock](https://github.com/permutationlock) for his program that merges pgns together, I use an adapted version of it for this project. As I've stated, message me on discord @justjustinjr, I'm also in .gg/chess
