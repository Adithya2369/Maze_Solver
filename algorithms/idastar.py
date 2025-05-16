# ai_maze_solver/algorithms/idastar.py
import math

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def idastar(maze, start, end):
    threshold = heuristic(start, end)
    visited = set()

    def search(path, g, threshold):
        node = path[-1]
        f = g + heuristic(node, end)
        if f > threshold:
            return f
        if node == end:
            return path
        min_threshold = float('inf')
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = node[0] + dr, node[1] + dc
            neighbor = (nr, nc)
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0 and neighbor not in path:
                path.append(neighbor)
                visited.add(neighbor)
                result = search(path, g + 1, threshold)
                if isinstance(result, list):
                    return result
                if result < min_threshold:
                    min_threshold = result
                path.pop()
        return min_threshold

    while True:
        path = [start]
        result = search(path, 0, threshold)
        if isinstance(result, list):
            return result, visited
        if result == float('inf'):
            return [], visited
        threshold = result
