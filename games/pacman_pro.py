import tkinter as tk
import random

TILE_SIZE = 25
FPS = 120

MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1],
    [1,2,1,1,0,1,1,0,1,0,1,1,0,1,1,0,1,2,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,0,1],
    [1,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,1],
    [1,1,1,1,0,1,1,1,0,1,0,1,1,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,0,0,0,0,0,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,1,0,1,1,0,0,0,0,0,0,1],
    [1,1,1,1,0,1,0,1,1,1,1,1,0,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,0,1,1,0,0,1,0,0,1,1,0,1,1,0,1],
    [1,2,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,2,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

class Ghost:
    def __init__(self, r, c, color):
        self.pos = [r, c]
        self.color = color
        self.start_pos = [r, c]

class PacmanPro:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Neon Pro 🟡")
        self.canvas = tk.Canvas(root, width=len(MAP[0])*TILE_SIZE, height=len(MAP)*TILE_SIZE, bg="black", highlightthickness=0)
        self.canvas.pack()

        self.pacman_pos = [11, 9]
        self.direction = (0, 0)
        self.next_dir = (0, 0)
        self.score = 0
        self.mouth_open = 0
        
        # Inicjalizacja duchów
        self.ghosts = [
            Ghost(7, 8, "#FF0000"), # Czerwony
            Ghost(7, 9, "#FFB8FF"), # Różowy
            Ghost(7, 10, "#00FFFF"),# Błękitny
            Ghost(8, 9, "#FFB852")  # Pomarańczowy
        ]

        self.root.bind("<KeyPress>", self.handle_keys)
        self.update()

    def handle_keys(self, e):
        keys = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if e.keysym in keys: self.next_dir = keys[e.keysym]

    def can_move(self, r, c):
        return 0 <= r < len(MAP) and 0 <= c < len(MAP[0]) and MAP[r][c] != 1

    def move_ghosts(self):
        for g in self.ghosts:
            # Prosta AI: Duchy próbują zbliżyć się do Pac-Mana, ale z 20% szansą idą losowo
            if random.random() < 0.8:
                dr = 1 if self.pacman_pos[0] > g.pos[0] else -1 if self.pacman_pos[0] < g.pos[0] else 0
                dc = 1 if self.pacman_pos[1] > g.pos[1] else -1 if self.pacman_pos[1] < g.pos[1] else 0
            else:
                dr, dc = random.choice([(0,1), (0,-1), (1,0), (-1,0)])

            if dr != 0 and self.can_move(g.pos[0]+dr, g.pos[1]): g.pos[0] += dr
            elif dc != 0 and self.can_move(g.pos[0], g.pos[1]+dc): g.pos[1] += dc

    def draw(self):
        self.canvas.delete("all")
        for r, row in enumerate(MAP):
            for c, val in enumerate(row):
                x, y = c*TILE_SIZE, r*TILE_SIZE
                if val == 1:
                    self.canvas.create_rectangle(x, y, x+TILE_SIZE, y+TILE_SIZE, fill="#121212", outline="#0000FF")
                elif val == 0:
                    self.canvas.create_oval(x+10, y+10, x+14, y+14, fill="#FFB8AE")
                elif val == 2: # Energizer
                    self.canvas.create_oval(x+6, y+6, x+18, y+18, fill="#FFFFFF")

        # Rysuj Pac-Mana (z animacją buzi)
        px, py = self.pacman_pos[1]*TILE_SIZE, self.pacman_pos[0]*TILE_SIZE
        extent = 359 if self.mouth_open % 2 == 0 else 280
        start_angle = 0
        if self.direction == (0, 1): start_angle = 40
        elif self.direction == (0, -1): start_angle = 220
        elif self.direction == (-1, 0): start_angle = 130
        elif self.direction == (1, 0): start_angle = 310
        
        self.canvas.create_arc(px+2, py+2, px+TILE_SIZE-2, py+TILE_SIZE-2, fill="yellow", start=start_angle, extent=extent)

        # Rysuj Duchy
        for g in self.ghosts:
            gx, gy = g.pos[1]*TILE_SIZE, g.pos[0]*TILE_SIZE
            self.canvas.create_oval(gx+3, gy+3, gx+TILE_SIZE-3, gy+TILE_SIZE-3, fill=g.color, outline="white")

        self.canvas.create_text(60, 15, text=f"SCORE: {self.score}", fill="white", font=("Courier", 12, "bold"))

    def update(self):
        self.mouth_open += 1
        if self.can_move(self.pacman_pos[0]+self.next_dir[0], self.pacman_pos[1]+self.next_dir[1]):
            self.direction = self.next_dir
        
        if self.can_move(self.pacman_pos[0]+self.direction[0], self.pacman_pos[1]+self.direction[1]):
            self.pacman_pos[0] += self.direction[0]
            self.pacman_pos[1] += self.direction[1]

        if MAP[self.pacman_pos[0]][self.pacman_pos[1]] in [0, 2]:
            self.score += 50 if MAP[self.pacman_pos[0]][self.pacman_pos[1]] == 2 else 10
            MAP[self.pacman_pos[0]][self.pacman_pos[1]] = 3 # Zjedzone

        self.move_ghosts()
        self.draw()

        # Sprawdź kolizję
        for g in self.ghosts:
            if g.pos == self.pacman_pos:
                self.canvas.create_text(self.canvas.winfo_width()//2, self.canvas.winfo_height()//2, text="WASTED", fill="red", font=("Courier", 40, "bold"))
                return

        self.root.after(FPS, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    game = PacmanPro(root)
    root.mainloop()