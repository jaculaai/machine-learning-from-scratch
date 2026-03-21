import tkinter as tk
import random
import heapq
import time

# --- KONFIGURACJA ---
CELL = 20
COLS, ROWS = 35, 25
WIDTH, HEIGHT = COLS * CELL, ROWS * CELL
COLOR_BG = "#0B0B0B"
COLOR_WALL = "#1A1A1A"
COLOR_PATH = "#121212"
COLOR_START = "#00BFFF" 
COLOR_END = "#FF4500"   
COLOR_SOLVE = "#FFD700"  

class MazeMaster:
    def __init__(self, root):
        self.root = root
        self.root.title("Maze Master: Generator & A* Solver 🛡️")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        self.grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        self.start_node = None
        self.end_node = None
        self.setup_ui()
        self.canvas.bind("<Button-1>", self.handle_click)

    def setup_ui(self):
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=50)
        style = {"bg": "#1A1A1A", "fg": "#00FF7F", "font": ("Courier", 10, "bold"), "relief": "flat", "padx": 15, "pady": 5}
        
        tk.Button(btn_frame, text="1. GENERATE MAZE", command=self.generate_maze, **style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="2. RESET POINTS", command=self.reset_points, **style).pack(side=tk.LEFT, padx=5)
        
        self.lbl_info = tk.Label(self.root, text="Step 1: Generate | Step 2: Click Start & End", 
                                 bg=COLOR_BG, fg="#888", font=("Courier", 10))
        self.lbl_info.pack(pady=10)

    def draw_cell(self, r, c, color):
        x0, y0 = c * CELL, r * CELL
        self.canvas.create_rectangle(x0+1, y0+1, x0+CELL-1, y0+CELL-1, fill=color, outline="")

    def handle_click(self, event):
        c, r = event.x // CELL, event.y // CELL
        if r < 0 or r >= ROWS or c < 0 or c >= COLS or self.grid[r][c] == 1:
            return

        if not self.start_node:
            self.start_node = (r, c)
            self.draw_cell(r, c, COLOR_START)
        elif not self.end_node and (r, c) != self.start_node:
            self.end_node = (r, c)
            self.draw_cell(r, c, COLOR_END)
            self.solve_a_star()

    def generate_maze(self):
        self.canvas.delete("all")
        self.grid = [[1 for _ in range(COLS)] for _ in range(ROWS)]
        self.start_node = self.end_node = None
        for r in range(ROWS):
            for c in range(COLS): self.draw_cell(r, c, COLOR_WALL)
        
        self.recursive_backtrack(1, 1)
        self.lbl_info.config(text="Maze Ready! Set Start and End points.", fg="#00FF7F")

    def recursive_backtrack(self, r, c):
        self.grid[r][c] = 0
        self.draw_cell(r, c, COLOR_PATH)
        neighbors = []
        for dr, dc in [(-2,0),(2,0),(0,-2),(0,2)]:
            nr, nc = r+dr, c+dc
            if 0 < nr < ROWS-1 and 0 < nc < COLS-1 and self.grid[nr][nc] == 1:
                neighbors.append((nr, nc, r+dr//2, c+dc//2))
        
        random.shuffle(neighbors)
        for nr, nc, mr, mc in neighbors:
            if self.grid[nr][nc] == 1:
                self.grid[mr][mc] = 0
                self.draw_cell(mr, mc, COLOR_PATH)
                self.recursive_backtrack(nr, nc)

    def solve_a_star(self):
        def h(p1, p2): return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])
        
        start, end = self.start_node, self.end_node
        queue = [(0, start)]
        came_from = {}
        g_score = {start: 0}
        
        while queue:
            _, current = heapq.heappop(queue)
            if current == end:
                self.reconstruct_path(came_from, current)
                return

            for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                neighbor = (current[0]+dr, current[1]+dc)
                if 0 <= neighbor[0] < ROWS and 0 <= neighbor[1] < COLS and self.grid[neighbor[0]][neighbor[1]] == 0:
                    temp_g = g_score[current] + 1
                    if neighbor not in g_score or temp_g < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = temp_g
                        f_score = temp_g + h(neighbor, end)
                        heapq.heappush(queue, (f_score, neighbor))

    def reconstruct_path(self, came_from, current):
        while current in came_from:
            current = came_from[current]
            if current != self.start_node:
                self.draw_cell(current[0], current[1], COLOR_SOLVE)
                self.root.update()

    def reset_points(self):
        self.start_node = self.end_node = None
        self.generate_maze()

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=COLOR_BG)
    MazeMaster(root)
    root.mainloop()