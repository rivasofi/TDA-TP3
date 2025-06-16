import os
from grafo import Grafo

# el grafo vendrían siendo cliques de tamaño tamano_clique, conectados entre sí por una sola arista
# muchas comunidades densas, todas del mismo tamaño, ideal para louvain porque será natural asignar cada clique a una comunidad
def generar_cliques_con_puentes(num_cliques, tamano_clique):
    grafo = Grafo()
    nodo_id = 0
    prev_ultimo = None
    for _ in range(num_cliques):
        nodos = list(range(nodo_id, nodo_id + tamano_clique))
        for v in nodos:
            grafo.agregar_vertice(v)
        for i in range(len(nodos)):
            for j in range(i + 1, len(nodos)):
                grafo.agregar_arista(nodos[i], nodos[j])
        if prev_ultimo is not None:
            grafo.agregar_arista(prev_ultimo, nodos[0])  # puente
        prev_ultimo = nodos[-1]
        nodo_id += tamano_clique
    return grafo

# escribir el archivo
def guardar_grafo_en_archivo(grafo, nombre_archivo):
    path = f"archivos_para_probar_louvain/{nombre_archivo}.txt"
    with open(path, "w") as f:
        f.write("# after the war I went back to new york\n")
        for v, w in grafo.aristas():
            f.write(f"{v},{w}\n")
    return path

def generar_archivos_de_prueba():
    # dani cambiá los valores acá si queres probar más variantes
    tamanios_clique = [5, 10, 20, 30, 100]
    cantidades_cliques = [10, 50, 100, 200, 100]

    for cantidad in cantidades_cliques:
        for tamanio in tamanios_clique:
            grafo = generar_cliques_con_puentes(cantidad, tamanio)
            nombre_archivo = f"{cantidad}_cliques_de_tamanio_{tamanio}"
            guardar_grafo_en_archivo(grafo, nombre_archivo)

if __name__ == "__main__":
    generar_archivos_de_prueba()