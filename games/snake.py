import tkinter as tk
import random

# Ustawienia gry
WIDTH, HEIGHT = 600, 400
SIZE = 20
SPEED = 100 # ms

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Neon Snake 🐍")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="#121212", highlightthickness=0)
        self.canvas.pack()

        self.snake = [(100, 100), (80, 100), (60, 100)]
        self.direction = "Right"
        self.food = self.create_food()
        self.score = 0
        self.running = True

        self.root.bind("<KeyPress>", self.change_direction)
        self.update()

    def create_food(self):
        x = random.randint(0, (WIDTH-SIZE)//SIZE) * SIZE
        y = random.randint(0, (HEIGHT-SIZE)//SIZE) * SIZE
        return (x, y)

    def change_direction(self, e):
        opponents = {"Left": "Right", "Right": "Left", "Up": "Down", "Down": "Up"}
        if e.keysym in opponents and e.keysym != opponents.get(self.direction):
            self.direction = e.keysym

    def update(self):
        if not self.running: return

        # Ruch głowy
        head_x, head_y = self.snake[0]
        if self.direction == "Left": head_x -= SIZE
        elif self.direction == "Right": head_x += SIZE
        elif self.direction == "Up": head_y -= SIZE
        elif self.direction == "Down": head_y += SIZE

        new_head = (head_x, head_y)

        # Kolizje (ściany + ogon)
        if (head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or new_head in self.snake):
            self.game_over()
            return

        self.snake.insert(0, new_head)

        # Jedzenie
        if new_head == self.food:
            self.score += 10
            self.food = self.create_food()
        else:
            self.snake.pop()

        self.draw()
        self.root.after(SPEED, self.update)

    def draw(self):
        self.canvas.delete("all")
        # Jedzenie
        self.canvas.create_oval(self.food[0], self.food[1], self.food[0]+SIZE, self.food[1]+SIZE, fill="#FF4500", outline="")
        # Wąż
        for i, (x, y) in enumerate(self.snake):
            color = "#00FF7F" if i == 0 else "#008F56"
            self.canvas.create_rectangle(x, y, x+SIZE, y+SIZE, fill=color, outline="#121212")
        
        self.canvas.create_text(50, 20, text=f"Score: {self.score}", fill="white", font=("Arial", 12, "bold"))

    def game_over(self):
        self.running = False
        self.canvas.create_text(WIDTH//2, HEIGHT//2, text="GAME OVER", fill="#FF4500", font=("Arial", 30, "bold"))
        self.canvas.create_text(WIDTH//2, HEIGHT//2 + 40, text=f"Final Score: {self.score}", fill="white")

if __name__ == "__main__":
    root = tk.Tk()
    SnakeGame(root)
    root.mainloop()