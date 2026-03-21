import tkinter as tk
from tkinter import messagebox, ttk
import time

class TuringMachine:
    def __init__(self, tape, rules, start_state, halt_state, blank_symbol="_"):
        self.tape = list(tape)
        self.rules = rules  # {(state, char): (new_state, new_char, direction)}
        self.state = start_state
        self.halt_state = halt_state
        self.blank_symbol = blank_symbol
        self.head_pos = 0

    def step(self):
        if self.state == self.halt_state:
            return False
        
        char_under_head = self.tape[self.head_pos]
        key = (self.state, char_under_head)
        
        if key not in self.rules:
            return False # Brak reguły = błąd/stop
        
        new_state, new_char, direction = self.rules[key]
        
        # Zapisz na taśmie
        self.tape[self.head_pos] = new_char
        # Zmień stan
        self.state = new_state
        # Przesuń głowicę
        if direction == "R":
            self.head_pos += 1
            if self.head_pos == len(self.tape):
                self.tape.append(self.blank_symbol)
        elif direction == "L":
            if self.head_pos == 0:
                self.tape.insert(0, self.blank_symbol)
            else:
                self.head_pos -= 1
        return True

# --- GUI ---
class TuringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Turing Machine Simulator 🧠")
        self.root.geometry("800x500")
        self.root.configure(bg="#1e1e1e")

        self.tm = None
        self.running = False

        # Panel górny - Sterowanie
        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TLabel", background="#1e1e1e", foreground="white")

        top_frame = tk.Frame(self.root, bg="#1e1e1e")
        top_frame.pack(pady=20)

        tk.Label(top_frame, text="Taśma wejściowa:", bg="#1e1e1e", fg="white").grid(row=0, column=0, padx=5)
        self.entry_tape = tk.Entry(top_frame, bg="#2d2d2d", fg="#00FF7F", font=("Courier", 14))
        self.entry_tape.insert(0, "1101")
        self.entry_tape.grid(row=0, column=1, padx=5)

        self.btn_run = tk.Button(top_frame, text="▶ URUCHOM", command=self.start_simulation, bg="#00FF7F", fg="black", font=("Arial", 10, "bold"))
        self.btn_run.grid(row=0, column=2, padx=10)

        # Wizualizacja Taśmy
        self.canvas = tk.Canvas(self.root, height=150, bg="#1e1e1e", highlightthickness=0)
        self.canvas.pack(fill=tk.X, pady=40)

        self.lbl_status = tk.Label(self.root, text="Stan: Oczekiwanie", bg="#1e1e1e", fg="#888888", font=("Arial", 12))
        self.lbl_status.pack()

    def draw_tape(self):
        self.canvas.delete("all")
        w = 50 # szerokość komórki
        h = 50 # wysokość komórki
        start_x = self.root.winfo_width() // 2 - (self.tm.head_pos * w) - w//2

        for i, char in enumerate(self.tm.tape):
            x1 = start_x + (i * w)
            y1 = 50
            x2 = x1 + w
            y2 = y1 + h

            # Rysuj komórkę
            color = "#00FF7F" if i == self.tm.head_pos else "#2d2d2d"
            outline = "white" if i == self.tm.head_pos else "#555555"
            self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline=outline, width=2)
            
            # Tekst w komórce
            text_color = "black" if i == self.tm.head_pos else "white"
            self.canvas.create_text(x1 + w//2, y1 + h//2, text=char, fill=text_color, font=("Courier", 16, "bold"))

        # Strzałka głowicy
        self.canvas.create_polygon(self.root.winfo_width()//2 - 10, 110, 
                                   self.root.winfo_width()//2 + 10, 110, 
                                   self.root.winfo_width()//2, 130, fill="#FF4500")

    def start_simulation(self):
        # Przykład: Odwracanie bitów (Inwerter)
        # (stan, znak) -> (nowy_stan, nowy_znak, kierunek)
        rules = {
            ("q0", "1"): ("q0", "0", "R"),
            ("q0", "0"): ("q0", "1", "R"),
            ("q0", "_"): ("halt", "_", "R"),
        }
        
        input_tape = self.entry_tape.get()
        if not input_tape: input_tape = "_"
        
        self.tm = TuringMachine(input_tape, rules, "q0", "halt")
        self.run_loop()

    def run_loop(self):
        if self.tm.step():
            self.draw_tape()
            self.lbl_status.config(text=f"Stan: {self.tm.state} | Pozycja: {self.tm.head_pos}")
            self.root.after(500, self.run_loop)
        else:
            self.draw_tape()
            self.lbl_status.config(text=f"KONIEC (Stan: {self.tm.state})", fg="#FF4500")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringApp(root)
    root.mainloop()