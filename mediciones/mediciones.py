import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from random import seed

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp

from util import time_algorithm

from script import *

from archivos_para_probar_louvain.script_louvain import *

from backtracking import clustering_optimizacion

from parser import *

from pl import *

from louvain import louvain



def graficar_medicion_k_3_bt(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de clustering_optimizacion con k = 3')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * (c2 ** x)
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x], p0=(1e-3, 1.1), maxfev =5000)
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")
    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste exponencial")
    ax.legend()
    fig.savefig(f"ajuste-k_3_bt.png", dpi=300, bbox_inches='tight')
    graficar_error_k_3_bt(c, results, x, f)

def graficar_error_k_3_bt(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_3_bt.png", dpi=300, bbox_inches='tight')

def graficar_medicion_k_6(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de clustering_optimizacion con k = 6')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * (c2 ** x)
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x], p0=(1e-3, 1.1), maxfev =5000)
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")
    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste exponencial")
    ax.legend()
    fig.savefig(f"ajuste-k_6.png", dpi=300, bbox_inches='tight')
    graficar_error_k_6(c, results, x, f)

def graficar_error_k_6(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_6.png", dpi=300, bbox_inches='tight')


def graficar_medicion_k_3_pl(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de algoritmo pl con k = 3')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * (c2 ** x)
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")
    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste exponencial")
    ax.legend()
    fig.savefig(f"ajuste-k_3_pl.png", dpi=300, bbox_inches='tight')
    graficar_error_k_3_pl(c, results, x, f)

def graficar_error_k_3_pl(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_3_pl.png", dpi=300, bbox_inches='tight')


def graficar_medicion_k_6_pl(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de algoritmo pl con k = 6')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * (c2 ** x)
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")
    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste exponencial")
    ax.legend()
    fig.savefig(f"ajuste-k_6_pl.png", dpi=300, bbox_inches='tight')
    graficar_error_k_6_pl(c, results, x, f)

def graficar_error_k_6_pl(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_6_pl.png", dpi=300, bbox_inches='tight')


def graficar_medicion_k_9_pl(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de algoritmo pl con k = 9')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * (c2 ** x)
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")
    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste exponencial")
    ax.legend()
    fig.savefig(f"ajuste-k_9_pl.png", dpi=300, bbox_inches='tight')
    graficar_error_k_9_pl(c, results, x, f)

def graficar_error_k_9_pl(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_9_pl.png", dpi=300, bbox_inches='tight')



def graficar_medicion_k_3_pl_log(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de algoritmo PL con k = 3 (ajuste n log n)')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * x * np.log2(x) + c2
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")

    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste n log n")
    ax.legend()
    fig.savefig(f"ajuste-k_3_pl_nlogn.png", dpi=300, bbox_inches='tight')
    graficar_error_k_3_pl_log(c, results, x, f)

def graficar_error_k_3_pl_log(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste (n log n)')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_3_pl_nlogn.png", dpi=300, bbox_inches='tight')


def graficar_medicion_k_6_pl_log(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de algoritmo PL con k = 6 (ajuste n log n)')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * x * np.log2(x) + c2
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")

    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste n log n")
    ax.legend()
    fig.savefig(f"ajuste-k_6_pl_nlogn.png", dpi=300, bbox_inches='tight')
    graficar_error_k_6_pl_log(c, results, x, f)

def graficar_error_k_6_pl_log(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste (n log n)')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_6_pl_nlogn.png", dpi=300, bbox_inches='tight')

def graficar_medicion_louvain(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de algoritmo de louvain con cliques de tamaño 100')
    ax.set_xlabel('Cantidad de cliques')
    ax.set_ylabel('Tiempo de ejecución (s)')

    f = lambda x, c1, c2: c1 * x * np.log2(x) + c2
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")

    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste n log n")
    ax.legend()
    fig.savefig(f"ajuste-louvain_t_100.png", dpi=300, bbox_inches='tight')
    graficar_error_louvain(c, results, x, f)

def graficar_error_louvain(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste (n log n)')
    ax.set_xlabel('Cantidad de cliques')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-louvain_t_100.png", dpi=300, bbox_inches='tight')



def obtener_volumenes(minimo, maximo, cantidad):
    return np.linspace(minimo, maximo, cantidad).astype(int)


def generar_grafo_louvain(cantidad):
    tamanio = 50 #numero de vértices en un clique
    grafo = generar_cliques_con_puentes(cantidad, tamanio)
    nombre_archivo = f"{cantidad}_cliques_de_tamanio_{tamanio}"
    guardar_grafo_en_archivo(grafo, nombre_archivo)
    return grafo

def generar_grafo(n):
    archivo = f"{n}.txt"
    generar_grafo_txt(n, aristas_extra= int(n*0.3))
    return cargar_grafo(archivo)


def obtener_args_algoritmo_k_3_bt(n):
    grafo = generar_grafo(n)
    k=3
    return [grafo,k]

def obtener_args_algoritmo_k_6_bt(n):
    grafo = generar_grafo(n)
    k=6
    return [grafo,k]

def obtener_args_algoritmo_k_3_pl(n):

    grafo = generar_grafo(n)
    k = 3
    distancias, max_dist = grafo.calcular_distancias()
    return [grafo, k, max_dist, distancias]

def obtener_args_algoritmo_k_6_pl(n):

    grafo = generar_grafo(n)
    k = 6
    distancias, max_dist = grafo.calcular_distancias()
    return [grafo, k, max_dist, distancias]

def obtener_args_algoritmo_k_9_pl(n):

    grafo = generar_grafo(n)
    k = 9
    distancias, max_dist = grafo.calcular_distancias()
    return [grafo, k, max_dist, distancias]

def obtener_args_louvain(cantidad):
    grafo = generar_grafo_louvain(cantidad)
    return [grafo]


def ejecutar_algoritmo_bt(grafo, k):
    print(f"Corriendo algoritmo")
    return clustering_optimizacion(grafo, k)

def ejecutar_algoritmo_pl(grafo, k, max_dist, distancias):
    print(f"Corriendo algoritmo")
    solucion_encontrada = False

    for C in range(max_dist + 1):
        modelo, x_vars = construir_modelo(grafo, k, C, distancias)
        modelo.solve(PULP_CBC_CMD(msg=False))

        if modelo.status == 1:
            clusters = extraer_clusters(x_vars, k)
            diametros = [calcular_distancia_max_cluster(grafo, nodos) for nodos in clusters.values()]
            diametro_max = max(diametros) if diametros else 0
            if validador_clustering(grafo, k, C, clusters):
                solucion_encontrada = True
                break

    if not solucion_encontrada:
        print("\033[31mNo se encontró solución válida para ningún valor de C.\033[0m")

def ejecutar_algoritmo_louvain(grafo):
    print(f"Corriendo Algoritmo")
    return louvain(grafo)

if __name__ == '__main__':
    seed(12345)
    np.random.seed(12345)
    sns.set_theme()

    inicio = time()
    
    x_n = obtener_volumenes(20,50,5)

    x_l = obtener_volumenes(50, 300, 6)

    print("k3_bt")
    inicio_k3_bt = time()
    results_k_3_bt = time_algorithm(ejecutar_algoritmo_bt, x_n, obtener_args_algoritmo_k_3_bt)
    graficar_medicion_k_3_bt(results_k_3_bt, x_n)
    #Error cuadrático total: 0.6508555824227805
    final_k3_bt = time()
    print(f"tarda en medir {final_k3_bt - inicio_k3_bt:.2f}s")
    #tarda en medir 7663.60s


    print("k6_bt")
    inicio_k6_bt = time()
    results_k_6_bt = time_algorithm(ejecutar_algoritmo_bt, x_n, obtener_args_algoritmo_k_6_bt)
    graficar_medicion_k_6(results_k_6_bt, x_n)
    #Error cuadrático total: 3.4027106668773985
    final_k6_bt = time()
    print(f"tarda en medir {final_k6_bt - inicio_k6_bt:.2f}s")
    #tarda en medir 205.33s

    print("k3_pl")
    inicio_k3_pl = time()
    results_k_3_pl = time_algorithm(ejecutar_algoritmo_pl, x_n, obtener_args_algoritmo_k_3_pl)
    graficar_medicion_k_3_pl(results_k_3_pl, x_n)
    #Error cuadrático total: 0.2974281745599414
    final_k3_pl = time()
    print(f"tarda en medir {final_k3_pl - inicio_k3_pl:.2f}s")
    #tarda en medir 144.64s

    print("k3_pl_log")
    inicio_k3_pl_log = time()
    results_k_3_pl_log = time_algorithm(ejecutar_algoritmo_pl, x_n, obtener_args_algoritmo_k_3_pl)
    graficar_medicion_k_3_pl_log(results_k_3_pl_log, x_n)
    #Error cuadrático total: 5.267768310007417
    final_k3_pl_log = time()
    print(f"tarda en medir {final_k3_pl_log - inicio_k3_pl_log:.2f}s")
    #tarda en medir 146.19s

    print("k6_pl")
    inicio_k6_pl = time()
    results_k_6_pl = time_algorithm(ejecutar_algoritmo_pl, x_n, obtener_args_algoritmo_k_6_pl)
    graficar_medicion_k_6_pl(results_k_6_pl, x_n)
    #Error cuadrático total: 6.159233102842426
    final_k6_pl = time()
    print(f"tarda en medir {final_k6_pl - inicio_k6_pl:.2f}s")
    #tarda en medir 719.33s

    print("k6_pl_log")
    inicio_k6_pl_log = time()
    results_k_6_pl_log = time_algorithm(ejecutar_algoritmo_pl, x_n, obtener_args_algoritmo_k_6_pl)
    graficar_medicion_k_6_pl_log(results_k_6_pl_log, x_n)
    #Error cuadrático total: 261.1167876171511
    final_k6_pl_log = time()
    print(f"tarda en medir {final_k6_pl_log - inicio_k6_pl_log:.2f}s")
    #tarda en medir 714.86s

    print("k9_pl")
    inicio_k9_pl = time()
    results_k_9_pl = time_algorithm(ejecutar_algoritmo_pl, x_n, obtener_args_algoritmo_k_9_pl)
    graficar_medicion_k_9_pl(results_k_9_pl, x_n)
    #Error cuadrático total: 148.21555988420957
    final_k9_pl = time()
    print(f"tarda en medir {final_k9_pl - inicio_k9_pl:.2f}s")
    #tarda en medir 2068.74s

    print("louvain")
    inicio_louvain = time()
    results_louvain = time_algorithm(ejecutar_algoritmo_louvain, x_l, obtener_args_louvain)
    graficar_medicion_louvain(results_louvain, x_l)
    #Error cuadrático total: 0.323231042741351
    final_louvain = time()
    print(f"tarda en medir {final_louvain - inicio_louvain:.2f}s")
    #tarda en medir 137.77s


    fin = time()

    total = fin - inicio
    print(f"tarda en medir {total:.2f}s")
    # total medicion 11800.45s
