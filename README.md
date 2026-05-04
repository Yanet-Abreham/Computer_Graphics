🎥 Demo Video

https://www.loom.com/share/84a11bb77a234249b8828f8161452b2d

🧩 Maze Generator & Solver

Generates a random 20×20 maze using DFS and backtracking, then solves it
— all visualized live in Pygame. Every run produces a different maze with a random start and end point.

🏗️ How the maze is built

Walls are stored in two 2D arrays:

- `north_wall[R+1][C]` — horizontal walls (top/bottom edges of each cell)
- `east_wall[R][C+1]` — vertical walls (left/right edges of each cell)

Every wall starts as `1` (intact). Generation knocks them down as paths open up.

The algorithm starts from a random cell and uses a stack to drive the DFS:

1. Mark the starting cell as visited and push it onto the stack.
2. Check for unvisited neighbors. If one exists, remove the wall between them and push the neighbor.
3. If no unvisited neighbors exist, pop the stack and backtrack.
4. Repeat until the stack is empty — meaning every cell has been visited.

There's also a small 5% chance that an extra wall gets removed during backtracking, 
which punches in a few extra paths and makes the maze less trivially solvable.

🧭 How it's solved

Solving follows the same DFS logic, starting from a random cell on the left edge and 
targeting a random cell on the right edge:

1. Push the start onto the stack and mark it visited.
2. At each step, check neighbors — but only move if the wall between them is actually gone.
3. If no valid move exists, mark the cell as a dead end and pop the stack.
4. Stop when the current position matches the end cell.

🎨 Visualization

The screen updates every frame during both generation and solving. Here's what each visual 
element means:

| Element | Meaning |
|---|---|
| Black lines | Intact walls |
| Green square | Current position |
| Red dot | Active exploration path |
| Blue dot | Backtracked (dead-end) cell |

The y-axis is flipped in the drawing logic so row `0` appears at the bottom, matching a standard
coordinate system.

 ▶️ Getting started

```bash
pip install pygame
python main.py


