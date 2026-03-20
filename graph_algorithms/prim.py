import tkinter as tk
from tkinter import messagebox, ttk
import heapq
import networkx as nx
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Ciemny motyw wykresów
plt.style.use('dark_background')

# --- Algorytm Prima ---
def prim(nodes, graph, start_node):
    mst = []
    visited = {start_node}
    # edges to kolejka priorytetowa: (waga, skąd, dokąd)
    edges = [
        (weight, start_node, to)
        for to, weight in graph[start_node].items()
    ]
    heapq.heapify(edges)
    total_cost = 0

    while edges:
        weight, frm, to = heapq.heappop(edges)
        if to not in visited:
            visited.add(to)
            mst.append((frm, to, weight))
            total_cost += weight

            # Dodajemy nowe krawędzie od nowo odwiedzonego węzła
            for next_to, next_weight in graph[to].items():
                if next_to not in visited:
                    heapq.heappush(edges, (next_weight, to, next_to))
                    
    return mst, total_cost

# --- Obsługa Interfejsu ---
def run_prim():
    input_data = text_edges.get("1.0", tk.END).strip().split('\n')
    start_node = entry_start.get().strip()
    
    if not input_data or not start_node:
        messagebox.showerror("Błąd", "Wprowadź krawędzie i wierzchołek startowy!")
        return

    full_graph = {}
    nodes = set()
    edges_list = []

    try:
        for line in input_data:
            if not line.strip(): continue
            u, v, w = line.split()
            w = float(w)
            nodes.add(u); nodes.add(v)
            edges_list.append((u, v, w))
            # Budujemy strukturę sąsiedztwa dla Prima
            if u not in full_graph: full_graph[u] = {}
            if v not in full_graph: full_graph[v] = {}
            full_graph[u][v] = w
            full_graph[v][u] = w
    except Exception:
        messagebox.showerror("Błąd", "Format: A B 10")
        return

    if start_node not in full_graph:
        messagebox.showerror("Błąd", f"Wierzchołek '{start_node}' nie istnieje!")
        return

    # Obliczamy MST
    mst_edges, cost = prim(list(nodes), full_graph, start_node)

    # Rysowanie
    fig.clear()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    G_full = nx.Graph()
    G_full.add_weighted_edges_from(edges_list)
    pos = nx.spring_layout(G_full, seed=42)

    # Graf PRZED
    ax1.set_title("PRZED: Wszystkie krawędzie", color='#FFD700', fontweight='bold')
    nx.draw(G_full, pos, ax=ax1, with_labels=True, node_color='#333333', edge_color='#555555', node_size=700, font_weight='bold')
    nx.draw_networkx_edge_labels(G_full, pos, edge_labels=nx.get_edge_attributes(G_full, 'weight'), ax=ax1, font_size=8)
    ax1.axis('off')

    # Graf PO (MST)
    G_mst = nx.Graph()
    G_mst.add_nodes_from(nodes)
    G_mst.add_weighted_edges_from(mst_edges)

    ax2.set_title(f"PO: Drzewo Prima\nKoszt: {cost:.2f}", color='#00FF7F', fontweight='bold')
    nx.draw_networkx_edges(G_full, pos, ax=ax2, alpha=0.1, edge_color='#555555', style='dashed')
    nx.draw(G_mst, pos, ax=ax2, with_labels=True, node_color='#006400', edge_color='#00FF7F', width=3, node_size=700, font_weight='bold')
    nx.draw_networkx_edge_labels(G_mst, pos, edge_labels=nx.get_edge_attributes(G_mst, 'weight'), ax=ax2, font_color='#00FF7F')
    ax2.axis('off')

    canvas.draw()

# --- GUI Setup ---
root = tk.Tk()
root.title("Prim MST Architect 🏗️")
root.geometry("1100x700")
root.configure(bg="#1e1e1e")

side_panel = tk.Frame(root, bg="#1e1e1e")
side_panel.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

tk.Label(side_panel, text="Krawędzie (np. A B 5):", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).pack()
text_edges = tk.Text(side_panel, height=20, width=25, bg="#2d2d2d", fg="white", font=("Courier", 11), borderwidth=0)
text_edges.pack(pady=5)
text_edges.insert("1.0", "A B 2\nA C 3\nB C 1\nB D 1\nC D 4\nD E 5")

tk.Label(side_panel, text="Wierzchołek startowy:", fg="white", bg="#1e1e1e").pack(pady=(10, 0))
entry_start = tk.Entry(side_panel, bg="#2d2d2d", fg="white", insertbackground="white", width=10)
entry_start.pack()
entry_start.insert(0, "A")

btn = tk.Button(side_panel, text="🏗️ BUDUJ MST", command=run_prim, bg="#00FF7F", fg="black", font=("Arial", 12, "bold"), height=2)
btn.pack(fill=tk.X, pady=20)

fig = plt.figure(figsize=(9, 6), facecolor="#1e1e1e")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()