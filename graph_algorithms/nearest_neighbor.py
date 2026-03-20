import tkinter as tk
from tkinter import messagebox, ttk
import networkx as nx
import matplotlib
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Styl wizualny
plt.style.use('dark_background')

def nearest_neighbor_tsp(nodes, graph, start_node):
    path = [start_node]
    unvisited = set(nodes)
    unvisited.remove(start_node)
    total_cost = 0
    curr = start_node
    edges_in_path = []

    while unvisited:
        # Szukamy najblizszego sasiada, ktory nie byl odwiedzony
        next_node = None
        min_dist = float('inf')
        
        for neighbor, weight in graph[curr].items():
            if neighbor in unvisited and weight < min_dist:
                min_dist = weight
                next_node = neighbor
        
        if next_node is None: break # Brak polaczenia
        
        edges_in_path.append((curr, next_node, min_dist))
        total_cost += min_dist
        path.append(next_node)
        unvisited.remove(next_node)
        curr = next_node
        
    return path, edges_in_path, total_cost

def run_algorithm():
    input_data = text_edges.get("1.0", tk.END).strip().split('\n')
    start_node = entry_start.get().strip()
    
    if not input_data or not start_node:
        messagebox.showerror("Błąd", "Wprowadź dane i start!")
        return

    full_graph = {}
    nodes = set()
    all_edges = []

    try:
        for line in input_data:
            if not line.strip(): continue
            u, v, w = line.split()
            w = float(w)
            nodes.add(u); nodes.add(v)
            all_edges.append((u, v, w))
            if u not in full_graph: full_graph[u] = {}
            if v not in full_graph: full_graph[v] = {}
            full_graph[u][v] = w
            full_graph[v][u] = w
    except:
        messagebox.showerror("Błąd", "Format: A B 10")
        return

    if start_node not in full_graph:
        messagebox.showerror("Błąd", "Start nie istnieje!")
        return

    path, path_edges, cost = nearest_neighbor_tsp(list(nodes), full_graph, start_node)

    # Rysowanie
    fig.clear()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)

    G_full = nx.Graph()
    G_full.add_weighted_edges_from(all_edges)
    pos = nx.spring_layout(G_full, seed=42)

    # PRZED
    ax1.set_title("PRZED: Sieć połączeń", color='#FFD700', fontweight='bold')
    nx.draw(G_full, pos, ax=ax1, with_labels=True, node_color='#333333', edge_color='#555555', node_size=700)
    ax1.axis('off')

    # PO (Trasa)
    G_path = nx.Graph()
    G_path.add_nodes_from(nodes)
    G_path.add_weighted_edges_from(path_edges)

    ax2.set_title(f"PO: Najtańsze Łącza\nKoszt: {cost:.2f}", color='#00BFFF', fontweight='bold')
    nx.draw_networkx_edges(G_full, pos, ax=ax2, alpha=0.1, edge_color='#555555', style='dashed')
    nx.draw(G_path, pos, ax=ax2, with_labels=True, node_color='#00008B', edge_color='#00BFFF', width=3, node_size=700)
    nx.draw_networkx_edge_labels(G_path, pos, edge_labels=nx.get_edge_attributes(G_path, 'weight'), ax=ax2, font_color='#00BFFF')
    ax2.axis('off')

    canvas.draw()
    text_result.delete("1.0", tk.END)
    text_result.insert(tk.END, "🚀 Kolejność:\n" + " -> ".join(path))

# --- GUI ---
root = tk.Tk()
root.title("Nearest Neighbor Finder 🏎️")
root.geometry("1100x750")
root.configure(bg="#1e1e1e")

side_panel = tk.Frame(root, bg="#1e1e1e")
side_panel.pack(side=tk.LEFT, fill=tk.Y, padx=15, pady=15)

tk.Label(side_panel, text="Krawędzie (A B 10):", fg="white", bg="#1e1e1e", font=("Arial", 10, "bold")).pack()
text_edges = tk.Text(side_panel, height=15, width=25, bg="#2d2d2d", fg="white", font=("Courier", 11))
text_edges.pack(pady=5)
text_edges.insert("1.0", "A B 10\nA C 15\nA D 20\nB C 35\nB D 25\nC D 30")

tk.Label(side_panel, text="Start node:", fg="white", bg="#1e1e1e").pack()
entry_start = tk.Entry(side_panel, bg="#2d2d2d", fg="white", width=10)
entry_start.pack()
entry_start.insert(0, "A")

btn = tk.Button(side_panel, text="🏎️ JEDŹ NAJBLIŻEJ", command=run_algorithm, bg="#00BFFF", fg="black", font=("Arial", 12, "bold"))
btn.pack(fill=tk.X, pady=20)

text_result = tk.Text(side_panel, height=5, width=25, bg="#1e1e1e", fg="#00BFFF")
text_result.pack()

fig = plt.figure(figsize=(9, 6), facecolor="#1e1e1e")
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

root.mainloop()