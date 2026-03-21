import tkinter as tk
import random

# Ustawienia
TILE_SIZE = 25
FPS = 150

# Mapa: 1 = Ściana, 0 = Kulka, 'P' = Pacman, 'G' = Duch
MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,0,0,'G',0,0,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,0,1,0,0,1,1,0,1,1,0,1],
    [1,0,0,1,0,0,0,0,0,'P',0,0,0,0,0,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class PacmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Pac-Man 🟡")
        self.rows = len(MAP)
        self.cols = len(MAP[0])
        self.canvas = tk.Canvas(root, width=self.cols*TILE_SIZE, height=self.rows*TILE_SIZE, bg="#000", highlightthickness=0)
        self.canvas.pack()

        self.score = 0
        self.pacman_pos = [13, 9]
        self.ghost_pos = [9, 9]
        self.direction = (0, 0)
        self.next_direction = (0, 0)
        
        self.root.bind("<KeyPress>", self.handle_key)
        self.draw_map()
        self.update()

    def handle_key(self, e):
        moves = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if e.keysym in moves:
            self.next_direction = moves[e.keysym]

    def can_move(self, pos, direction):
        new_r, new_c = pos[0] + direction[0], pos[1] + direction[1]
        if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
            return MAP[new_r][new_c] != 1
        return False

    def draw_map(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c*TILE_SIZE, r*TILE_SIZE
                if MAP[r][c] == 1:
                    # Ściany w kolorze Midnight Blue z neonową ramką
                    self.canvas.create_rectangle(x1, y1, x1+TILE_SIZE, y1+TILE_SIZE, fill="#191970", outline="#0000FF")
                elif MAP[r][c] == 0:
                    # Kulki do zjedzenia
                    self.canvas.create_oval(x1+10, y1+10, x1+15, y1+15, fill="#FFD700")
        
        # Rysowanie Pacmana
        px, py = self.pacman_pos[1]*TILE_SIZE, self.pacman_pos[0]*TILE_SIZE
        self.canvas.create_oval(px+2, py+2, px+TILE_SIZE-2, py+TILE_SIZE-2, fill="#FFFF00", outline="")
        
        # Rysowanie Ducha
        gx, gy = self.ghost_pos[1]*TILE_SIZE, self.ghost_pos[0]*TILE_SIZE
        self.canvas.create_rectangle(gx+4, gy+4, gx+TILE_SIZE-4, gy+TILE_SIZE-4, fill="#FF0000", outline="")

    def move_ghost(self):
        # Bardzo prosta AI duszka: wybiera kierunek bliżej Pacmana
        dr = 1 if self.pacman_pos[0] > self.ghost_pos[0] else -1 if self.pacman_pos[0] < self.ghost_pos[0] else 0
        dc = 1 if self.pacman_pos[1] > self.ghost_pos[1] else -1 if self.pacman_pos[1] < self.ghost_pos[1] else 0
        
        if dr != 0 and self.can_move(self.ghost_pos, (dr, 0)):
            self.ghost_pos[0] += dr
        elif dc != 0 and self.can_move(self.ghost_pos, (0, dc)):
            self.ghost_pos[1] += dc

    def update(self):
        # Sprawdzenie czy możemy zmienić kierunek na ten wybrany przez gracza
        if self.can_move(self.pacman_pos, self.next_direction):
            self.direction = self.next_direction
        
        # Ruch Pacmana
        if self.can_move(self.pacman_pos, self.direction):
            self.pacman_pos[0] += self.direction[0]
            self.pacman_pos[1] += self.direction[1]
            
        # Zjadanie kulek (oznaczamy jako 2 w macierzy)
        if MAP[self.pacman_pos[0]][self.pacman_pos[1]] == 0:
            MAP[self.pacman_pos[0]][self.pacman_pos[1]] = 2 
            self.score += 10
            
        self.move_ghost()
        self.draw_map()
        
        # Kolizja z duchem
        if self.pacman_pos == self.ghost_pos:
            self.canvas.create_text(self.cols*TILE_SIZE//2, self.rows*TILE_SIZE//2, 
                                   text="GAME OVER", fill="#FF4500", font=("Arial", 24, "bold"))
            return

        self.root.after(FPS, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = PacmanGame(root)
    root.mainloop()