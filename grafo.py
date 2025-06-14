import random
from collections import deque

class Grafo:
    def __init__(self, dirigido=False, vertices_init=[]):
        self.dirigido = dirigido
        self.ady = {}
        for v in vertices_init:
            self.agregar_vertice(v)

    def agregar_vertice(self, v):
        if v not in self.ady:
            self.ady[v] = {}

    def borrar_vertice(self, v):
        if v in self.ady:
            for w in list(self.ady[v]):
                self.borrar_arista(v, w)
            del self.ady[v]

    def agregar_arista(self, v, w, peso=1):
        self.agregar_vertice(v)
        self.agregar_vertice(w)
        self.ady[v][w] = peso
        if not self.dirigido:
            self.ady[w][v] = peso

    def borrar_arista(self, v, w):
        if v in self.ady and w in self.ady[v]:
            del self.ady[v][w]
        if not self.dirigido and w in self.ady and v in self.ady[w]:
            del self.ady[w][v]

    def estan_unidos(self, v, w):
        return v in self.ady and w in self.ady[v]

    def peso_arista(self, v, w):
        if self.estan_unidos(v, w):
            return self.ady[v][w]
        raise ValueError(f"No existe arista entre {v} y {w}")

    def obtener_vertices(self):
        return list(self.ady.keys())

    def vertice_aleatorio(self):
        if not self.ady:
            raise ValueError("El grafo está vacío")
        return random.choice(self.obtener_vertices())

    def adyacentes(self, v):
        if v in self.ady:
            return list(self.ady[v].keys())
        raise ValueError(f"El vértice {v} no existe")

    def __str__(self):
        resultado = []
        for v in self.ady:
            for w in self.ady[v]:
                if self.dirigido or (v < w):  # Para evitar duplicados en no dirigido
                    resultado.append(f"{v} <--> {w} (peso {self.ady[v][w]})")
        return "\n".join(resultado)

    # calcula distancias mínimas entre todos los pares de vértices usando BFS desde cada vértice
    # guarda en un diccionario (v,u) la distancia (número de aristas) y devuelve la máxima distancia encontrada (diámetro del grafo)
    def calcular_distancias(self):
        V = self.obtener_vertices()
        distancias = {}
        max_dist = 0
        for v in V:
            distancias_v = self.bfs_distancias(v)
            for u in V:
                d = distancias_v.get(u, float('inf'))
                distancias[(v, u)] = d
                distancias[(u, v)] = d
                if d != float('inf'):
                    max_dist = max(max_dist, d)
        return distancias, max_dist

    # BFS para calcular la distancia mínima desde v a todos los otros vértices que puede alcanzar en el grafo
    # retorna un diccionario distancias con las distancias mínimas
    def bfs_distancias(self, v):
        distancias = {v: 0}
        cola = deque([v])
        while cola:
            actual = cola.popleft()
            for vecino in self.adyacentes(actual):
                if vecino not in distancias:
                    distancias[vecino] = distancias[actual] + 1
                    cola.append(vecino)
        return distancias