import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI (Minimax) 🤖")
        self.root.configure(bg="#121212")
        
        self.board = [" " for _ in range(9)]
        self.human = "X"
        self.ai = "O"
        self.buttons = []
        self.setup_ui()

    def setup_ui(self):
        grid_frame = tk.Frame(self.root, bg="#333", padx=10, pady=10)
        grid_frame.pack(pady=20)

        for i in range(9):
            btn = tk.Button(grid_frame, text="", font=("Arial", 24, "bold"),
                           width=3, height=1, bg="#1e1e1e", fg="#00FF7F",
                           activebackground="#333", activeforeground="#00FF7F",
                           relief="flat", command=lambda i=i: self.human_move(i))
            btn.grid(row=i//3, column=i%3, padx=5, pady=5)
            self.buttons.append(btn)

        tk.Button(self.root, text="RESET", command=self.reset_game,
                  bg="#FF4500", fg="white", font=("Arial", 10, "bold")).pack(pady=10)

    def human_move(self, i):
        if self.board[i] == " " and not self.check_winner(self.board):
            self.make_move(i, self.human)
            if not self.check_winner(self.board) and " " in self.board:
                self.root.after(500, self.ai_move)

    def make_move(self, i, player):
        self.board[i] = player
        self.buttons[i].config(text=player, fg="#00FF7F" if player == "X" else "#FFD700")
        
        winner = self.check_winner(self.board)
        if winner:
            self.end_game(f"Wygrał: {winner}")
        elif " " not in self.board:
            self.end_game("Remis!")

    def ai_move(self):
        best_score = -float('inf')
        move = None
        for i in range(9):
            if self.board[i] == " ":
                self.board[i] = self.ai
                score = self.minimax(self.board, 0, False)
                self.board[i] = " "
                if score > best_score:
                    best_score = score
                    move = i
        if move is not None:
            self.make_move(move, self.ai)

    def minimax(self, board, depth, is_maximizing):
        winner = self.check_winner(board)
        if winner == self.ai: return 10 - depth
        if winner == self.human: return depth - 10
        if " " not in board: return 0

        if is_maximizing:
            best_score = -float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.ai
                    score = self.minimax(board, depth + 1, False)
                    board[i] = " "
                    best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(9):
                if board[i] == " ":
                    board[i] = self.human
                    score = self.minimax(board, depth + 1, True)
                    board[i] = " "
                    best_score = min(score, best_score)
            return best_score

    def check_winner(self, b):
        win_states = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]
        for s in win_states:
            if b[s[0]] == b[s[1]] == b[s[2]] != " ": return b[s[0]]
        return None

    def end_game(self, msg):
        messagebox.showinfo("Koniec", msg)
        self.reset_game()

    def reset_game(self):
        self.board = [" " for _ in range(9)]
        for btn in self.buttons: btn.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    TicTacToe(root)
    root.mainloop()