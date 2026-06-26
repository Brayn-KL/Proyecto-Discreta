# dfa_expendedora.py — Máquina expendedora (8 estados, solo 'a')
import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch

# === Definición del DFA (Máquina Expendedora) ===
# Estados: q0=Inicio, q1=Moneda S/1, q2=Moneda S/2, q3=Moneda S/5,
#          q4=Seleccionar, q5=Confirmar, q6=Entregar, q7=Finalizar
states = {f"q{i}" for i in range(8)}
alphabet = {"a", "b"}  # Solo 'a' tiene transiciones

# Transiciones: todas con 'a' y van al siguiente estado
delta = {
    ("q0", "a"): "q1",
    ("q1", "a"): "q2",
    ("q2", "a"): "q3",
    ("q3", "a"): "q4",
    ("q4", "a"): "q5",
    ("q5", "a"): "q6",
    ("q6", "a"): "q7",
    # No hay transiciones con 'b' (se rechazarán)
}

q0 = "q0"
F = {"q7"}  # Estado final: Finalizar acción

# Nombres largos para mostrar en la gráfica
nombres_estados = {
    "q0": "Inicio",
    "q1": "Moneda S/1",
    "q2": "Moneda S/2",
    "q3": "Moneda S/5",
    "q4": "Seleccionar",
    "q5": "Confirmar",
    "q6": "Entregar",
    "q7": "Finalizar"
}

# === Simulación ===
def run(s):
    q = q0
    steps = [q0]
    for i, ch in enumerate(s):
        if ch not in alphabet:
            raise ValueError(f"Carácter '{ch}' no permitido (solo a y b)")
        if (q, ch) not in delta:
            raise ValueError(f"Sin transición desde {nombres_estados[q]} con '{ch}' en paso {i+1}")
        q = delta[(q, ch)]
        steps.append(q)
    return steps, steps[-1] in F

# === Grafo y layout ===
G = nx.MultiDiGraph()
G.add_nodes_from(states)
for (q, a), p in delta.items():
    G.add_edge(q, p, key=a, label=a)

# Posiciones fijas para visualizar la secuencia (vertical)
pos = {
    "q0": (0, 3.5),
    "q1": (0, 2.5),
    "q2": (0, 1.5),
    "q3": (0, 0.5),
    "q4": (0, -0.5),
    "q5": (0, -1.5),
    "q6": (0, -2.5),
    "q7": (0, -3.5),
}

# === Dibujo ===
def _mid(p1, p2, offset=0.10):
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    nx_, ny_ = -dy, dx
    L = (nx_**2 + ny_**2) ** 0.5
    if L == 0:
        return mx, my
    return mx + offset * nx_ / L, my + offset * ny_ / L

def draw_step(current, idx, sym=None):
    plt.clf()
    nodes = list(G.nodes())
    
    # Colores y tamaños
    node_colors = ['lightblue' if n == current else 'white' for n in nodes]
    node_sizes = [900 if n == current else 600 for n in nodes]
    edge_colors = ['red' if n == current else 'black' for n in nodes]
    linewidths = [3 if n in F else 1 for n in nodes]
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, nodelist=nodes,
                          node_size=node_sizes,
                          node_color=node_colors,
                          linewidths=linewidths,
                          edgecolors=edge_colors)
    
    # Etiquetas con nombres largos
    labels = {n: nombres_estados[n] for n in nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)
    
    # Dibujar arcos
    seen = {}
    for u, v, k, d in G.edges(keys=True, data=True):
        if u == v:
            # Bucle (no hay en este DFA, pero se mantiene por si acaso)
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
            i = seen.get((u, v), 0)
            seen[(u, v)] = i + 1
            rad = 0.2 if i % 2 == 0 else -0.2
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)],
                                  connectionstyle=f"arc3,rad={rad}",
                                  arrows=True,
                                  arrowstyle='-|>',
                                  arrowsize=20,
                                  edge_color='black')
            lx, ly = _mid(pos[u], pos[v], 0.10 if i % 2 == 0 else -0.10)
            plt.text(lx, ly, d['label'], fontsize=10,
                    ha='center', va='center', weight='bold')
    
    # Círculo doble para estado final
    for state in F:
        x, y = pos[state]
        circle = plt.Circle((x, y), 0.12, fill=False, edgecolor='black', linewidth=2)
        plt.gca().add_patch(circle)
    
    plt.axis('off')
    titulo = f"Paso {idx}: {nombres_estados[current]}"
    if sym:
        titulo += f" | símbolo: '{sym}'"
    plt.title(titulo)
    plt.tight_layout()
    plt.pause(1.0)

# === Función principal ===
def main():
    if len(sys.argv) > 1:
        s = sys.argv[1].strip()
    else:
        s = input("Ingrese secuencia de pasos (solo a y b): ").strip()
    
    if not s:
        print("ERROR: Cadena vacía")
        return
    
    try:
        steps, accepted = run(s)
        print(f"{'ACEPTA' if accepted else 'RECHAZA'} (estado final: {nombres_estados[steps[-1]]})")
        
        plt.ion()
        plt.figure(figsize=(6, 10))  # Ajuste para vista vertical
        
        draw_step(steps[0], 0)
        for i, ch in enumerate(s, 1):
            draw_step(steps[i], i, ch)
        
        plt.ioff()
        plt.show(block=True)
        
    except ValueError as e:
        print(f"RECHAZA: {e}")
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    main()