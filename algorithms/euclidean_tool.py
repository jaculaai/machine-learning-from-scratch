import tkinter as tk
from tkinter import ttk

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

class EuclideanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Euclidean Algorithm Visualizer 🔢")
        self.root.geometry("600x450")
        self.root.configure(bg="#121212")

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.configure("TLabel", background="#121212", foreground="white", font=("Arial", 11))

        main_frame = tk.Frame(self.root, bg="#1e1e1e", padx=30, pady=30, relief="flat")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Input A
        tk.Label(main_frame, text="Liczba a:", bg="#1e1e1e", fg="#888888").grid(row=0, column=0, sticky="w")
        self.entry_a = tk.Entry(main_frame, bg="#2d2d2d", fg="#00FF7F", font=("Courier", 14), insertbackground="white", width=15)
        self.entry_a.grid(row=1, column=0, pady=(0, 20), padx=5)

        # Input B
        tk.Label(main_frame, text="Liczba b:", bg="#1e1e1e", fg="#888888").grid(row=0, column=1, sticky="w")
        self.entry_b = tk.Entry(main_frame, bg="#2d2d2d", fg="#00FF7F", font=("Courier", 14), insertbackground="white", width=15)
        self.entry_b.grid(row=1, column=1, pady=(0, 20), padx=5)

        # Przycisk obliczeń
        self.btn_calc = tk.Button(main_frame, text="OBLICZ NWD", command=self.calculate, 
                                 bg="#00FF7F", fg="black", font=("Arial", 10, "bold"), 
                                 padx=20, pady=10, cursor="hand2")
        self.btn_calc.grid(row=2, column=0, columnspan=2, pady=10)

        # Wyniki
        self.res_nwd = tk.Label(main_frame, text="NWD(a, b) = ?", bg="#1e1e1e", fg="white", font=("Arial", 16, "bold"))
        self.res_nwd.grid(row=3, column=0, columnspan=2, pady=(20, 5))

        self.res_ext = tk.Label(main_frame, text="Równanie: ?", bg="#1e1e1e", fg="#00FF7F", font=("Courier", 11))
        self.res_ext.grid(row=4, column=0, columnspan=2)

    def calculate(self):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            
            gcd, x, y = extended_gcd(a, b)
            
            self.res_nwd.config(text=f"NWD({a}, {b}) = {gcd}")
            self.res_ext.config(text=f"{a} * ({x}) + {b} * ({y}) = {gcd}")
        except ValueError:
            self.res_nwd.config(text="BŁĄD: Wpisz liczby!", fg="#FF4500")

if __name__ == "__main__":
    root = tk.Tk()
    app = EuclideanApp(root)
    root.mainloop()