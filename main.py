# dfa_expendedora_imagen.py
import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch

# ===== Estados =====
states = {f"q{i}" for i in range(8)}  # q0 a q7
alphabet = {"a", "b", "c", "d", "e", "f"}

# ===== Transiciones =====
delta = {
    ("q0", "a"): "q0",
    ("q0", "b"): "q2",
    ("q0", "c"): "q3",
    ("q0", "d"): "q1",

    ("q1", "b"): "q2",
    ("q1", "c"): "q4",

    ("q2", "b"): "q2",
    ("q2", "c"): "q1",
    ("q2", "d"): "q3",

    ("q3", "c"): "q2",
    ("q3", "d"): "q4",

    ("q4", "d"): "q4",
    ("q4", "e"): "q5",
    ("q4", "b"): "q7",

    ("q5", "e"): "q6",

    ("q6", "f"): "q7",
}

q0 = "q0"
F = {"q7"}

# ===== Nombres =====
nombres = {
    "q0": "Inicio de funcionamiento\n(encender)",
    "q1": "Ingresar moneda S/1",
    "q2": "Ingresar moneda S/2",
    "q3": "Ingresar moneda S/5",
    "q4": "Seleccionar producto",
    "q5": "Confirmar compra",
    "q6": "Entregar producto",
    "q7": "Finalizar acción"
}

# ===== Simulación =====
def run(s):
    q = q0
    steps = [q0]

    for i, ch in enumerate(s):
        if ch not in alphabet:
            raise ValueError(
                f"Carácter '{ch}' no permitido."
            )

        if (q, ch) not in delta:
            raise ValueError(
                f"Sin transición desde "
                f"{nombres[q].replace(chr(10),' ')} "
                f"con '{ch}'"
            )

        q = delta[(q, ch)]
        steps.append(q)

    return steps, q in F

# ===== Crear grafo =====
G = nx.MultiDiGraph()
G.add_nodes_from(states)

for (q, a), p in delta.items():
    G.add_edge(q, p, key=a, label=a)

# ===== Posiciones =====
pos = {
    "q0": (-3, 0),
    "q1": (-1, 1),
    "q2": (-1, 0),
    "q3": (-1, -1),
    "q4": (1, 0),
    "q5": (3, 0),
    "q6": (3, -1),
    "q7": (3, -2),
}

# ===== Punto medio =====
def _mid(p1, p2, offset=0.12):
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    nx_, ny_ = -dy, dx
    L = (nx_**2 + ny_**2) ** 0.5

    if L == 0:
        return mx, my

    return mx + offset * nx_ / L, my + offset * ny_ / L

# ===== Dibujar =====
def draw_step(current, idx, sym=None):
    plt.clf()

    nodes = list(G.nodes())

    node_colors = [
        'lightblue' if n == current else 'white'
        for n in nodes
    ]

    node_sizes = [
        1200 if n == current else 900
        for n in nodes
    ]

    linewidths = [
        3 if n in F else 1.5
        for n in nodes
    ]

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nodes,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors='black',
        linewidths=linewidths
    )

    labels = {n: nombres[n] for n in nodes}

    nx.draw_networkx_labels(
        G,
        pos,
        labels=labels,
        font_size=8
    )

    seen = {}

    for u, v, k, d in G.edges(keys=True, data=True):

        if u == v:
            x, y = pos[u]

            arrow = FancyArrowPatch(
                (x, y),
                (x + 0.01, y + 0.01),
                connectionstyle="arc3,rad=0.5",
                arrowstyle='-|>',
                mutation_scale=20
            )

            plt.gca().add_patch(arrow)

            plt.text(
                x + 0.25,
                y + 0.25,
                d["label"],
                fontsize=10,
                weight='bold'
            )

        else:
            i = seen.get((u, v), 0)
            seen[(u, v)] = i + 1

            rad = 0.20 if i % 2 == 0 else -0.20

            nx.draw_networkx_edges(
                G,
                pos,
                edgelist=[(u, v)],
                arrows=True,
                arrowstyle='-|>',
                arrowsize=20,
                connectionstyle=f"arc3,rad={rad}"
            )

            lx, ly = _mid(
                pos[u],
                pos[v],
                0.15 if i % 2 == 0 else -0.15
            )

            plt.text(
                lx,
                ly,
                d["label"],
                fontsize=10,
                weight='bold'
            )

    # círculo doble del estado final
    for state in F:
        x, y = pos[state]

        circle = plt.Circle(
            (x, y),
            0.18,
            fill=False,
            linewidth=2
        )

        plt.gca().add_patch(circle)

    plt.axis('off')

    titulo = f"Paso {idx}: {nombres[current].replace(chr(10),' ')}"

    if sym:
        titulo += f" | símbolo '{sym}'"

    plt.title(titulo)
    plt.tight_layout()
    plt.pause(1)

# ===== Programa principal =====
def main():

    if len(sys.argv) > 1:
        s = sys.argv[1].strip()
    else:
        s = input(
            "Ingrese la secuencia: "
        ).strip()

    try:
        steps, accepted = run(s)

        print(
            "ACEPTA"
            if accepted
            else "RECHAZA"
        )

        plt.ion()
        plt.figure(figsize=(10, 6))

        draw_step(steps[0], 0)

        for i, ch in enumerate(s, 1):
            draw_step(
                steps[i],
                i,
                ch
            )

        plt.ioff()
        plt.show()

    except ValueError as e:
        print("RECHAZA:", e)

if __name__ == "__main__":
    main()