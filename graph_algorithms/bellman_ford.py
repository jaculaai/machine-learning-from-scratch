import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt

def bellman_ford(graph, start):
    dist = {node: float("Inf") for node in graph}
    parent = {node: None for node in graph}
    dist[start] = 0

    nodes = list(graph.keys())
    # Relaksacja krawędzi
    for _ in range(len(nodes) - 1):
        for u in graph:
            for v, weight in graph[u].items():
                if dist[u] != float("Inf") and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    parent[v] = u

    # Sprawdzanie ujemnych cykli (ważne: w grafie nieskierowanym 
    # ujemna krawędź SAMA W SOBIE tworzy ujemny cykl!)
    for u in graph:
        for v, weight in graph[u].items():
            if dist[u] != float("Inf") and dist[u] + weight < dist[v]:
                return None, None

    return dist, parent

def get_path(parent, target):
    path = []
    curr = target
    while curr is not None:
        path.append(curr)
        curr = parent[curr]
    path.reverse()
    return " -> ".join(path) if len(path) > 1 or path == [target] else "Brak dojścia"

def get_edges_from_input():
    edges_text = text_edges.get("1.0", tk.END).strip().split('\n')
    edges = []
    for line in edges_text:
        if not line.strip(): continue
        try:
            u, v, w = line.split()
            w = float(w)
            edges.append((u, v, w))
        except ValueError:
            messagebox.showerror("Błąd", "Format: A B 5")
            return None
    return edges

def run_algorithm():
    edges = get_edges_from_input()
    if edges is None: return
    start_node = entry_start.get().strip()
    
    graph = {}
    for u, v, w in edges:
        # GRAF NIESKIEROWANY - dodajemy w obie strony!
        if u not in graph: graph[u] = {}
        if v not in graph: graph[v] = {}
        graph[u][v] = w
        graph[v][u] = w # Ta linijka robi różnicę!

    if start_node not in graph:
        messagebox.showerror("Błąd", "Start nie istnieje!")
        return

    dist, parent = bellman_ford(graph, start_node)
    
    text_result.delete("1.0", tk.END)
    if dist is None:
        text_result.insert(tk.END, "⚠️ WYKRYTO UJEMNY CYKL / UJEMNĄ KRAWĘDŹ!\nW grafie nieskierowanym ujemna waga to błąd.")
    else:
        text_result.insert(tk.END, f"🚀 Start: {start_node}\n" + "="*30 + "\n")
        for node in sorted(dist.keys()):
            d = dist[node]
            path = get_path(parent, node)
            res_str = "Inf" if d == float("Inf") else str(d)
            text_result.insert(tk.END, f"📍 Do {node} | Koszt: {res_str}\n   Trasa: {path}\n\n")

def draw_graph():
    edges = get_edges_from_input()
    if not edges: return
    G = nx.Graph() # Zmienione z DiGraph na Graph (brak strzałek)
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    # Rysujemy bez strzałek
    nx.draw(G, pos, with_labels=True, node_color='lightcoral', node_size=1500, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.show()

# Reszta GUI bez zmian...
root = tk.Tk()
root.title("Bellman-Ford Nieskierowany 🚀")
root.geometry("500x650")

tk.Label(root, text="Wprowadź krawędzie (nieskierowane):", font=("Arial", 11, "bold")).pack(pady=5)
text_edges = tk.Text(root, height=8, width=50)
text_edges.pack()
tk.Button(root, text="🎨 Pokaż Graf", command=draw_graph).pack(pady=5)
tk.Label(root, text="🏁 Start:", font=("Arial", 11, "bold")).pack()
entry_start = tk.Entry(root, justify="center", width=10)
entry_start.pack()
tk.Button(root, text="⚡ OBLICZ", command=run_algorithm, bg="green", font=("Arial", 12, "bold")).pack(pady=10)
text_result = tk.Text(root, height=12, width=50)
text_result.pack(pady=5)
root.mainloop()