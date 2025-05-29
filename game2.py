import tkinter as tk
from tkinter import ttk, messagebox
import random
from collections import deque
import heapq

# --- Prompt for maze size before main window ---
class MazeSizePrompt:
    def __init__(self, root):
        self.root = root
        self.root.title("Enter Maze Size")
        self.size = None

        tk.Label(root, text="Enter maze size (5-200):").pack(padx=10, pady=(10, 0))
        self.entry = tk.Entry(root)
        self.entry.pack(padx=10, pady=5)
        self.entry.focus()
        tk.Button(root, text="Start", command=self.submit).pack(pady=(0, 10))
        self.root.bind('<Return>', lambda event: self.submit())

    def submit(self):
        try:
            size = int(self.entry.get())
            if size < 5 or size > 200:
                raise ValueError
            self.size = size
            self.root.destroy()
        except Exception:
            messagebox.showerror("Invalid input", "Please enter an integer between 5 and 200.")

def get_maze_size():
    prompt_root = tk.Tk()
    prompt = MazeSizePrompt(prompt_root)
    prompt_root.mainloop()
    return prompt.size if prompt.size else 20

# --- Main Maze Solver ---
class MazeSolver:
    def __init__(self, size=20):
        self.size = size
        self.start = (0, 0)
        self.end = (size-1, size-1)
        self.cell_size = max(8, 400 // size)

        self.root = tk.Tk()
        self.root.title("AI Maze Solver")

        # Main frame for centering
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill='both')

        # Controls (centered)
        self.controls_frame = tk.Frame(self.main_frame)
        self.controls_frame.pack(pady=10)

        self.algo_var = tk.StringVar()
        # self.combo = ttk.Combobox(self.controls_frame, textvariable=self.algo_var,
        #                           values=["BFS", "DFS", "A*", "IDA*"], width=10)
        self.combo = ttk.Combobox(self.controls_frame, textvariable=self.algo_var,
                                    values=["BFS", "DFS", "A*"], width=10)
        self.combo.grid(row=0, column=0, padx=5)
        self.generate_btn = tk.Button(self.controls_frame, text="Generate Maze", command=self.generate_maze)
        self.generate_btn.grid(row=0, column=1, padx=5)
        self.solve_btn = tk.Button(self.controls_frame, text="Solve", command=self.solve_maze)
        self.solve_btn.grid(row=0, column=2, padx=5)
        self.clear_btn = tk.Button(self.controls_frame, text="Clear Path", command=self.clear_path)
        self.clear_btn.grid(row=0, column=3, padx=5)

        # Canvas with scrollbars
        self.canvas_frame = tk.Frame(self.main_frame)
        self.canvas_frame.pack(expand=True, fill='both', padx=10, pady=10)

        canvas_width = min(600, self.size * self.cell_size)
        canvas_height = min(600, self.size * self.cell_size)
        self.canvas = tk.Canvas(self.canvas_frame, width=canvas_width, height=canvas_height, bg='white')
        self.canvas.grid(row=0, column=0, sticky='nsew')

        # Scrollbars
        self.vbar = tk.Scrollbar(self.canvas_frame, orient='vertical', command=self.canvas.yview)
        self.vbar.grid(row=0, column=1, sticky='ns')
        self.hbar = tk.Scrollbar(self.canvas_frame, orient='horizontal', command=self.canvas.xview)
        self.hbar.grid(row=1, column=0, sticky='ew')
        self.canvas.config(yscrollcommand=self.vbar.set, xscrollcommand=self.hbar.set)

        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        self.generate_maze()

    def generate_maze(self):
        # Generate initial maze with Prim's algorithm
        self.maze = [[1 for _ in range(self.size)] for _ in range(self.size)]
        front = []
        sx, sy = self.start
        self.maze[sx][sy] = 0
        front.extend(self.get_frontiers(sx, sy))
        while front:
            x, y = random.choice(front)
            front.remove((x, y))
            neighbors = self.get_neighbors(x, y)
            if neighbors:
                nx, ny = random.choice(neighbors)
                self.maze[x][y] = 0
                self.maze[(x + nx)//2][(y + ny)//2] = 0
            for f in self.get_frontiers(x, y):
                if f not in front:
                    front.append(f)
        # Add loops for complexity
        for _ in range(self.size * 5):
            x = random.randint(0, self.size-1)
            y = random.randint(0, self.size-1)
            if self.maze[x][y] == 1:
                self.maze[x][y] = 0
        # Guarantee a path: carve a direct path if not connected
        if not self.path_exists():
            self.carve_direct_path()
        # Set start/end markers
        self.maze[sx][sy] = 2
        ex, ey = self.end
        self.maze[ex][ey] = 3
        self.draw_maze()

    def carve_direct_path(self):
        x, y = self.start
        ex, ey = self.end
        while x != ex:
            x += 1 if x < ex else -1
            self.maze[x][y] = 0
        while y != ey:
            y += 1 if y < ey else -1
            self.maze[x][y] = 0

    def get_frontiers(self, x, y):
        return [(x+dx, y+dy) for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]
                if 0 <= x+dx < self.size and 0 <= y+dy < self.size and self.maze[x+dx][y+dy] == 1]

    def get_neighbors(self, x, y):
        return [(x+dx, y+dy) for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]
                if 0 <= x+dx < self.size and 0 <= y+dy < self.size and self.maze[x+dx][y+dy] == 0]

    def draw_maze(self):
        self.canvas.delete("all")
        width = self.size * self.cell_size
        height = self.size * self.cell_size
        self.canvas.config(scrollregion=(0, 0, width, height))
        for i in range(self.size):
            for j in range(self.size):
                color = "white"
                if self.maze[i][j] == 1:
                    color = "black"
                elif self.maze[i][j] == 2:
                    color = "green"
                elif self.maze[i][j] == 3:
                    color = "red"
                self.canvas.create_rectangle(
                    j*self.cell_size, i*self.cell_size,
                    (j+1)*self.cell_size, (i+1)*self.cell_size,
                    fill=color, outline="gray"
                )

    def clear_path(self):
        # Redraw maze but leave start/end/walls untouched, erase blue path
        for i in range(self.size):
            for j in range(self.size):
                if self.maze[i][j] == 0:
                    self.canvas.create_rectangle(
                        j*self.cell_size, i*self.cell_size,
                        (j+1)*self.cell_size, (i+1)*self.cell_size,
                        fill="white", outline="gray"
                    )
                elif self.maze[i][j] == 2:
                    self.canvas.create_rectangle(
                        j*self.cell_size, i*self.cell_size,
                        (j+1)*self.cell_size, (i+1)*self.cell_size,
                        fill="green", outline="gray"
                    )
                elif self.maze[i][j] == 3:
                    self.canvas.create_rectangle(
                        j*self.cell_size, i*self.cell_size,
                        (j+1)*self.cell_size, (i+1)*self.cell_size,
                        fill="red", outline="gray"
                    )
                elif self.maze[i][j] == 1:
                    self.canvas.create_rectangle(
                        j*self.cell_size, i*self.cell_size,
                        (j+1)*self.cell_size, (i+1)*self.cell_size,
                        fill="black", outline="gray"
                    )

    def solve_maze(self):
        try:
            algorithm = self.algo_var.get()
            if not algorithm:
                raise ValueError("Please select an algorithm first!")
            if not self.path_exists():
                raise ValueError("No valid path exists!")
            self.path = []
            self.visited = set()
            self.start = (0, 0)
            self.end = (self.size-1, self.size-1)
            if algorithm == "BFS":
                self.bfs()
            elif algorithm == "DFS":
                self.dfs()
            elif algorithm == "A*":
                self.a_star()
            # elif algorithm == "IDA*":
            #     self.ida_star()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def path_exists(self):
        queue = deque([self.start])
        visited = set()
        while queue:
            current = queue.popleft()
            if current == self.end:
                return True
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current[0]+dx, current[1]+dy
                if 0 <= nx < self.size and 0 <= ny < self.size and \
                   self.maze[nx][ny] != 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append((nx, ny))
        return False

    # BFS
    def bfs(self):
        queue = deque([(self.start, [])])
        visited = set()
        while queue:
            current, path = queue.popleft()
            if current == self.end:
                self.animate_path(path + [current])
                return
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current[0]+dx, current[1]+dy
                if 0 <= nx < self.size and 0 <= ny < self.size and \
                   self.maze[nx][ny] != 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    queue.append(((nx, ny), path + [current]))

    # DFS
    def dfs(self):
        stack = [(self.start, [])]
        visited = set()
        while stack:
            current, path = stack.pop()
            if current == self.end:
                self.animate_path(path + [current])
                return
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current[0]+dx, current[1]+dy
                if 0 <= nx < self.size and 0 <= ny < self.size and \
                   self.maze[nx][ny] != 1 and (nx, ny) not in visited:
                    visited.add((nx, ny))
                    stack.append(((nx, ny), path + [current]))

    # A*
    def a_star(self):
        def heuristic(a, b):
            return abs(a[0]-b[0]) + abs(a[1]-b[1])
        heap = []
        heapq.heappush(heap, (0, self.start, []))
        visited = set()
        while heap:
            cost, current, path = heapq.heappop(heap)
            if current == self.end:
                self.animate_path(path + [current])
                return
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = current[0]+dx, current[1]+dy
                if 0 <= nx < self.size and 0 <= ny < self.size and \
                   self.maze[nx][ny] != 1 and (nx, ny) not in visited:
                    new_cost = len(path) + 1 + heuristic(self.end, (nx, ny))
                    visited.add((nx, ny))
                    heapq.heappush(heap, (new_cost, (nx, ny), path + [current]))

    # # IDA*
    # def ida_star(self):
    #     def heuristic(a):
    #         return abs(a[0]-self.end[0]) + abs(a[1]-self.end[1])
    #     threshold = heuristic(self.start)
    #     path = [self.start]
    #     while True:
    #         temp = self.ida_search(path, 0, threshold, heuristic)
    #         if temp == "FOUND":
    #             self.animate_path(path)
    #             return
    #         if temp == float('inf'):
    #             return
    #         threshold = temp

    # def ida_search(self, path, g, threshold, heuristic):
    #     current = path[-1]
    #     f = g + heuristic(current)
    #     if f > threshold:
    #         return f
    #     if current == self.end:
    #         return "FOUND"
    #     min_cost = float('inf')
    #     for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
    #         nx, ny = current[0]+dx, current[1]+dy
    #         if 0 <= nx < self.size and 0 <= ny < self.size and \
    #            self.maze[nx][ny] != 1 and (nx, ny) not in path:
    #             path.append((nx, ny))
    #             temp = self.ida_search(path, g+1, threshold, heuristic)
    #             if temp == "FOUND":
    #                 return "FOUND"
    #             if temp < min_cost:
    #                 min_cost = temp
    #             path.pop()
    #     return min_cost

    def animate_path(self, path):
        for i, (x, y) in enumerate(path):
            self.canvas.after(1*i, self.draw_cell, x, y, "blue")
        self.canvas.after(1*len(path), self.draw_final_path, path)

    def draw_cell(self, x, y, color):
        if self.maze[x][y] == 2:
            color = "green"
        elif self.maze[x][y] == 3:
            color = "red"
        self.canvas.create_rectangle(
            y*self.cell_size, x*self.cell_size,
            (y+1)*self.cell_size, (x+1)*self.cell_size,
            fill=color, outline="gray"
        )

    def draw_final_path(self, path):
        for x, y in path:
            self.draw_cell(x, y, "blue")

if __name__ == "__main__":
    size = get_maze_size()
    app = MazeSolver(size=size)
    app.root.mainloop()
