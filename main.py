import sys
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import FancyArrowPatch

# ================= DFA =================
states = {"q0", "q1", "q2", "q3", "q4", "q5", "q6"}
alphabet = {"a", "b"}

delta = {
    ("q0", "a"): "q1",
    ("q0", "b"): "q2",
    ("q1", "a"): "q3",
    ("q1", "b"): "q4",
    ("q2", "a"): "q2",
    ("q2", "b"): "q5",
    ("q3", "a"): "q6",
    ("q3", "b"): "q0",
    ("q4", "a"): "q1",
    ("q4", "b"): "q6",
    ("q5", "a"): "q3",
    ("q5", "b"): "q5",
    ("q6", "a"): "q4",
    ("q6", "b"): "q0"
}

q0 = "q0"
F = {"q6"}

# ================= SIMULACIÓN =================
def run(cadena):
    estado = q0
    pasos = [estado]
    for i, simbolo in enumerate(cadena):
        if (estado, simbolo) not in delta:
            raise ValueError(
                f"No existe transición desde {estado} con '{simbolo}'"
            )

        estado = delta[(estado, simbolo)]
        pasos.append(estado)

    return pasos, estado in F


# ================= GRAFO =================
G = nx.MultiDiGraph()
G.add_nodes_from(states)

for (q, a), p in delta.items():
    G.add_edge(q, p, key=a, label=a)

pos = nx.spring_layout(G, seed=7)


# ================= POSICIÓN DE ETIQUETAS =================
def punto_medio(p1, p2, offset=0.10):
    (x1, y1), (x2, y2) = p1, p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    nx_, ny_ = -dy, dx
    L = (nx_**2 + ny_**2)**0.5 or 1

    return (
        mx + offset * nx_ / L,
        my + offset * ny_ / L
    )


# ================= DIBUJO =================
def draw_step(actual, paso, simbolo=None):
    plt.clf()

    nodos = list(G.nodes())

    nx.draw_networkx_nodes(
        G,
        pos,
        nodelist=nodos,
        node_size=[
            1000 if n == actual else 700
            for n in nodos
        ],
        linewidths=[
            3 if n in F else 1
            for n in nodos
        ],
        edgecolors="black"
    )

    nx.draw_networkx_labels(G, pos)

    vistos = {}

    for u, v, k, d in G.edges(keys=True, data=True):

        # Bucle
        if u == v:
            x, y = pos[u]
            plt.gca().add_patch(
                FancyArrowPatch(
                    (x, y),
                    (x + 0.001, y + 0.001),
                    connectionstyle="arc3,rad=0.45",
                    arrowstyle="-|>",
                    mutation_scale=18
                )
            )

            plt.text(
                x,
                y + 0.18,
                d["label"],
                fontsize=11,
                ha="center"
            )
            continue

        i = vistos.get((u, v), 0)
        vistos[(u, v)] = i + 1

        rad = 0.25 if i % 2 == 0 else -0.25

        nx.draw_networkx_edges(
            G,
            pos,
            edgelist=[(u, v)],
            connectionstyle=f"arc3,rad={rad}",
            arrows=True,
            arrowstyle="-|>",
            arrowsize=20
        )

        lx, ly = punto_medio(
            pos[u],
            pos[v],
            0.10 if i % 2 == 0 else -0.10
        )

        plt.text(
            lx,
            ly,
            d["label"],
            fontsize=11,
            ha="center"
        )

    plt.axis("off")

    titulo = f"Paso {paso}: {actual}"
    if simbolo:
        titulo += f" | símbolo: '{simbolo}'"

    plt.title(titulo)
    plt.pause(1)


# ================= MAIN =================
if __name__ == "__main__":

    cadena = (
        sys.argv[1]
        if len(sys.argv) > 1
        else input("Cadena (a/b): ").strip()
    )

    try:
        pasos, acepta = run(cadena)

        print(
            "ACEPTA" if acepta else "RECHAZA",
            f"(estado final: {pasos[-1]})"
        )

        plt.ion()

        draw_step(pasos[0], 0)

        for i, simbolo in enumerate(cadena, 1):
            draw_step(
                pasos[i],
                i,
                simbolo
            )

        plt.ioff()
        plt.show()

    except Exception as e:
        print("ERROR:", e)