from grafo import Grafo

def cargar_grafo(ruta_archivo):
    aristas = []

    with open(ruta_archivo) as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea or linea.startswith("#"):
                continue
            u, v = map(int, linea.split(","))
            aristas.append((u, v))

    # obtengo los vertices
    vertices = set()
    
    for u, v in aristas:
        vertices.add(u)
        vertices.add(v)

    grafo = Grafo()
    
    for v in vertices:
        grafo.agregar_vertice(v)
        
    for u, v in aristas:
        grafo.agregar_arista(u, v)

    return grafo