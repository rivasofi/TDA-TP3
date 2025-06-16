from parser import *
from grafo import Grafo
from backtracking import clustering_optimizacion
import sys
import time

def imprimir_asignaciones(clusters, diametro, duracion):
    print("\n\033[35mAsignación:\033[m")
    for cluster, vertices in clusters.items():
        print(f"{cluster}: {vertices}")
    print("Maxima distancia dentro del cluster: \033[92m", diametro, "\033[0m")
    print(f"\033[96mTiempo total de ejecución: {duracion:.2f} segundos\033[0m")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python main.py <archivo_grafo> <k>")
        sys.exit(1)

    #ruta predefinida como archivos_catedra/archivo
    #funciona con txt y csv
    archivo = f"archivos_catedra/{sys.argv[1]}"
    k = int(sys.argv[2])

    grafo_trabajo = cargar_grafo(archivo)
    inicio = time.time()
    clusters, diametro = clustering_optimizacion(grafo_trabajo, k)
    fin = time.time()
    imprimir_asignaciones(clusters, diametro, fin - inicio)
