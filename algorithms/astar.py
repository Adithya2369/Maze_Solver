# ai_maze_solver/algorithms/astar.py
import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar(maze, start, end):
    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {}
    g_score = {start: 0}
    visited = set()

    while open_set:
        _, current = heapq.heappop(open_set)
        visited.add(current)
        if current == end:
            break
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = current[0] + dr, current[1] + dc
            neighbor = (nr, nc)
            if 0 <= nr < len(maze) and 0 <= nc < len(maze[0]) and maze[nr][nc] == 0:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f, neighbor))
                    parent[neighbor] = current

    path = []
    node = end
    while node != start:
        path.append(node)
        node = parent.get(node)
        if node is None:
            return [], visited
    path.append(start)
    path.reverse()
    return path, visited