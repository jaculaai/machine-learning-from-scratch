import tkinter as tk
from tkinter import ttk

def get_extended_gcd_steps(a, b):
    steps = []
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    
    while r != 0:
        quotient = old_r // r
        steps.append({
            "r_prev": old_r, "r": r, "q": quotient, "res": old_r % r,
            "s": old_s, "t": old_t
        })
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
        
    return old_r, old_s, old_t, steps

class EuclideanVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Extended Euclidean Steps 🔢")
        self.root.geometry("800x600")
        self.root.configure(bg="#121212")

        self.setup_ui()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg="#1e1e1e", pady=20)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="a:", bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=10)
        self.ent_a = tk.Entry(header, width=10, bg="#2d2d2d", fg="#00FF7F", font=("Courier", 14))
        self.ent_a.insert(0, "240")
        self.ent_a.pack(side=tk.LEFT)

        tk.Label(header, text="b:", bg="#1e1e1e", fg="white").pack(side=tk.LEFT, padx=10)
        self.ent_b = tk.Entry(header, width=10, bg="#2d2d2d", fg="#00FF7F", font=("Courier", 14))
        self.ent_b.insert(0, "46")
        self.ent_b.pack(side=tk.LEFT)

        tk.Button(header, text="POKAŻ ROZKŁAD", command=self.update, bg="#00FF7F", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=20)

        # Table area
        self.tree = ttk.Treeview(self.root, columns=("step", "eq", "s", "t"), show="headings")
        self.tree.heading("step", text="Krok")
        self.tree.heading("eq", text="Równanie (r = a - q*b)")
        self.tree.heading("s", text="Współczynnik s")
        self.tree.heading("t", text="Współczynnik t")
        
        # Style for Dark Mode table
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", background="#1e1e1e", foreground="white", fieldbackground="#1e1e1e", rowheight=30)
        style.map("Treeview", background=[('selected', '#00FF7F')], foreground=[('selected', 'black')])
        
        self.tree.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.lbl_final = tk.Label(self.root, text="", bg="#121212", fg="#00FF7F", font=("Courier", 14, "bold"))
        self.lbl_final.pack(pady=10)

    def update(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        try:
            a, b = int(self.ent_a.get()), int(self.ent_b.get())
            gcd, s, t, steps = get_extended_gcd_steps(a, b)
            
            for i, step in enumerate(steps):
                eq = f"{step['r_prev']} = {step['q']} * {step['r']} + {step['res']}"
                self.tree.insert("", tk.END, values=(i+1, eq, step['s'], step['t']))
            
            self.lbl_final.config(text=f"KONIEC: {gcd} = {a}*({s}) + {b}*({t})")
        except:
            self.lbl_final.config(text="BŁĄD DANYCH", fg="#FF4500")

if __name__ == "__main__":
    root = tk.Tk()
    app = EuclideanVisualizer(root)
    root.mainloop()