import tkinter as tk
from tkinter import ttk

class TuringMachine:
    def __init__(self, tape, rules, start_state, accept_states, blank="_"):
        self.tape = list(tape) + [blank]
        self.rules = rules # {(state, char): (new_state, new_char, dir)}
        self.state = start_state
        self.accept_states = accept_states
        self.head_pos = 0
        self.blank = blank

    def step(self):
        char = self.tape[self.head_pos]
        key = (self.state, char)
        if key not in self.rules: return False
        
        new_state, new_char, direction = self.rules[key]
        self.tape[self.head_pos] = new_char
        self.state = new_state
        
        if direction == "R":
            self.head_pos += 1
            if self.head_pos == len(self.tape): self.tape.append(self.blank)
        elif direction == "L":
            self.head_pos = max(0, self.head_pos - 1)
        return True

class TuringApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Turing Logic Generator 🧠")
        self.root.geometry("900x600")
        self.root.configure(bg="#121212")
        self.tm = None

        self.setup_ui()

    def setup_ui(self):
        # Panel Sterowania
        ctrl_frame = tk.Frame(self.root, bg="#1e1e1e", padx=20, pady=20)
        ctrl_frame.pack(fill=tk.X)

        tk.Label(ctrl_frame, text="Akceptowane ciągi (oddziel przecinkiem):", fg="white", bg="#1e1e1e").grid(row=0, column=0, sticky="w")
        self.patterns = tk.Entry(ctrl_frame, bg="#2d2d2d", fg="#00FF7F", width=40, insertbackground="white")
        self.patterns.insert(0, "01, 110, 000")
        self.patterns.grid(row=0, column=1, padx=10)

        tk.Label(ctrl_frame, text="Taśma do testu:", fg="white", bg="#1e1e1e").grid(row=1, column=0, sticky="w", pady=10)
        self.test_tape = tk.Entry(ctrl_frame, bg="#2d2d2d", fg="#00FF7F", width=40, insertbackground="white")
        self.test_tape.insert(0, "01")
        self.test_tape.grid(row=1, column=1, padx=10)

        self.btn_gen = tk.Button(ctrl_frame, text="⚡ GENERUJ I URUCHOM", command=self.generate_and_run, bg="#00FF7F", font=("Arial", 10, "bold"))
        self.btn_gen.grid(row=0, column=2, rowspan=2, padx=20)

        # Wizualizacja
        self.canvas = tk.Canvas(self.root, height=200, bg="#121212", highlightthickness=0)
        self.canvas.pack(fill=tk.X, pady=50)

        self.lbl_status = tk.Label(self.root, text="System gotowy", bg="#121212", fg="#888888", font=("Courier", 14))
        self.lbl_status.pack()

    def generate_rules(self, strings):
        rules = {}
        accept_states = set()
        state_counter = 0
        
        # Prosty generator automatu (Trie-based TM)
        for s in strings:
            current_state = "start"
            for char in s.strip():
                next_state = f"q{state_counter}"
                # Jeśli przejście już istnieje, użyj go
                if (current_state, char) in rules:
                    next_state = rules[(current_state, char)][0]
                else:
                    rules[(current_state, char)] = (next_state, char, "R")
                    state_counter += 1
                current_state = next_state
            
            # Po przejściu całego ciągu, dodaj przejście do HALT na pustym znaku
            rules[(current_state, "_")] = ("ACC", "_", "R")
            accept_states.add("ACC")
            
        return rules, "start", accept_states

    def draw(self):
        self.canvas.delete("all")
        w, h = 60, 60
        mid_x = self.root.winfo_width() // 2
        offset_x = mid_x - (self.tm.head_pos * w)

        for i, val in enumerate(self.tm.tape):
            x1 = offset_x + (i * w) - w//2
            color = "#00FF7F" if i == self.tm.head_pos else "#1e1e1e"
            self.canvas.create_rectangle(x1, 70, x1+w, 70+h, fill=color, outline="#333")
            self.canvas.create_text(x1+w//2, 70+h//2, text=val, fill="white" if i != self.tm.head_pos else "black", font=("Courier", 20, "bold"))

        # Głowica
        self.canvas.create_polygon(mid_x-15, 140, mid_x+15, 140, mid_x, 160, fill="#FF4500")

    def generate_and_run(self):
        str_list = self.patterns.get().split(",")
        rules, start, accepts = self.generate_rules(str_list)
        self.tm = TuringMachine(self.test_tape.get(), rules, start, accepts)
        self.step_sim()

    def step_sim(self):
        if self.tm.step():
            self.draw()
            self.lbl_status.config(text=f"Stan: {self.tm.state}", fg="#00FF7F")
            self.root.after(400, self.step_sim)
        else:
            self.draw()
            if self.tm.state in self.tm.accept_states:
                self.lbl_status.config(text="✅ CIĄG ZAAKCEPTOWANY", fg="#00FF7F")
            else:
                self.lbl_status.config(text="❌ ODRZUCONO", fg="#FF4500")

if __name__ == "__main__":
    root = tk.Tk()
    app = TuringApp(root)
    root.mainloop()