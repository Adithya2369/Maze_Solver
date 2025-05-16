# ai_maze_solver/main.py
import tkinter as tk
from gui import MazeSolverGUI

if __name__ == "__main__":
    root = tk.Tk()
    app = MazeSolverGUI(root)
    root.mainloop()