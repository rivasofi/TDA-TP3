import random

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
