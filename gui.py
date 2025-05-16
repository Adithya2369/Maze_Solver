# ai_maze_solver/gui.py
import tkinter as tk
from tkinter import ttk
from maze_generator import generate_maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar
from algorithms.idastar import idastar
import time

CELL_SIZE = 25

class MazeSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Maze Solver")
        self.rows = 20
        self.cols = 20
        self.canvas = tk.Canvas(root, width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE, bg="white")
        self.canvas.pack()

        self.algorithm = tk.StringVar(value="BFS")
        ttk.Label(root, text="Algorithm:").pack()
        ttk.Combobox(root, textvariable=self.algorithm, values=["BFS", "DFS", "A*", "IDA*"], state="readonly").pack()

        ttk.Button(root, text="Generate Maze", command=self.new_maze).pack()
        ttk.Button(root, text="Solve", command=self.solve_maze).pack()

        self.new_maze()

    def new_maze(self):
        self.maze, self.start, self.end = generate_maze(self.rows, self.cols)
        self.draw_maze()

    def draw_maze(self, path=None, visited=None):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * CELL_SIZE, r * CELL_SIZE
                x2, y2 = x1 + CELL_SIZE, y1 + CELL_SIZE
                if (r, c) == self.start:
                    color = "green"
                elif (r, c) == self.end:
                    color = "red"
                elif self.maze[r][c] == 1:
                    color = "black"
                elif visited and (r, c) in visited:
                    color = "yellow"
                elif path and (r, c) in path:
                    color = "purple"
                else:
                    color = "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def solve_maze(self):
        if self.algorithm.get() == "BFS":
            path, visited = bfs(self.maze, self.start, self.end)
        elif self.algorithm.get() == "DFS":
            path, visited = dfs(self.maze, self.start, self.end)
        elif self.algorithm.get() == "A*":
            path, visited = astar(self.maze, self.start, self.end)
        elif self.algorithm.get() == "IDA*":
            path, visited = idastar(self.maze, self.start, self.end)
        else:
            return
        self.draw_maze(path, visited)