from grafo import Grafo
from collections import defaultdict
from parser import cargar_grafo
from validador import calcular_distancia_max_cluster
import time
import os
import sys

# con esto calculamos el cambio en modularidad al mover un nodo a una comunidad
# se me pasó en la versión anterior, por eso tardaba tanto, estaba calculando la modularidad completa cada vez que se movía un nodo

# parámetros:
# - m: suma total de pesos de aristas / 2
# - k_i_in: suma de pesos de aristas del nodo hacia la comunidad destino
# - k_i: grado (peso total de aristas) del nodo
# - sum_tot: suma total de grados (peso total de aristas) de nodos en la comunidad destino
# - sum_in: suma total de pesos de aristas internas de la comunidad destino

# la fórmula para el cambio de modularidad era:
# delta(Q) = [ (sum_in + 2*k_i_in)/2m - ((sum_tot + k_i)/2m)^2 ] - [ sum_in/2m - (sum_tot/2m)^2 - (k_i/2m)^2 ]
def calcular_delta_modularidad(m, k_i_in, k_i, sum_tot, sum_in):
    m2 = 2 * m
    part1 = (sum_in + 2 * k_i_in) / m2 - ((sum_tot + k_i) / m2) ** 2
    part2 = (sum_in / m2) - (sum_tot / m2) ** 2 - (k_i / m2) ** 2
    return part1 - part2


# reubicamos nodos en comunidades para maximizar el aumento de modularidad
def primera_etapa(grafo, comunidades, nodo_a_comunidad):
    m = sum(grafo.peso_arista(v, w) for v, w in grafo.aristas()) / 2

    # inicializar sumas necesarias para modularidad
    grado_total = {}  # suma de grados de nodos en comunidad
    peso_interno = {} # suma de pesos internos en comunidad

    for comunidad_id, nodos in comunidades.items():
        grado_total[comunidad_id] = sum(grafo.grado(n) for n in nodos)
        peso_interno[comunidad_id] = sum(
            grafo.peso_arista(n1, n2)
            for n1 in nodos for n2 in grafo.adyacentes(n1)
            if n2 in nodos
        ) / 2

    hubo_cambio = True
    while hubo_cambio:
        hubo_cambio = False
        for nodo in grafo.obtener_vertices():
            comunidad_actual = nodo_a_comunidad[nodo]
            comunidades[comunidad_actual].remove(nodo)

            grado_nodo = grafo.grado(nodo)
            grado_total[comunidad_actual] -= grado_nodo

            internos_reducidos = sum(
                grafo.peso_arista(nodo, vecino)
                for vecino in grafo.adyacentes(nodo)
                if nodo_a_comunidad[vecino] == comunidad_actual
            )
            peso_interno[comunidad_actual] -= internos_reducidos

            mejor_comunidad = comunidad_actual
            mejor_mod = 0  # el delta modularidad para quedarse en su comunidad (0 si no se mueve)

            vecinos = grafo.adyacentes(nodo)
            comunidades_vecinas = set(nodo_a_comunidad[vec] for vec in vecinos)

            for comunidad in comunidades_vecinas:
                sum_tot = grado_total.get(comunidad, 0)
                sum_in = peso_interno.get(comunidad, 0)

                # k_i_in = suma pesos arista del nodo hacia la comunidad "comunidad"
                k_i_in = sum(
                    grafo.peso_arista(nodo, vecino)
                    for vecino in vecinos
                    if nodo_a_comunidad[vecino] == comunidad
                )

                delta_mod = calcular_delta_modularidad(m, k_i_in, grado_nodo, sum_tot, sum_in)

                if delta_mod > mejor_mod:
                    mejor_mod = delta_mod
                    mejor_comunidad = comunidad

            # asignamos el nodo a la mejor comunidad
            comunidades[mejor_comunidad].add(nodo)
            nodo_a_comunidad[nodo] = mejor_comunidad

            grado_total[mejor_comunidad] = grado_total.get(mejor_comunidad, 0) + grado_nodo
            peso_interno[mejor_comunidad] = peso_interno.get(mejor_comunidad, 0) + 2 * sum(
                grafo.peso_arista(nodo, vecino)
                for vecino in grafo.adyacentes(nodo)
                if nodo_a_comunidad[vecino] == mejor_comunidad
            )

            if mejor_comunidad != comunidad_actual:
                hubo_cambio = True

    return nodo_a_comunidad, comunidades


# crea un nuevo grafo donde cada comunidad es un supernodo
def segunda_etapa(grafo, comunidades):
    nuevo_grafo = Grafo(dirigido=False)
    id_por_comunidad = list(comunidades.keys())
    nodo_a_comunidad = {}

    for idx, comunidad in enumerate(id_por_comunidad):
        for nodo in comunidades[comunidad]:
            nodo_a_comunidad[nodo] = idx
        nuevo_grafo.agregar_vertice(idx)

    for v, w in grafo.aristas():
        c_v = nodo_a_comunidad[v]
        c_w = nodo_a_comunidad[w]
        peso = grafo.peso_arista(v, w)

        if nuevo_grafo.estan_unidos(c_v, c_w):
            nuevo_grafo.ady[c_v][c_w] += peso
            if not grafo.dirigido:
                nuevo_grafo.ady[c_w][c_v] += peso
        else:
            nuevo_grafo.agregar_arista(c_v, c_w, peso)

    return nuevo_grafo, nodo_a_comunidad


