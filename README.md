# AI Maze Solver

![Maze Solver Demo](demo.gif) *(example GIF placeholder)*

## Overview
The AI Maze Solver is a Python application that generates random mazes and demonstrates various pathfinding algorithms to solve them. It provides a visual representation of how different algorithms explore and find paths through mazes.

## Features
- Generates random mazes using Prim's algorithm
- Solves mazes using multiple pathfinding algorithms:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search Algorithm
- Adjustable maze size (5x5 to 200x200)
- Interactive visualization of the solving process
- Clear visualization of the final path

## Requirements
- Python 3.8 or above is suggested, but the code will work same with any Python 3.x
- tkinter (usually included with Python)
- Standard Python libraries (random, collections, heapq)

## Installation
1. Clone the repository or download the Python script
2. Ensure Python 3.8 or above is installed on your system
3. No additional packages are required beyond standard Python libraries

## Usage
1. Run the script: `python maze.py`
2. Enter your desired maze size (between 5 and 200) when prompted
3. Use the interface controls:
   - **Algorithm Selection**: Choose from BFS, DFS, or A*
   - **Generate Maze**: Create a new random maze
   - **Solve**: Run the selected algorithm on the current maze
   - **Clear Path**: Remove the current solution path

## How It Works

### Maze Generation
The maze is generated using a modified version of Prim's algorithm:
1. Starts with a grid of walls
2. Randomly carves out passages to create a maze
3. Adds additional loops for complexity
4. Guarantees at least one valid path from start to finish

### Pathfinding Algorithms

#### Breadth-First Search (BFS)
- Explores all neighbors at the present depth before moving deeper
- Guaranteed to find the shortest path
- Uses a queue data structure

#### Depth-First Search (DFS)
- Explores as far as possible along each branch before backtracking
- Doesn't guarantee the shortest path
- Uses a stack data structure

#### A* Search
- Uses both the actual cost from start and heuristic cost to goal
- Heuristic is Manhattan distance to the endpoint
- Efficiently finds the shortest path
- Uses a priority queue (heap)

### Visualization
- **Black cells**: Walls/obstacles
- **White cells**: Passable areas
- **Green cell**: Start position (top-left corner)
- **Red cell**: End position (bottom-right corner)
- **Blue cells**: Solution path (when solved)

## Code Structure
The main components of the code are:

1. **MazeSizePrompt**: Initial dialog to get maze size from user
2. **MazeSolver**: Main application class containing:
   - Maze generation logic
   - Pathfinding algorithm implementations
   - Visualization methods
   - UI controls

Key methods:
- `generate_maze()`: Creates the random maze
- `solve_maze()`: Dispatches to the selected algorithm
- `bfs()/dfs()/a_star()`: Algorithm implementations
- `animate_path()`: Visualizes the solving process

## Customization
You can modify the code to:
- Change colors by editing the `draw_cell()` method
- Adjust maze generation parameters in `generate_maze()`
- Add new algorithms by implementing them and adding to the combo box

## Limitations
- Very large mazes (>100x100) may have performance issues
- Visualization may be too fast on small mazes (can adjust animation speed)

## Future Enhancements
Potential improvements:
- Add more algorithms (Dijkstra's, Greedy Best-First Search)
- Allow custom start/end positions
- Add maze saving/loading functionality
- Implement maze editing tools
- Add speed controls for visualization

## License
This project is open-source and available under the MIT License.

---

*To run the application, simply execute the Python script and follow the on-screen instructions.*
