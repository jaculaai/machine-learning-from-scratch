import tkinter as tk
import random
from tkinter import messagebox

class Minesweeper:
    def __init__(self, root, rows=10, cols=10, mines=10):
        self.root = root
        self.root.title("Neon Minesweeper 💣")
        self.rows, self.cols, self.mines = rows, cols, mines
        self.board = [[0 for _ in range(cols)] for _ in range(rows)]
        self.mine_locs = set()
        self.buttons = {}
        self.setup_board()
        self.setup_ui()

    def setup_board(self):
        while len(self.mine_locs) < self.mines:
            r, c = random.randint(0, self.rows-1), random.randint(0, self.cols-1)
            if (r, c) not in self.mine_locs:
                self.mine_locs.add((r, c))
                self.board[r][c] = -1 # Mina

        for r, c in self.mine_locs:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols and self.board[nr][nc] != -1:
                        self.board[nr][nc] += 1

    def setup_ui(self):
        self.frame = tk.Frame(self.root, bg="#121212")
        self.frame.pack(padx=10, pady=10)
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.frame, width=3, height=1, bg="#2d2d2d", fg="white", 
                               relief="flat", font=("Arial", 10, "bold"))
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.flag(r, c))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

    def click(self, r, c):
        if (r, c) in self.mine_locs:
            self.buttons[(r, c)].config(text="💣", bg="#FF4500")
            messagebox.showinfo("BUM!", "Trafiłeś na minę!")
            self.root.destroy()
        else:
            self.reveal(r, c)

    def reveal(self, r, c):
        btn = self.buttons[(r, c)]
        if btn["state"] == "disabled": return
        val = self.board[r][c]
        btn.config(text=str(val) if val > 0 else "", bg="#121212", state="disabled", disabledforeground="#00FF7F")
        if val == 0:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    nr, nc = r+dr, c+dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal(nr, nc)

    def flag(self, r, c):
        btn = self.buttons[(r, c)]
        if btn["text"] == "🚩": btn.config(text="", fg="white")
        else: btn.config(text="🚩", fg="#FFD700")

if __name__ == "__main__":
    root = tk.Tk()
    Minesweeper(root)
    root.mainloop()