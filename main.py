# dfa_cli_compacto.py — versión modificada y corregida
import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch

# === Definición del DFA ===
states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}  # 7 estados
alphabet = {"a", "b"}

# Transiciones completas
delta = {
    ("q0", "a"): "q1", ("q0", "b"): "q2",
    ("q1", "a"): "q3", ("q1", "b"): "q4",
    ("q2", "a"): "q5", ("q2", "b"): "q2",  # bucle en q2
    ("q3", "a"): "q6", ("q3", "b"): "q0",
    ("q4", "a"): "q1", ("q4", "b"): "q6",
    ("q5", "a"): "q5", ("q5", "b"): "q4",  # bucle en q5
    ("q6", "a"): "q6", ("q6", "b"): "q6"   # bucle en q6 (estado final)
}

q0 = "q0"
F = {"q6"}

# === Simulación ===
def run(s):
    q = q0
    steps = [q0]
    for i, ch in enumerate(s):
        if ch not in alphabet:
            raise ValueError(f"Carácter '{ch}' no válido en posición {i}")
        if (q, ch) not in delta:
            raise ValueError(f"Sin transición desde {q} con '{ch}' en pos {i}")
        q = delta[(q, ch)]
        steps.append(q)
    return steps, steps[-1] in F

# === Grafo y layout ===
G = nx.MultiDiGraph()
G.add_nodes_from(states)
for (q, a), p in delta.items():
    G.add_edge(q, p, key=a, label=a)

# Layout fijo para consistencia
pos = {
    'q0': (0.0, 0.0),
    'q1': (-1.0, 0.5),
    'q2': (1.0, 0.5),
    'q3': (-1.5, -0.5),
    'q4': (0.0, 1.0),
    'q5': (1.5, -0.5),
    'q6': (0.0, -1.0)
}

# === Dibujo de bucles y arcos ===
def _mid(p1, p2, offset=0.10):
    """Calcula punto medio con desplazamiento para etiquetas"""
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    nx_, ny_ = -dy, dx
    L = (nx_**2 + ny_**2) ** 0.5
    if L == 0:
        return mx, my
    return mx + offset * nx_ / L, my + offset * ny_ / L

def draw_step(current, idx, sym=None):
    """Dibuja un paso de la simulación"""
    plt.clf()
    
    # Nodos
    nodes = list(G.nodes())
    node_colors = ['lightblue' if n == current else 'white' for n in nodes]
    node_sizes = [900 if n == current else 600 for n in nodes]
    edge_colors = ['red' if n == current else 'black' for n in nodes]
    linewidths = [3 if n in F else 1 for n in nodes]
    
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, 
                          node_size=node_sizes,
                          node_color=node_colors,
                          linewidths=linewidths,
                          edgecolors=edge_colors)
    nx.draw_networkx_labels(G, pos)
    
    # Dibujar transiciones
    seen = {}
    for u, v, k, d in G.edges(keys=True, data=True):
        if u == v:
            # Bucle
            x, y = pos[u]
            arrow = FancyArrowPatch((x, y), (x + 0.1, y + 0.1),
                                   connectionstyle="arc3,rad=0.4",
                                   arrowstyle='-|>',
                                   mutation_scale=18,
                                   color='black')
            plt.gca().add_patch(arrow)
            plt.text(x + 0.15, y + 0.15, d['label'], 
                    fontsize=10, ha='center', va='center')
        else:
            # Arco entre estados diferentes
            i = seen.get((u, v), 0)
            seen[(u, v)] = i + 1
            rad = 0.2 if i % 2 == 0 else -0.2
            
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                                  connectionstyle=f"arc3,rad={rad}",
                                  arrows=True,
                                  arrowstyle='-|>',
                                  arrowsize=20,
                                  edge_color='black')
            
            # Etiqueta
            lx, ly = _mid(pos[u], pos[v], 0.10 if i % 2 == 0 else -0.10)
            plt.text(lx, ly, d['label'], fontsize=10, 
                    ha='center', va='center', weight='bold')
    
    # Estado final (doble círculo)
    for state in F:
        x, y = pos[state]
        circle = plt.Circle((x, y), 0.12, fill=False, edgecolor='black', linewidth=2)
        plt.gca().add_patch(circle)
    
    plt.axis('off')
    plt.title(f"Paso {idx}: {current}" + (f" | símbolo: '{sym}'" if sym else ""))
    plt.tight_layout()
    plt.pause(1.0)

# === Función principal ===
def main():
    # Obtener cadena de entrada
    if len(sys.argv) > 1:
        s = sys.argv[1].strip()
    else:
        s = input("Ingrese cadena (solo a y b): ").strip()
    
    # Validar entrada
    if not s:
        print("ERROR: Cadena vacía")
        return
    
    try:
        # Ejecutar simulación
        steps, accepted = run(s)
        print(f"{'ACEPTA' if accepted else 'RECHAZA'} (estado final: {steps[-1]})")
        
        # Visualizar
        plt.ion()
        plt.figure(figsize=(8, 6))
        
        # Paso inicial
        draw_step(steps[0], 0)
        
        # Pasos siguientes
        for i, ch in enumerate(s, 1):
            draw_step(steps[i], i, ch)
        
        # Mantener la figura abierta
        plt.ioff()
        plt.show(block=True)
        
    except ValueError as e:
        print(f"RECHAZA: {e}")
        return
    except Exception as e:
        print(f"ERROR inesperado: {e}")
        return

# === Punto de entrada ===
if __name__ == "__main__":
    main()