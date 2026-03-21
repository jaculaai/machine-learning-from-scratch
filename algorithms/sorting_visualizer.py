import tkinter as tk
import random
import tkinter as tk
import random
import time

# --- KONFIGURACJA ESTETYCZNA ---
WIDTH, HEIGHT = 900, 500
BAR_WIDTH = 6
COLOR_BG = "#0B0B0B"
COLOR_DEFAULT = "#2D2D2D"
COLOR_COMPARE = "#FF4500"  # Neon Orange
COLOR_PIVOT = "#00BFFF"    # Deep Sky Blue
COLOR_DONE = "#00FF7F"     # Spring Green

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Visualizer Pro 📊")
        self.canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg=COLOR_BG, highlightthickness=0)
        self.canvas.pack(pady=20)
        
        self.data = []
        self.comparisons = 0
        self.running = False
        self.data_size = WIDTH // (BAR_WIDTH + 2)
        
        self.setup_ui()
        self.generate_data()

    def setup_ui(self):
        btn_frame = tk.Frame(self.root, bg=COLOR_BG)
        btn_frame.pack(fill=tk.X, padx=50)
        
        style = {"bg": "#1A1A1A", "fg": "white", "font": ("Courier", 10, "bold"), "relief": "flat", "padx": 15, "pady": 5}
        
        tk.Button(btn_frame, text="NEW DATA", command=self.generate_data, **style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="BUBBLE SORT", command=lambda: self.run_sort("bubble"), **style).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="QUICK SORT", command=lambda: self.run_sort("quick"), **style).pack(side=tk.LEFT, padx=5)
        
        self.lbl_stats = tk.Label(self.root, text="Comparisons: 0", bg=COLOR_BG, fg="#888", font=("Courier", 12))
        self.lbl_stats.pack(pady=10)

    def generate_data(self):
        if self.running: return
        self.data = [random.randint(20, HEIGHT - 50) for _ in range(self.data_size)]
        self.comparisons = 0
        self.update_stats()
        self.draw_bars(COLOR_DEFAULT)

    def draw_bars(self, color_map):
        self.canvas.delete("all")
        for i, val in enumerate(self.data):
            x0 = i * (BAR_WIDTH + 2) + 5
            y0 = HEIGHT - val
            x1 = x0 + BAR_WIDTH
            y1 = HEIGHT
            
            color = color_map[i] if isinstance(color_map, list) else color_map
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="")
        self.root.update()

    def update_stats(self):
        self.lbl_stats.config(text=f"Comparisons: {self.comparisons}")

    def run_sort(self, alg):
        if self.running: return
        self.running = True
        if alg == "bubble":
            self.bubble_sort()
        elif alg == "quick":
            self.quick_sort(0, len(self.data) - 1)
        
        self.draw_bars(COLOR_DONE)
        self.running = False

    def bubble_sort(self):
        n = len(self.data)
        for i in range(n):
            for j in range(0, n - i - 1):
                self.comparisons += 1
                if self.data[j] > self.data[j+1]:
                    self.data[j], self.data[j+1] = self.data[j+1], self.data[j]
                
                if j % 2 == 0: # Optymalizacja rysowania
                    colors = [COLOR_DEFAULT] * n
                    colors[j] = COLOR_COMPARE
                    colors[j+1] = COLOR_COMPARE
                    self.draw_bars(colors)
                    self.update_stats()

    def quick_sort(self, low, high):
        if low < high:
            pivot_idx = self.partition(low, high)
            self.quick_sort(low, pivot_idx - 1)
            self.quick_sort(pivot_idx + 1, high)

    def partition(self, low, high):
        pivot = self.data[high]
        i = low - 1
        for j in range(low, high):
            self.comparisons += 1
            colors = [COLOR_DEFAULT] * len(self.data)
            colors[j] = COLOR_COMPARE
            colors[high] = COLOR_PIVOT
            
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
            
            if j % 2 == 0:
                self.draw_bars(colors)
                self.update_stats()
                
        self.data[i+1], self.data[high] = self.data[high], self.data[i+1]
        return i + 1

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg=COLOR_BG)
    SortingVisualizer(root)
    root.mainloop()