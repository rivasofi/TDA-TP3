# Escribir un algoritmo que, por backtracking, obtenga la solución óptima al problema (valga la redundancia) en la versión de optimización: Dado un grafo no
# dirigido y no pesado, y un valor k, determinar los k clusters para que la distancia máxima de cada cluster sea mínima. Para esto, considerar minimizar el
# máximo de las distancias máximas (es decir, de las distancias máximas de cada cluster, nos quedamos con la mayor, y ese valor es el que queremos minimizar).

# tengo un grafo no dirigido y no pesado y un k. Tengo que separar el grafo en k clusters sin nodos repetidos tales que pueda minimizar la maxima distancia
# mas grande

# ejemplo:

# Partición A:
# Cluster 1: diámetro = 1
# Cluster 2: diámetro = 4
# Máximo = 4, Suma = 5

# Partición B:
# Cluster 1: diámetro = 3
# Cluster 2: diámetro = 3
# Máximo = 3, Suma = 6

# me quedaría con la particion B porque su máximo es menor incluso si la suma de sus diámetros es mayor. Minimizo el peor caso
# dado que no puedo no poner un vértice, la pregunta ya no es "pongo, o no pongo?" sino que sería "¿en cuál pongo?"

from grafo import Grafo
from validador import calcular_distancia_max_cluster
import copy

# sol optima y sol temporal de tipo dicc cluster:[vertices]

def generar_clusters(k):
    clusters = {}
    for i in range(0, k):
        clusters[f"Cluster {i}"] = []
    return clusters

def clusters_vacios(clusters):
    for cluster, vertices in clusters.items():
        if len(vertices) == 0:
            return True
    return False

def calcular_mayor_diametro_cluster(grafo, clusters):
    distancia_maxima = 0
    for cluster, vertices in clusters.items():
        distancia = calcular_distancia_max_cluster(grafo, vertices)
        distancia_maxima = max(distancia_maxima, distancia)
    return distancia_maxima

#poda: ya no llego
def alcanzan_vertices(vertices_restantes, clusters):
    clusters_vacios_restantes = 0
    
    for cluster, valor in clusters.items():
        if len(valor) == 0:
            clusters_vacios_restantes += 1
    
    return vertices_restantes >= clusters_vacios_restantes

def clustering_bt(grafo, vertices, actual, sol_optima, sol_temporal, k):
    # ya asigne todos
    if actual >= len(vertices):
        if clusters_vacios(sol_temporal):
            return sol_optima
        if calcular_mayor_diametro_cluster(grafo, sol_temporal) < calcular_mayor_diametro_cluster(grafo, sol_optima):
            return copy.deepcopy(sol_temporal)
        else:
            return sol_optima

    vertice = vertices[actual]
    mejor_solucion = sol_optima
    # pongo el vertice en que cluster?
    
    for cluster, v in sol_temporal.items():
        #pruebo vertice en un cluster
        sol_temporal[cluster].append(vertice)
        
        vertices_restantes = len(vertices) - (actual + 1)
        #poda: no me alcanzan los vertices para llenar los clusters vacíos
        if not alcanzan_vertices(vertices_restantes, sol_temporal):
            sol_temporal[cluster].pop()
            continue  # paso al siguiente cluster
        
        #poda: ¿supero el diametro maximo de lo que ya tengo?
        if not clusters_vacios(sol_temporal):
            diametro_parcial = calcular_mayor_diametro_cluster(grafo, sol_temporal)
            diametro_optimo = calcular_mayor_diametro_cluster(grafo, sol_optima)
            if diametro_parcial >= diametro_optimo:
                sol_temporal[cluster].pop()
                continue
        
        incluyendo = clustering_bt(grafo, vertices, actual + 1, sol_optima, sol_temporal, k)
        
        diametro_incluyendo = calcular_mayor_diametro_cluster(grafo, incluyendo)
        diametro_mejor_solucion = calcular_mayor_diametro_cluster(grafo, mejor_solucion)
        
        if diametro_incluyendo < diametro_mejor_solucion:
            mejor_solucion = copy.deepcopy(incluyendo)
            
        #saco vertice de ese cluster
        sol_temporal[cluster].pop()

    return mejor_solucion

def clustering_optimizacion(grafo, k):
    # genero k clusters vacíos
    sol_optima = generar_clusters(k)
    sol_temporal = generar_clusters(k)
    vertices = grafo.obtener_vertices()

    # primera "poda", si la cantidad de vertices es menor a la cantidad de clusters
    # nunca voy a poder llenar k-clusters.

    if len(vertices) < k:
        return None, None

    clusters = clustering_bt(grafo, vertices, 0, sol_optima, sol_temporal, k)
    diametro = calcular_mayor_diametro_cluster(grafo, clusters)
    
    return clusters, diametro