from grafo import Grafo
from collections import deque
import copy
from greedy import maximizar_modularidad

# sol optima y sol temporal de tipo dicc cluster:[vertices]

def obtener_solucion_inicial_greedy(grafo, k):
    lista_comunidades = maximizar_modularidad(grafo)
    todos_nodos = set(grafo.obtener_vertices())
    asignados = set()

    sol_optima = generar_clusters(k)
    i = 0

    for comunidad in lista_comunidades:
        for nodo in comunidad:
            sol_optima[f"Cluster {i % k}"].append(nodo)
            asignados.add(nodo)
        i += 1

    nodos_faltantes = todos_nodos - asignados
    for nodo in nodos_faltantes:
        sol_optima[f"Cluster {i % k}"].append(nodo)
        i += 1

    return sol_optima

def bfs_distancias(grafo, origen):
    distancias = {}
    visitado = set()
    cola = deque([(origen, 0)])
    visitado.add(origen)

    while cola:
        actual, d = cola.popleft()
        distancias[actual] = d
        for vecino in grafo.adyacentes(actual):
            if vecino not in visitado:
                visitado.add(vecino)
                cola.append((vecino, d + 1))
    return distancias

def precalcular_distancias(grafo):
    distancias = {}
    vertices = grafo.obtener_vertices()
    for v in vertices:
        dist_v = bfs_distancias(grafo, v)
        for w, d in dist_v.items():
            if w != v:
                clave = tuple(sorted((w, v)))
                distancias[clave] = d
    return distancias

def calcular_distancia_max(vertices, distancias):
    if len(vertices) <= 1:
        return 0

    distancia_maxima = 0
    
    for i in range(len(vertices)):
        for j in range(i + 1, len(vertices)):
            clave = (min(vertices[i], vertices[j]), max(vertices[i], vertices[j]))
            distancia = distancias.get(clave, float('inf'))
            distancia_maxima = max(distancia_maxima, distancia)
    return distancia_maxima

def generar_clusters(k):
    clusters = {}
    for i in range(0, k):
        clusters[f"Cluster {i}"] = []
    return clusters

def calcular_mayor_diametro_cluster(clusters, distancias):
    distancia_maxima = 0
    for vertices in clusters.values():
        if len(vertices) > 1:
            distancia = calcular_distancia_max(vertices, distancias)
            distancia_maxima = max(distancia_maxima, distancia)
    return distancia_maxima

#poda: ya no llego
def alcanzan_vertices(vertices_restantes, clusters):
    clusters_vacios_restantes = 0
    
    for cluster, valor in clusters.items():
        if len(valor) == 0:
            clusters_vacios_restantes += 1
    
    return vertices_restantes >= clusters_vacios_restantes

# poda para evitar explorar combinaciones equivalentes entre sí
def es_cluster_vacio_anterior(clusters, indice_actual):
    i = 0
    for cluster, vertices in clusters.items():
        if i >= indice_actual:
            break
        if len(vertices) == 0:
            return True
        i += 1
    return False

# poda para evitar que un cluster crezca desmedidamente en relacion a otros
def cluster_desbalanceado(clusters, total_vertices, k):
    max_permitido = (total_vertices + k - 1) // k  # redondeo hacia arriba
    for cluster, vertices in clusters.items():
        if len(vertices) > max_permitido:
            return True
    return False

def clustering_bt(grafo, vertices, actual, sol_optima, sol_temporal, k, distancias, diametros_actuales, mejor_diametro_actual):
    # ya asigne todos
    if actual >= len(vertices):
        diametro_actual = max(diametros_actuales.values())
        if mejor_diametro_actual is None or diametro_actual < mejor_diametro_actual:
            return copy.deepcopy(sol_temporal), diametro_actual
        return sol_optima, mejor_diametro_actual
    
    vertice = vertices[actual]
    mejor_solucion = sol_optima
    # pongo el vertice en que cluster?
    
    for cluster in sol_temporal:
        #poda de simetria
        if not sol_temporal[cluster] and es_cluster_vacio_anterior(sol_temporal, list(sol_temporal.keys()).index(cluster)):
            continue
        
        nuevo_diametro = diametros_actuales[cluster]
        for otro in sol_temporal[cluster]:
            clave = tuple(sorted((vertice, otro)))
            nuevo_diametro = max(nuevo_diametro, distancias.get(clave, float('inf')))
        
        diametro_anterior = diametros_actuales[cluster]
        sol_temporal[cluster].append(vertice)
        diametros_actuales[cluster] = nuevo_diametro
        
        vertices_restantes = len(vertices) - (actual + 1)
        #poda: no me alcanzan los vertices para llenar los clusters vacíos: "determinar los 
        # k clusters para que la distancia máxima de cada cluster sea mínima". Piden siempre k clusters
        if not alcanzan_vertices(vertices_restantes, sol_temporal):
            sol_temporal[cluster].pop()
            diametros_actuales[cluster] = diametro_anterior
            continue  # paso al siguiente cluster
        
        #poda: desbalanceo
        if cluster_desbalanceado(sol_temporal, len(vertices), k):
            sol_temporal[cluster].pop()
            diametros_actuales[cluster] = diametro_anterior
            continue
            
        #poda: ¿supero el diametro maximo de lo que ya tengo?
        diametro_parcial = max(diametros_actuales.values())
        if mejor_diametro_actual is not None and diametro_parcial >= mejor_diametro_actual:
            sol_temporal[cluster].pop()
            diametros_actuales[cluster] = diametro_anterior
            continue
        
        incluyendo, nuevo_diametro_sol = clustering_bt(grafo, vertices, actual + 1, mejor_solucion, sol_temporal, k, distancias, diametros_actuales, mejor_diametro_actual)
        
        if mejor_diametro_actual is None or nuevo_diametro_sol < mejor_diametro_actual:
            mejor_solucion = copy.deepcopy(incluyendo)
            mejor_diametro_actual = nuevo_diametro_sol
            
        #saco vertice de ese cluster
        sol_temporal[cluster].pop()
        diametros_actuales[cluster] = diametro_anterior

    return mejor_solucion, mejor_diametro_actual

def clustering_optimizacion(grafo, k):
    # usamos greedy como solución inicial para establecer cota
    sol_optima = obtener_solucion_inicial_greedy(grafo, k)
    
    # si no se pudo obtener una solución inicial válida, retornamos None
    if sol_optima is None:
        return None, None
    
    sol_temporal = generar_clusters(k)
    
    vertices = sorted(grafo.obtener_vertices(), key=lambda v: -len(grafo.adyacentes(v)))

    if len(vertices) < k:
        return None, None

    distancias = precalcular_distancias(grafo)
    mejor_diametro = calcular_mayor_diametro_cluster(sol_optima, distancias)
    diametros_actuales = {nombre: 0 for nombre in sol_temporal}

    clusters, diametro = clustering_bt( grafo, vertices, 0, sol_optima, sol_temporal, k, distancias, diametros_actuales, mejor_diametro)
    
    return clusters, diametro
