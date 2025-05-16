# ai_maze_solver/maze_generator.py
import random

def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    start = (0, 0)
    end = (rows - 1, cols - 1)
    stack = [start]
    maze[start[0]][start[1]] = 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        current = stack[-1]
        r, c = current
        neighbors = []
        for dr, dc in directions:
            nr, nc = r + dr*2, c + dc*2
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 1:
                neighbors.append((nr, nc, dr, dc))
        if neighbors:
            nr, nc, dr, dc = random.choice(neighbors)
            maze[r + dr][c + dc] = 0
            maze[nr][nc] = 0
            stack.append((nr, nc))
        else:
            stack.pop()

    maze[end[0]][end[1]] = 0
    return maze, start, end