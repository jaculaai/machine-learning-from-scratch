import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx

# Wymuszamy nowoczesny silnik graficzny
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Ciemny Motyw dla Matplotlib ---
plt.style.use('dark_background')

# --- Klasa do zarządzania zbiorami rozłącznymi (Union-Find) ---
class UnionFind:
    def __init__(self, nodes):
        self.parent = {node: node for node in nodes}
    def find(self, i):
        if self.parent[i] == i: return i
        return self.find(self.parent[i])
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            self.parent[root_i] = root_j
            return True
        return False

# --- Główna logika Algorytmu Kruskala ---
def kruskal(nodes, edges):
    edges.sort(key=lambda x: x[2]) # Sortowanie po wagach
    uf = UnionFind(nodes)
    mst = []
    total_cost = 0
    for u, v, weight in edges:
        if uf.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight
    return mst, total_cost

# --- Funkcje obsługi Interfejsu ---
def get_data_from_input():
    input_data = text_edges.get("1.0", tk.END).strip().split('\n')
    edges = []
    nodes = set()
    try:
        for line in input_data:
            if not line.strip(): continue
            u, v, w = line.split()
            w = float(w)
            edges.append((u, v, w))
            nodes.add(u)
            nodes.add(v)
    except ValueError:
        messagebox.showerror("Błąd formatu", "Wpisz krawędzie jako: Start Koniec Waga\nPrzykład: A B 5")
        return None, None
    return list(nodes), edges

def run_comparison():
    nodes, edges = get_data_from_input()
    if not nodes: return

    # 🔥 Kluczowe: Czyścimy całą figurę, a nie tylko osie!
    fig.clear()
    
    # Tworzymy osie od nowa (obok siebie)
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    # 1. Graf "PRZED" (Pełny)
    G_full = nx.Graph()
    G_full.add_nodes_from(nodes)
    G_full.add_weighted_edges_from(edges)
    pos = nx.spring_layout(G_full, seed=42) # Stałe pozycje

    ax1.set_title("1. PEŁNY GRAF (PRZED)", fontsize=11, fontweight='bold', color='#FFD700')
    nx.draw(G_full, pos, ax=ax1, with_labels=True, node_color='#333333', edge_color='#555555', node_size=800, font_color='white', font_weight='bold')
    labels = nx.get_edge_attributes(G_full, 'weight')
    nx.draw_networkx_edge_labels(G_full, pos, edge_labels=labels, ax=ax1, font_size=9, font_color='#AAAAAA')
    ax1.axis('off')

    # 2. Obliczamy MST
    mst_edges, total_cost = kruskal(nodes, edges)

    # 3. Graf "PO" (Tylko MST)
    G_mst = nx.Graph()
    G_mst.add_nodes_from(nodes)
    G_mst.add_weighted_edges_from(mst_edges)

    ax2.set_title(f"2. NAJTAŃSZA SIEĆ (PO)\nKoszt: {total_cost:.2f}", fontsize=11, fontweight='bold', color='#00FF7F')
    nx.draw_networkx_edges(G_full, pos, ax=ax2, alpha=0.1, edge_color='#555555', style='dashed')
    nx.draw(G_mst, pos, ax=ax2, with_labels=True, node_color='#006400', edge_color='#00FF7F', width=3, node_size=800, font_color='white', font_weight='bold')
    mst_labels = nx.get_edge_attributes(G_mst, 'weight')
    nx.draw_networkx_edge_labels(G_mst, pos, edge_labels=mst_labels, ax=ax2, font_color='#00FF7F', font_size=10, font_weight='bold')
    ax2.axis('off')

    # Odświeżamy płótno
    canvas.draw()

# ==========================================
# GŁÓWNE OKNO APLIKACJI (Dark Mode)
# ==========================================
BG_COLOR = "#1e1e1e" # Ciemnoszary z VS Code
FG_COLOR = "white"

root = tk.Tk()
root.title("Kruskal Analyzer Pro v2.0 🌳🕶️")
root.geometry("1100x700")
root.configure(bg=BG_COLOR)

# Stylizacja nowoczesna (ttk)
style = ttk.Style()
style.theme_use('clam') # Nowocześniejszy silnik bazowy
style.configure("TFrame", background=BG_COLOR)
style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR, font=("Arial", 11))
style.configure("TButton", background="#444444", foreground=FG_COLOR, font=("Arial", 11, "bold"))
style.map("TButton", background=[('active', '#666666')])

# Panel boczny na wprowadzanie danych
side_panel = ttk.Frame(root)
side_panel.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

ttk.Label(side_panel, text="Wprowadź dane (A B 10):", font=("Arial", 12, "bold")).pack(pady=(0, 10))
text_edges = tk.Text(side_panel, height=22, width=30, bg="#2d2d2d", fg=FG_COLOR, insertbackground=FG_COLOR, font=("Courier", 11), borderwidth=0)
text_edges.pack(pady=5)

# Przykładowe dane na start
text_edges.insert("1.0", "A B 4\nA H 8\nB C 8\nB H 11\nC D 7\nC I 2\nC F 4\nD E 9\nD F 14\nE F 10\nF G 2\nG H 1\nG I 6\nH I 7")

# Nowoczesny przycisk z tłem
frame_btn = tk.Frame(side_panel, bg="#4CAF50", bd=0) # Ramka dla koloru tła przycisku
frame_btn.pack(fill=tk.X, pady=20)
btn_run = tk.Button(frame_btn, text="🚀 GENERUJ ANALIZĘ", command=run_comparison, 
                    bg="#4CAF50", fg="black", font=("Arial", 12, "bold"), relief="flat", height=2)
btn_run.pack(fill=tk.X)

# Panel na wykresy
plot_container = ttk.Frame(root)
plot_container.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=15, pady=15)

# Tworzymy figurę z ciemnym tłem
fig = plt.figure(figsize=(9, 6), facecolor=BG_COLOR)
canvas = FigureCanvasTkAgg(fig, master=plot_container)
canvas.get_tk_widget().config(bg=BG_COLOR)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

root.mainloop()