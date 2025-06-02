# Demostrar que el Problema de Clustering por bajo diámetro se encuentra en NP.

# Para los primeros dos puntos considerar la versión de decisión del problema de Clustering por bajo diámetro: Dado un grafo no dirigido y no pesado, un
# número entero k y un valor C, ¿es posible separar los vértices en a lo sumo k grupos/clusters disjuntos, de tal forma que todo vértice pertenezca a un
# cluster, y que la distancia máxima dentro de cada cluster sea a lo sumo C? (Si un cluster queda vacío o con un único elemento, considerar la distancia
# máxima como 0).

# Al calcular las distancias se tienen en cuenta tanto las aristas entre vértices dentro del cluster, como cualquier otra arista dentro del grafo.

# NP: problemas para los que existe un certificador eficiente → se pueden validar en tiempo polinomial.

# Todo problema que se puede resolver en tiempo polinomial (P) también puede ser verificado en tiempo polinomial (NP).

from grafo import Grafo
from collections import deque

# asumo que la solución propuesta es un diccionario del tipo cluster-n: [vertices]

def calcular_distancia_vertices(grafo, v1, v2):
    visitados = set([v1]) #arranco desde ese
    cola = deque([v1])
    camino_aux = {}
    camino = []
    
    #bfs para caminos minimos
    while cola:
        actual = cola.popleft()
        if actual == v2:
            vertice = actual
            while vertice != v1:
                camino.append(vertice)
                vertice = camino_aux[vertice]
            camino.append(v1)
            return len(camino) - 1
        for adyacente in grafo.adyacentes(actual):
            if adyacente not in visitados:
                cola.append(adyacente)
                visitados.add(adyacente)
                camino_aux[adyacente] = actual
    
    #no hay camino
    return None

def calcular_distancia_max_cluster(grafo, vertices):
    if len(vertices) <= 1:
        return 0
    
    distancia_maxima = 0
    
    #para cada vertice v dentro del cluster calculo distancia (v,w) siendo w otro vertice del cluster
    #todos deben poder llegar a todos pero no necesariamente entre ellos
    
    for v in vertices:
        for w in vertices:
            if v == w:
                continue
            distancia = calcular_distancia_vertices(grafo, v, w)
            #si no hay camino el cluster es invalido, debemos poder llegar de todos a todos con 1 o mas de distancia, pongo infinito si no hay así lo considera
            #invalido en la validación posterior
            if distancia == None: distancia = float('inf')
            distancia_maxima = max(distancia, distancia_maxima)
            
    return distancia_maxima

# False si la solucion no es la correcta
def validador_clustering(grafo, k, c, solucion_propuesta):
    
    #a lo sumo k grupos
    if len(solucion_propuesta) > k:
        return False
    
    usados = set()
    total_vertices = set(grafo.obtener_vertices())
    
    #cuales vertices uso? lleno usados
    for cluster, vertices in solucion_propuesta.items():
        for vertice in vertices:
            if vertice not in usados:
                usados.add(vertice)
            else:
                #si repetimos vertice, está mal, no es clustering correcto
                return False

    #todo vértice pertenezca a un cluster
    #uso todos?
    if usados != total_vertices:
        return False
    
    #distancia máxima dentro de cada cluster sea a lo sumo C
    
    for cluster, vertices in solucion_propuesta.items():
        distancia_maxima = calcular_distancia_max_cluster(grafo, vertices)
        if distancia_maxima > c:
            return False

    return True

"""
Dado el código realizado en el presente archivo, encontramos las siguientes complejidades:

calcular_distancia_vertices(grafo, v1, v2) -> O(V+E)
calcular_distancia_max_cluster(grafo, vertices) -> O(n^2 * (V+E))
validador_clustering(grafo, k, c, solucion_propuesta) -> O(k * V^2 * (V+E))

Con estas funciones, podemos verificar si una solución propuesta para el problema de clustering por bajo diámetro es correcta o no, realizandolo en tiempo
polinomial con respecto al tamaño de su entrada (grafo(V,E), k, c).

Se concluye por lo tanto que el presente problema pertenece a NP al poder validarse una solución del mismo en tiempo polinomial.
"""