import tkinter as tk
from queue import PriorityQueue

# Ustawienia siatki
WIDTH = 600
ROWS = 25
GAP = WIDTH // ROWS

# Kolory Dark Mode
COLOR_BG = "#121212"
COLOR_GRID = "#333333"
COLOR_WALL = "#555555"
COLOR_START = "#00FF7F"  # Neon Green
COLOR_END = "#FF4500"    # Orange-Red
COLOR_PATH = "#FFD700"   # Gold
COLOR_OPEN = "#2e4a3e"
COLOR_CLOSED = "#4a2e2e"

class Node:
    def __init__(self, row, col):
        self.row, self.col = row, col
        self.x, self.y = row * GAP, col * GAP
        self.color = COLOR_BG
        self.neighbors = []

    def draw(self, canvas):
        canvas.create_rectangle(self.x, self.y, self.x + GAP, self.y + GAP, 
                                 fill=self.color, outline=COLOR_GRID)

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < ROWS - 1 and grid[self.row + 1][self.col].color != COLOR_WALL:
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.row > 0 and grid[self.row - 1][self.col].color != COLOR_WALL:
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.col < ROWS - 1 and grid[self.row][self.col + 1].color != COLOR_WALL:
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.col > 0 and grid[self.row][self.col - 1].color != COLOR_WALL:
            self.neighbors.append(grid[self.row][self.col - 1])

def h(p1, p2): # Heurystyka: odległość Manhattan
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstruct_path(came_from, current, draw_fn):
    while current in came_from:
        current = came_from[current]
        if current.color not in [COLOR_START, COLOR_END]:
            current.color = COLOR_PATH
        draw_fn()

def a_star(draw_fn, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    # Przekazujemy f_score, count (dla unikalności) i obiekt węzła
    open_set.put((0, count, start))
    came_from = {}
    
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    f_score = {node: float("inf") for row in grid for node in row}
    # POPRAWKA: Przekazujemy krotki (row, col) do funkcji h
    f_score[start] = h((start.row, start.col), (end.row, end.col))

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw_fn)
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                # POPRAWKA: Tutaj też przekazujemy krotki (row, col)
                f_score[neighbor] = temp_g_score + h((neighbor.row, neighbor.col), (end.row, end.col))
                
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != end:
                        neighbor.color = COLOR_OPEN
        
        draw_fn()
        if current != start:
            current.color = COLOR_CLOSED

    return False

class App:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=WIDTH, height=WIDTH, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack()
        self.grid = [[Node(i, j) for j in range(ROWS)] for i in range(ROWS)]
        
        # Punkty start/koniec
        self.start = self.grid[2][2]
        self.end = self.grid[ROWS-3][ROWS-3]
        self.start.color, self.end.color = COLOR_START, COLOR_END
        
        root.bind("<B1-Motion>", self.handle_click)
        root.bind("<Button-1>", self.handle_click)
        root.bind("<Button-3>", self.handle_right_click)
        root.bind("<space>", lambda e: self.run())
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        for row in self.grid:
            for node in row:
                node.draw(self.canvas)
        self.canvas.update()

    def handle_click(self, event):
        row, col = event.x // GAP, event.y // GAP
        if 0 <= row < ROWS and 0 <= col < ROWS:
            node = self.grid[row][col]
            if node != self.start and node != self.end:
                node.color = COLOR_WALL
            self.draw()

    def handle_right_click(self, event):
        row, col = event.x // GAP, event.y // GAP
        if 0 <= row < ROWS and 0 <= col < ROWS:
            node = self.grid[row][col]
            if node != self.start and node != self.end:
                node.color = COLOR_BG
            self.draw()

    def run(self):
        # Resetowanie kolorów pola (oprócz ścian i startu/końca) przed nowym szukaniem
        for row in self.grid:
            for node in row:
                node.update_neighbors(self.grid)
                if node.color in [COLOR_PATH, COLOR_OPEN, COLOR_CLOSED]:
                    node.color = COLOR_BG
        
        a_star(self.draw, self.grid, self.start, self.end)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("A* Pathfinding Visualizer 🚀")
    app = App(root)
    tk.Label(root, text="LEWY MYSZY: Rysuj ściany | PRAWY MYSZY: Usuń | SPACJA: Szukaj drogi", 
             bg=COLOR_BG, fg="white", font=("Arial", 10)).pack(pady=5)
    root.mainloop()