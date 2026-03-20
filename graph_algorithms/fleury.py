import tkinter as tk
from tkinter import messagebox
import networkx as nx
import matplotlib.pyplot as plt
import copy

def is_bridge(G, u, v):
    # Krawędź jest mostem, jeśli jej usunięcie zwiększa liczbę komponentów spójności
    if G.degree(u) == 1:
        return False
    
    orig_nodes = nx.number_connected_components(G)
    G.remove_edge(u, v)
    new_nodes = nx.number_connected_components(G)
    G.add_edge(u, v) # Przywracamy po teście
    
    return new_nodes > orig_nodes

def fleury(G_orig, start_node):
    G = copy.deepcopy(G_orig)
    path = [start_node]
    curr = start_node
    
    while G.number_of_edges() > 0:
        neighbors = list(G.neighbors(curr))
        if not neighbors: break
        
        chosen_v = neighbors[0]
        # Staramy się nie wybierać mostu
        for v in neighbors:
            if not is_bridge(G, curr, v):
                chosen_v = v
                break
        
        path.append(chosen_v)
        G.remove_edge(curr, chosen_v)
        curr = chosen_v
        
    return path

def get_edges_from_input():
    edges_text = text_edges.get("1.0", tk.END).strip().split('\n')
    edges = []
    for line in edges_text:
        if not line.strip(): continue
        try:
            u, v = line.split()[:2] # Wagi są tu opcjonalne, Fleury ich nie potrzebuje
            edges.append((u, v))
        except ValueError:
            messagebox.showerror("Błąd", "Format: A B")
            return None
    return edges

def run_algorithm():
    edges = get_edges_from_input()
    if not edges: return
    start_node = entry_start.get().strip()
    
    G = nx.Graph()
    G.add_edges_from(edges)
    
    # Sprawdzenie warunku Eulera (wszystkie wierzchołki muszą mieć parzysty stopień dla cyklu)
    odd_degrees = [v for v, d in G.degree() if d % 2 != 0]
    
    if start_node not in G:
        messagebox.showerror("Błąd", "Start nie istnieje!")
        return

    text_result.delete("1.0", tk.END)
    if len(odd_degrees) != 0 and len(odd_degrees) != 2:
        text_result.insert(tk.END, "⚠️ Graf nie posiada ścieżki Eulera!\n(Więcej niż 2 wierzchołki mają nieparzysty stopień)")
        return

    result_path = fleury(G, start_node)
    
    text_result.insert(tk.END, f"🚀 Trasa Eulera (Fleury):\n" + "="*30 + "\n")
    text_result.insert(tk.END, " -> ".join(result_path))

def draw_graph():
    edges = get_edges_from_input()
    if not edges: return
    G = nx.Graph()
    G.add_edges_from(edges)
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='lightgreen', node_size=1500, font_weight='bold')
    plt.title("Graf dla Algorytmu Fleury'ego")
    plt.show()

# GUI Setup
root = tk.Tk()
root.title("Algorytm Fleury'ego (Cykl Eulera) 🎨")
root.geometry("500x600")

tk.Label(root, text="Wprowadź krawędzie (np. A B):", font=("Arial", 11, "bold")).pack(pady=5)
text_edges = tk.Text(root, height=8, width=50)
text_edges.pack()

tk.Button(root, text="🎨 Pokaż Graf", command=draw_graph).pack(pady=5)

tk.Label(root, text="🏁 Start (Wierzchołek):", font=("Arial", 11, "bold")).pack()
entry_start = tk.Entry(root, justify="center", width=10)
entry_start.pack()

tk.Button(root, text="⚡ ZNAJDŹ CYKL/ŚCIEŻKĘ", command=run_algorithm, bg="orange", font=("Arial", 12, "bold")).pack(pady=10)

tk.Label(root, text="WYNIK (KOLEJNOŚĆ WIERZCHOŁKÓW):", font=("Arial", 11, "bold")).pack()
text_result = tk.Text(root, height=10, width=50)
text_result.pack(pady=5)

root.mainloop()