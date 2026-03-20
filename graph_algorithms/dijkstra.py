import tkinter as tk
from tkinter import messagebox
import heapq
import networkx as nx
import matplotlib.pyplot as plt

def dijkstra(graph, start):
    # Inicjalizacja: dystans nieskończony, brak rodzica
    distances = {node: float('infinity') for node in graph}
    parent = {node: None for node in graph}
    distances[start] = 0
    
    # Kolejka priorytetowa (dystans, wierzchołek)
    pq = [(0, start)]

    while pq:
        curr_dist, curr_node = heapq.heappop(pq)
        
        if curr_dist > distances[curr_node]: 
            continue
        
        for neighbor, weight in graph[curr_node].items():
            # Dijkstra nie trawi ujemnych wag!
            if weight < 0:
                return None, None
                
            dist = curr_dist + weight
            if dist < distances[neighbor]:
                distances[neighbor] = dist
                parent[neighbor] = curr_node
                heapq.heappush(pq, (dist, neighbor))
                
    return distances, parent

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
            messagebox.showerror("Błąd", "Format: Start Koniec Waga (np. A B 5)")
            return None
    return edges

def run_algorithm():
    edges = get_edges_from_input()
    if edges is None: return
    start_node = entry_start.get().strip()
    
    graph = {}
    for u, v, w in edges:
        # Budujemy graf nieskierowany
        if u not in graph: graph[u] = {}
        if v not in graph: graph[v] = {}
        graph[u][v] = w
        graph[v][u] = w

    if start_node not in graph:
        messagebox.showerror("Błąd", f"Wierzchołek '{start_node}' nie istnieje!")
        return

    dist, parent = dijkstra(graph, start_node)
    
    text_result.delete("1.0", tk.END)
    if dist is None:
        messagebox.showerror("Błąd", "Dijkstra nie obsługuje wag ujemnych! Użyj Bellmana-Forda.")
    else:
        text_result.insert(tk.END, f"🚀 Start: {start_node} (Dijkstra)\n" + "="*35 + "\n")
        for node in sorted(dist.keys()):
            d = dist[node]
            path = get_path(parent, node)
            res_str = "Inf" if d == float("Inf") else str(d)
            text_result.insert(tk.END, f"📍 Do {node} | Koszt: {res_str}\n   Trasa: {path}\n\n")

def draw_graph():
    edges = get_edges_from_input()
    if not edges: return
    G = nx.Graph() # Nieskierowany (brak strzałek)
    for u, v, w in edges: G.add_edge(u, v, weight=w)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='gold', node_size=1500, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Wizualizacja Grafu Nieskierowanego (Dijkstra)")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Algorytm Dijkstry 🧭")
root.geometry("500x650")

tk.Label(root, text="Wprowadź krawędzie (np. A B 5):", font=("Arial", 11, "bold")).pack(pady=5)
text_edges = tk.Text(root, height=8, width=50)
text_edges.pack()

tk.Button(root, text="🎨 Pokaż Graf", command=draw_graph).pack(pady=5)

tk.Label(root, text="🏁 Start:", font=("Arial", 11, "bold")).pack()
entry_start = tk.Entry(root, justify="center", width=10)
entry_start.pack()

tk.Button(root, text="⚡ OBLICZ", command=run_algorithm, bg="#FFD700", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(root, text="WYNIKI I NAJKRÓTSZE TRASY:", font=("Arial", 11, "bold")).pack()
text_result = tk.Text(root, height=12, width=50)
text_result.pack(pady=5)

root.mainloop()