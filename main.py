# dfa_expendedora_imagen.py — Máquina expendedora con 6 símbolos (a-f)
import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch

# === Definición del DFA según la imagen ===
states = {f"q{i}" for i in range(7)}          # q0 a q6
alphabet = {"a", "b", "c", "d", "e", "f"}     # 6 símbolos

# Transiciones secuenciales
delta = {
    ("q0", "a"): "q1",
    ("q1", "b"): "q2",
    ("q2", "c"): "q3",
    ("q3", "d"): "q4",
    ("q4", "e"): "q5",
    ("q5", "f"): "q6",
}

q0 = "q0"
F = {"q6"}  # Estado final: Finalizar acción

# Nombres largos para mostrar en la gráfica (según la imagen)
nombres = {
    "q0": "Inicio de funcionamiento\n(encender)",
    "q1": "Seleccionar producto",
    "q2": "Ingresar moneda S/1",
    "q3": "Ingresar moneda S/2",
    "q4": "Ingresar moneda S/5",
    "q5": "Confirmar compra",
    "q6": "Entregar producto\nFinalizar acción"
}

# === Simulación ===
def run(s):
    q = q0
    steps = [q0]
    for i, ch in enumerate(s):
        if ch not in alphabet:
            raise ValueError(f"Carácter '{ch}' no permitido (solo a-f)")
        if (q, ch) not in delta:
            raise ValueError(f"Sin transición desde {nombres[q].replace(chr(10),' ')} con '{ch}' en paso {i+1}")
        q = delta[(q, ch)]
        steps.append(q)
    return steps, steps[-1] in F

# === Grafo y layout ===
G = nx.MultiDiGraph()
G.add_nodes_from(states)
for (q, a), p in delta.items():
    G.add_edge(q, p, key=a, label=a)

# Posiciones fijas para una vista vertical (similar a la imagen)
pos = {
    "q0": (0, 3.0),
    "q1": (0, 2.0),
    "q2": (0, 1.0),
    "q3": (0, 0.0),
    "q4": (0, -1.0),
    "q5": (0, -2.0),
    "q6": (0, -3.0),
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
    linewidths = [3 if n in F else 1 for n in nodes]
    
    # Dibujar nodos
    nx.draw_networkx_nodes(G, pos, nodelist=nodes,
                          node_size=node_sizes,
                          node_color=node_colors,
                          linewidths=linewidths,
                          edgecolors='black')
    
    # Etiquetas con nombres largos
    labels = {n: nombres[n] for n in nodes}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=8)
    
    # Dibujar arcos
    seen = {}
    for u, v, k, d in G.edges(keys=True, data=True):
        if u == v:
            # No hay bucles en este DFA, pero mantenemos por si acaso
            x, y = pos[u]
            arrow = FancyArrowPatch((x, y), (x+0.1, y+0.1),
                                   connectionstyle="arc3,rad=0.4",
                                   arrowstyle='-|>',
                                   mutation_scale=18,
                                   color='black')
            plt.gca().add_patch(arrow)
            plt.text(x+0.15, y+0.15, d['label'],
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
    
    # Círculo doble para el estado final
    for state in F:
        x, y = pos[state]
        circle = plt.Circle((x, y), 0.12, fill=False, edgecolor='black', linewidth=2)
        plt.gca().add_patch(circle)
    
    plt.axis('off')
    titulo = f"Paso {idx}: {nombres[current].replace(chr(10),' ')}"
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
        s = input("Ingrese la secuencia (solo a,b,c,d,e,f): ").strip()
    
    if not s:
        print("ERROR: Cadena vacía")
        return
    
    try:
        steps, accepted = run(s)
        print(f"{'ACEPTA' if accepted else 'RECHAZA'} (estado final: {nombres[steps[-1]].replace(chr(10),' ')})")
        
        plt.ion()
        plt.figure(figsize=(6, 8))
        
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