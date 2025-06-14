import random
import sys


# Recibe un n (cantidad vértices) y un aristas_extra (cantidad de aristas además de las n-1 necesarias)
# Genera un grafo no dirigido, no pesado, conectado, con n vértices.
def generar_grafo_txt(n, aristas_extra):

    aristas = set()
    nodos = list(range(n))
    random.shuffle(nodos)

    for i in range(1, n):
        u = nodos[i]
        v = random.choice(nodos[:i])
        aristas.add(tuple(sorted((u, v))))

    while len(aristas) < n - 1 + aristas_extra:
        u, v = random.sample(nodos, 2)
        if u != v:
            aristas.add(tuple(sorted((u, v))))

    archivo_salida = f"{n}.txt"
    with open(archivo_salida, "w") as f:
        f.write("# turururu\n")
        for u, v in sorted(aristas):
            f.write(f"{u},{v}\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 script.py <cantidad_nodos> [aristas_extra]")
        sys.exit(1)

    n = int(sys.argv[1])
    aristas_extra = int(sys.argv[2]) if len(sys.argv) > 2 else 0

    generar_grafo_txt(n, aristas_extra)