# algoritmo principal
def louvain(grafo):
    nodo_a_comunidad = {v: v for v in grafo.obtener_vertices()}
    comunidades = {v: set([v]) for v in grafo.obtener_vertices()}

    while True:
        nodo_a_comunidad, comunidades = primera_etapa(grafo, comunidades, nodo_a_comunidad)
        nuevo_grafo, mapeo = segunda_etapa(grafo, comunidades)

        if len(nuevo_grafo.obtener_vertices()) == len(grafo.obtener_vertices()):
            break  # no hubo fusiones nuevas

        grafo = nuevo_grafo
        nodo_a_comunidad = {nodo: comunidad for nodo, comunidad in mapeo.items()}
        comunidades = defaultdict(set)
        for nodo, comunidad in nodo_a_comunidad.items():
            comunidades[comunidad].add(nodo)

    resultado = defaultdict(set)
    for nodo, comunidad in nodo_a_comunidad.items():
        resultado[comunidad].add(nodo)

    return list(resultado.values())


# auxiliares para pruebas


# para comparar resultados
def generar_particion_esperada(num_cliques, tamano_clique):
    particion = {}
    nodo_id = 0
    for i in range(num_cliques):
        for _ in range(tamano_clique):
            particion[nodo_id] = i
            nodo_id += 1
    return particion


# para printear las asignaciones esperadas y obtenidas
def imprimir_particion(particion):
    clusters = {}
    for nodo, cluster in particion.items():
        clusters.setdefault(cluster, []).append(nodo)
    for c, nodos in sorted(clusters.items()):
        print(f"Cluster {c} : {sorted(nodos)}")


# para que no fallen las pruebas si asigna en otro orden
def son_equivalentes(part1, part2):
    grupos1 = {}
    grupos2 = {}
    for nodo in part1:
        grupos1.setdefault(part1[nodo], set()).add(nodo)
        grupos2.setdefault(part2[nodo], set()).add(nodo)
    return sorted([sorted(g) for g in grupos1.values()]) == sorted([sorted(g) for g in grupos2.values()])


def imprimir_asignaciones(clusters, diametro, duracion):
    print("\n\033[35mAsignación:\033[m")
    for cluster, vertices in clusters.items():
        print(f"{cluster}: {sorted(list(vertices))}")
    print(f"\033[96mTiempo total de ejecución: {duracion:.2f} segundos\033[0m")


def ejecutar_test(archivo):
    print(f"\n\033[35mArchivo: {archivo}\033[0m")
    inicio = time.time()

    grafo = cargar_grafo(f"archivos_para_probar_louvain/{archivo}")
    resultado_lista = louvain(grafo)
    resultado = {nodo: i for i, comunidad in enumerate(resultado_lista) for nodo in comunidad}

    # intentamos obtener la partición esperada desde el nombre del archivo
    partes = archivo.replace(".txt", "").split("_")
    num_cliques = int(partes[0])
    tamano_clique = int(partes[-1])
    particion_esperada = generar_particion_esperada(num_cliques, tamano_clique)

    if son_equivalentes(resultado, particion_esperada):
        print("\033[92m[PASÓ LA PRUEBA]\033[0m")
    else:
        print("\033[31m[FALLÓ LA PRUEBA]\033[0m")

    fin = time.time()
    print(f"\033[36m- Tardó: {fin - inicio:.3f} segundos\033[0m")


# main que ejecuta el test para todos los archivos que haya en la carpeta "archivos_para_probar_louvain"
# uso: python3 louvain.py
if __name__ == "__main__":
    archivos = [archivo for archivo in os.listdir("archivos_para_probar_louvain") if archivo.endswith(".txt")]
    print("\n\033[96mArchivos a testear (si pasa la prueba, es porque louvain asignó un cluster por clique, que es lo que se espera que haga):\n")
    for archivo in archivos:
        print(f"- {archivo}")
    print("\033[0m")

    for archivo in archivos:
        ejecutar_test(archivo)


'''
# main para ejecutar el algoritmo louvain y mostrar la asignación que hace
# uso: python3 louvain.py <ruta_archivo_grafo.txt>
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python louvain.py <archivo_grafo>")
        sys.exit(1)

    archivo = sys.argv[1]

    grafo = cargar_grafo(archivo)
    inicio = time.time()
    resultado_lista = louvain(grafo)
    fin = time.time()

    clusters = {i: set(comunidad) for i, comunidad in enumerate(resultado_lista)}

    diametro = max(
        calcular_distancia_max_cluster(grafo, comunidad)
        for comunidad in resultado_lista
    )

    imprimir_asignaciones(clusters, diametro, fin - inicio)
'''