import sys
from time import time
from pulp import *
from parser import cargar_grafo
from validador import *
import grafo

'''
Constantes para el problema:
- C = dist. máxima permitida entre vértices del mismo cluster
- k = cant. máxima de clusters permitidos

Variables:
    X_v,i = {
        1, si v pertenece al cluster i
        0, si v no pertenece al cluster i
    }, para todo v perteneciente a V, y para todo i entre 1 y k ==> V*k variables

    Y_i = {
        1, si se usó el cluster i
        0. si no se usó el cluster i
    }, para todo i entre 1 y k ==> k variables

Función Objetivo: Minimizar la cantidad de clusters utilizados
    min ∑_{i=1}^{k} Y_i

Restricciones:
    X_v,i <= Y_i
        Para que si X_v,i = 1, forcemos a que Y_i también valga 1, ya que se está usando el cluster i (hay que contarlo)
        V*k restricciones
    
    La sumatoria de todos los Y_i (con i entre 1 y k) debe ser <= k
        Para que no se puedan usar más de k clusters
        Una sola restricción

    La sumatoria de todos los X_v,i (i entre 1 y k) debe ser = 1 para todo vértice v
        Para que cada vértice pertenezca a un sólo cluster
        V restricciones

    X_u,i + X_v,i <= 1 para cada i entre 1 y k, y para cada par de vértices u,v cuya distancia sea > C
    Para que u y v no puedan estar en el mismo cluster si los separa una distancia > C
    k * |{(u,v) ∈ V x V : u < v y d(u,v) > C}| restricciones


    cantidad total de restricciones = |V| * k (activación) + 1 (límite) + |V| (asignación) + |P_C| * k (diámetro)
    ⇒ Total ≈ |V| * (k + 1) + 1 + |P_C| * k
'''


def construir_modelo(grafo, k, C, distancias):
    V = grafo.obtener_vertices()  # vértices
    modelo = LpProblem("Clustering_bajo_diametro", LpMinimize)  # queremos minimizar cantidad de clusters

    # variables
    x = {(v, i): LpVariable(f"x_{v}_{i}", 0, 1, LpBinary) for v in V for i in range(k)}
    y = {i: LpVariable(f"y_{i}", 0, 1, LpBinary) for i in range(k)}

    modelo += 0

    # para que cada vértice pertenezca sólo a un cluster
    for v in V:
        modelo += lpSum(x[v, i] for i in range(k)) == 1

    # para marcar que si un nodo está en un cluster i, y_i valga 1 (marcar que se usa el cluster i)
    for v in V:
        for i in range(k):
            modelo += x[v, i] <= y[i]

    # solo puede haber k clusters activos (no más), la sumatoria de todos los y_i no puede ser mayor a k
    modelo += lpSum(y[i] for i in range(k)) <= k

    # dos vértices que están a distancia > C no pueden estar en el mismo cluster
    for i in range(k): # para cada cluster
        for u in V:  
            for v in V:  
                if u >= v:  # ignorar repetidos
                    continue
                if distancias[(u, v)] > C:
                    # restricción si la distancia es > C:
                    modelo += x[u, i] + x[v, i] <= 1

    return modelo, x


# convierte la solución del modelo (variables binarias) en un diccionario de clusters
def extraer_clusters(x_vars, k):
    clusters = {i: [] for i in range(k)}
    for (v, i), var in x_vars.items():
        if var.varValue > 0.5:  # si se asignó a un cluster:
            clusters[i].append(v)
    return {i: verts for i, verts in clusters.items() if verts}


# copypaste de la de main.py
def imprimir_asignaciones(clusters, diametro, duracion):
    print("\n\033[35mAsignación:\033[m")
    for cluster, vertices in clusters.items():
        print(f"{cluster}: {vertices}")
    print(f"\nMaxima distancia dentro del cluster:\033[92m {diametro}\033[0m")


# main que ejecuta el algoritmo con todos los archivos de la cátedra y muestra la asignación que hace"
# muestra si el resultado del algoritmo coincide con el esperado por la cátedra
# uso: python3 pl.py
if __name__ == "__main__":
    archivos = [("10_3.txt", 2, 2), ("10_3.txt", 5, 1), ("22_3.txt", 3, 2), ("22_3.txt", 4, 2), ("22_3.txt", 10, 1), ("22_5.txt", 2, 2), ("22_5.txt", 7, 1), ("30_3.txt", 2, 3), ("30_3.txt", 6, 2), ("30_5.txt", 5, 2), ("40_5.txt", 3, 2), ("45_3.txt", 7, 3), ("50_3.txt", 3, 3)]

    for archivo, k, c_esperado in archivos:
        archivo = f"archivos_catedra/{archivo}"

        grafo = cargar_grafo(archivo)
        distancias, max_dist = grafo.calcular_distancias()

        print("\n\033[96m----------------------------------------------------------------")
        print(f"Archivo: {archivo}")
        print("----------------------------------------------------------------\033[0m")
        inicio = time()
        solucion_encontrada = False

        # probamos armar y resolver el modelo para cada C
        for C in range(max_dist + 1):
            modelo, x_vars = construir_modelo(grafo, k, C, distancias)

            # para que no imprima 389492 cosas, después de las pruebas, con dejar modelo.solve() anda
            modelo.solve(PULP_CBC_CMD(msg=False))  

            #encontró solución
            if modelo.status == 1:
                fin = time()
                clusters = extraer_clusters(x_vars, k)
                diametros = [calcular_distancia_max_cluster(grafo, nodos) for nodos in clusters.values()]
                diametro_max = max(diametros) if diametros else 0
                imprimir_asignaciones(clusters, diametro_max, fin - inicio)
                solucion_encontrada = True
                break

        if not solucion_encontrada:
            print("\033[31mNo se encontró solución para ningún valor entre 0 y C.\033[0m")

        if diametro_max == c_esperado:
            print(f"Máxima distancia esperada dentro del cluster: \033[92m{c_esperado}\033[0m")
        else:
            print(f"Máxima distancia esperada dentro del cluster: \033[31m{c_esperado}\033[0m")

        print(f"\033[96mTiempo total de ejecución: {fin-inicio:.2f} segundos\033[0m")

'''
# main para ejecutar el algoritmo con el archivo pasado y un cierto valor k, y mostrar la asignación que hace
# uso: python3 pl.py <ruta_archivo_grafo.txt> <k>
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python main_pl.py <archivo_grafo> <k_clusters>")
        sys.exit(1)

    archivo = sys.argv[1]
    k = int(sys.argv[2])

    grafo = cargar_grafo(archivo)
    distancias, max_dist = grafo.calcular_distancias()

    inicio = time()
    solucion_encontrada = False

    for C in range(max_dist + 1):
        modelo, x_vars = construir_modelo(grafo, k, C, distancias)
        modelo.solve(PULP_CBC_CMD(msg=False))

        if modelo.status == 1:
            clusters = extraer_clusters(x_vars, k)
            diametros = [calcular_distancia_max_cluster(grafo, nodos) for nodos in clusters.values()]
            diametro_max = max(diametros) if diametros else 0
            if validador_clustering(grafo, k, C, clusters):
                fin = time()
                imprimir_asignaciones(clusters, diametro_max, fin - inicio)
                solucion_encontrada = True
                break

    if not solucion_encontrada:
        print("\033[31mNo se encontró solución válida para ningún valor de C.\033[0m")

'''