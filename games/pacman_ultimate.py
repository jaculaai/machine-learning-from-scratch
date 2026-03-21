import tkinter as tk
import random

# --- KONFIGURACJA ESTETYCZNA ---
TILE_SIZE = 25
COLOR_BG = "#000000"
COLOR_WALL = "#050520"
COLOR_WALL_OUTLINE = "#2222FF"
COLOR_PACMAN = "#FFFF00"
COLOR_GHOST_EYE = "#FFFFFF"

# MAPA XXL (1=Ściana, 0=Kulka, 2=Energizer, 3=Puste)
ULTIMATE_MAP = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1],
    [1,2,1,1,1,0,1,1,1,1,1,0,1,0,1,1,1,1,1,0,1,1,1,2,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1,1,1,1,1,1,1,1,1,0,1,0,1,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,0,1,1,1,1,3,3,1,3,3,1,1,1,1,0,1,1,1,1,1],
    [1,1,1,1,1,0,1,3,3,3,3,3,3,3,3,3,3,3,1,0,1,1,1,1,1],
    [1,1,1,1,1,0,1,3,1,1,1,3,3,3,1,1,1,3,1,0,1,1,1,1,1],
    [3,3,3,3,3,0,3,3,1,3,3,3,3,3,3,3,1,3,3,0,3,3,3,3,3], # Tunel
    [1,1,1,1,1,0,1,3,1,1,1,1,1,1,1,1,1,3,1,0,1,1,1,1,1],
    [1,1,1,1,1,0,1,3,3,3,3,3,3,3,3,3,3,3,1,0,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1,1,1,3,3,3,1,1,1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,0,0,0,0,0,1,0,0,0,0,0,1,1,1,1,1,0,1],
    [1,2,0,0,1,1,0,1,1,1,1,0,1,0,1,1,1,0,1,1,0,0,2,0,1],
    [1,1,1,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,1,1,1],
    [1,0,0,0,0,0,0,1,1,1,1,1,0,1,1,1,1,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

class Ghost:
    def __init__(self, r, c, color, personality):
        self.r, self.c = r, c
        self.start_r, self.start_c = r, c
        self.color = color
        self.personality = personality 
        self.frightened = False

    def reset(self):
        self.r, self.c = self.start_r, self.start_c
        self.frightened = False

class PacmanUltimate:
    def __init__(self, root):
        self.root = root
        self.root.title("Pac-Man Ultimate Edition 🏆")
        self.win_w = len(ULTIMATE_MAP[0]) * TILE_SIZE
        self.win_h = len(ULTIMATE_MAP) * TILE_SIZE + 80
        
        self.canvas = tk.Canvas(root, width=self.win_w, height=self.win_h, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack()
        
        self.in_menu = True
        self.difficulty = "Normal"
        self.show_menu()
        self.root.bind("<KeyPress>", self.handle_keys)

    def show_menu(self):
        self.canvas.delete("all")
        mid_x = self.win_w // 2
        
        # Ramka menu
        self.canvas.create_rectangle(30, 30, self.win_w-30, self.win_h-100, outline=COLOR_WALL_OUTLINE, width=2)
        
        # Nagłówek
        self.canvas.create_text(mid_x, 100, text="PAC-MAN", fill=COLOR_PACMAN, font=("Courier", 50, "bold"))
        self.canvas.create_text(mid_x, 150, text="ULTIMATE EDITION", fill="#00FFFF", font=("Courier", 18, "italic"))
        
        # Wybór
        self.canvas.create_text(mid_x, 240, text="SELECT DIFFICULTY:", fill="white", font=("Courier", 14))
        self.canvas.create_text(mid_x, 290, text="[1] EASY MODE", fill="#00FF7F", font=("Courier", 16, "bold"))
        self.canvas.create_text(mid_x, 330, text="[2] NORMAL MODE", fill="#FFD700", font=("Courier", 16, "bold"))
        self.canvas.create_text(mid_x, 370, text="[3] HARDCORE", fill="#FF4500", font=("Courier", 16, "bold"))
        
        self.canvas.create_text(mid_x, self.win_h-140, text="Press a number or SPACE to start", fill="#666", font=("Courier", 10))

    def start_game(self, diff):
        self.in_menu = False
        if diff == "1":
            self.fps = 180; self.ghost_agg = 0.4; self.difficulty = "Easy"
        elif diff == "3":
            self.fps = 90; self.ghost_agg = 0.9; self.difficulty = "Hard"
        else:
            self.fps = 140; self.ghost_agg = 0.7; self.difficulty = "Normal"
            
        self.init_full_game()
        self.game_loop()

    def init_full_game(self):
        self.map_data = [row[:] for row in ULTIMATE_MAP]
        self.pacman_pos = [15, 12]
        self.direction = (0, 0); self.next_dir = (0, 0)
        self.score = 0; self.lives = 3
        self.game_over = False; self.won = False
        self.mouth_open = 0; self.power_timer = 0
        self.ghosts = [
            Ghost(9, 11, "#FF0000", 0), Ghost(9, 12, "#FFB8FF", 2),
            Ghost(10, 11, "#00FFFF", 1), Ghost(10, 13, "#FFB852", 1)
        ]

    def handle_keys(self, e):
        if self.in_menu:
            if e.char in ["1", "2", "3"]: self.start_game(e.char)
            elif e.keysym == "space": self.start_game("2")
            return

        keys = {"Up": (-1, 0), "Down": (1, 0), "Left": (0, -1), "Right": (0, 1)}
        if e.keysym in keys: self.next_dir = keys[e.keysym]
        if e.keysym.lower() == 'r' and (self.game_over or self.won):
            self.in_menu = True
            self.show_menu()

    def can_move(self, r, c):
        if c < 0 or c >= len(self.map_data[0]): return True
        if r < 0 or r >= len(self.map_data): return False
        return self.map_data[r][c] != 1

    def draw(self):
        self.canvas.delete("all")
        # Mapa
        for r, row in enumerate(self.map_data):
            for c, val in enumerate(row):
                x, y = c*TILE_SIZE, r*TILE_SIZE
                if val == 1:
                    self.canvas.create_rectangle(x+4, y+4, x+TILE_SIZE-4, y+TILE_SIZE-4, outline="#191970", fill=COLOR_WALL, width=2)
                elif val == 0:
                    self.canvas.create_oval(x+10, y+10, x+14, y+14, fill="#FFB8AE", outline="")
                elif val == 2:
                    color = "white" if self.mouth_open % 2 == 0 else "#333"
                    self.canvas.create_oval(x+6, y+6, x+18, y+18, fill=color, outline="")

        # Pacman
        px, py = self.pacman_pos[1]*TILE_SIZE, self.pacman_pos[0]*TILE_SIZE
        extent = 359 if self.mouth_open % 2 == 0 else 280
        angles = {(0, 1): 40, (0, -1): 220, (-1, 0): 130, (1, 0): 310}
        start_angle = angles.get(self.direction, 0)
        self.canvas.create_arc(px+3, py+3, px+TILE_SIZE-3, py+TILE_SIZE-3, fill=COLOR_PACMAN, start=start_angle, extent=extent, outline="black")

        # Duchy
        for g in self.ghosts:
            gx, gy = g.c*TILE_SIZE, g.r*TILE_SIZE
            color = "#2222FF" if g.frightened else g.color
            self.canvas.create_oval(gx+3, gy+3, gx+TILE_SIZE-3, gy+TILE_SIZE-3, fill=color, outline="white")
            self.canvas.create_oval(gx+7, gy+8, gx+10, gy+11, fill=COLOR_GHOST_EYE)
            self.canvas.create_oval(gx+15, gy+8, gx+18, gy+11, fill=COLOR_GHOST_EYE)

        # Panel Dolny
        self.canvas.create_line(0, self.win_h-70, self.win_w, self.win_h-70, fill="#333")
        self.canvas.create_text(80, self.win_h-35, text=f"SCORE: {self.score}", fill="#00FF7F", font=("Courier", 14, "bold"))
        self.canvas.create_text(self.win_w//2, self.win_h-35, text=f"LVL: {self.difficulty.upper()}", fill="white", font=("Courier", 10))
        self.canvas.create_text(self.win_w-80, self.win_h-35, text=f"LIVES: {'❤'*self.lives}", fill="#FF4500", font=("Courier", 14))
        
        if self.game_over: self.show_overlay("GAME OVER", "#FF4500")
        elif self.won: self.show_overlay("VICTORY!", "#FFD700")

    def show_overlay(self, text, color):
        mid_x, mid_y = self.win_w // 2, (self.win_h-70) // 2
        self.canvas.create_rectangle(0, 0, self.win_w, self.win_h-70, fill="black", stipple="gray50")
        self.canvas.create_text(mid_x, mid_y - 20, text=text, fill=color, font=("Courier", 48, "bold"))
        self.canvas.create_text(mid_x, mid_y + 40, text="PRESS 'R' TO RESTART", fill="white", font=("Courier", 14))

    def game_loop(self):
        if not (self.game_over or self.won or self.in_menu):
            self.mouth_open += 1
            if self.pacman_pos[1] < 0: self.pacman_pos[1] = len(self.map_data[0]) - 1
            elif self.pacman_pos[1] >= len(self.map_data[0]): self.pacman_pos[1] = 0

            if self.can_move(self.pacman_pos[0] + self.next_dir[0], self.pacman_pos[1] + self.next_dir[1]): self.direction = self.next_dir
            if self.can_move(self.pacman_pos[0] + self.direction[0], self.pacman_pos[1] + self.direction[1]):
                self.pacman_pos[0] += self.direction[0]; self.pacman_pos[1] += self.direction[1]

            r, c = self.pacman_pos[0], self.pacman_pos[1]
            if 0 <= r < len(self.map_data) and 0 <= c < len(self.map_data[0]):
                if self.map_data[r][c] in [0, 2]:
                    self.score += 50 if self.map_data[r][c] == 2 else 10
                    if self.map_data[r][c] == 2:
                        self.power_timer = 40
                        for g in self.ghosts: g.frightened = True
                    self.map_data[r][c] = 3

            if not any(0 in row or 2 in row for row in self.map_data): self.won = True
            if self.power_timer > 0:
                self.power_timer -= 1
                if self.power_timer == 0:
                    for g in self.ghosts: g.frightened = False

            for g in self.ghosts:
                if random.random() < self.ghost_agg:
                    dr = 1 if self.pacman_pos[0] > g.r else -1 if self.pacman_pos[0] < g.r else 0
                    dc = 1 if self.pacman_pos[1] > g.c else -1 if self.pacman_pos[1] < g.c else 0
                else: dr, dc = random.choice([(0,1), (0,-1), (1,0), (-1,0)])
                if dr != 0 and self.can_move(g.r+dr, g.c): g.r += dr
                elif dc != 0 and self.can_move(g.r, g.c+dc): g.c += dc

                if [g.r, g.c] == self.pacman_pos:
                    if g.frightened: self.score += 200; g.reset()
                    else:
                        self.lives -= 1
                        if self.lives <= 0: self.game_over = True
                        else: 
                            self.pacman_pos = [15, 12]; self.direction = (0, 0); self.next_dir = (0, 0)
                            for gh in self.ghosts: gh.reset()
            self.draw()
            self.root.after(self.fps, self.game_loop)

if __name__ == "__main__":
    root = tk.Tk()
    game = PacmanUltimate(root); root.mainloop()