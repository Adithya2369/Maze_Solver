# ai_maze_solver/algorithms/dfs.py
def dfs(maze, start, end):
    stack = [start]
    visited = set()
    parent = {}
    rows, cols = len(maze), len(maze[0])

    while stack:
        node = stack.pop()
        if node in visited:
            continue
        visited.add(node)
        if node == end:
            break
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
            nr, nc = node[0] + dr, node[1] + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr,nc) not in visited:
                parent[(nr,nc)] = node
                stack.append((nr,nc))

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
