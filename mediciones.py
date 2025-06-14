import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from random import seed

from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import scipy as sp

from util import time_algorithm

from script import *

from backtracking import clustering_optimizacion

from parser import *



def graficar_medicion_k_3(results, x):
    ax: plt.Axes
    fig, ax = plt.subplots()
    ax.plot(x, [results[i] for i in x], label="Medición")
    ax.set_title('Tiempo de ejecución de clustering_optimizacion')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Tiempo de ejecución (s)')

    # Ajuste exponencial: f(V) = c1 * c2^V
    f = lambda x, c1, c2: c1 * (c2 ** x)
    c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x], p0=(1e-6, 2.0))
    print(f"c_1 = {c[0]}, c_2 = {c[1]}")
    r = np.sum((f(np.array(x), *c) - [results[n] for n in x]) ** 2)
    print(f"Error cuadrático total: {r}")
    ax.plot(x, [f(n, *c) for n in x], 'r--', label="Ajuste exponencial")
    ax.legend()
    fig.savefig(f"ajuste-k_3.png", dpi=300, bbox_inches='tight')
    graficar_error_k_3(c, results, x, f)

def graficar_error_k_3(c, results, x, f):
    ax: plt.Axes
    fig, ax = plt.subplots()
    errors = [np.abs(f(n, *c) - results[n]) for n in x]
    ax.plot(x, errors)
    ax.set_title('Error de ajuste')
    ax.set_xlabel('Cantidad de nodos V')
    ax.set_ylabel('Error absoluto (s)')
    fig.savefig(f"error-k_3.png", dpi=300, bbox_inches='tight')



# def graficar_medicion_n_variable(results, x):
#     ax: plt.Axes
#     fig, ax = plt.subplots()
#     ax.plot(x, [results[i] for i in x], label="Medición")
#     ax.set_title('Tiempo de ejecución de algoritmo') #CHEQUEAR NAME
#     ax.set_xlabel('Largo cadena recibida')
#     ax.set_ylabel('Tiempo de ejecución (s)')
#     None

#     # scipy nos pide una función que recibe primero x y luego los parámetros a ajustar:
#     f = lambda x, c1, c2: c1 * x + c2 

#     c, pcov = sp.optimize.curve_fit(f, x, [results[n] for n in x])


#     print(f"c_1 = {c[0]}, c_2 = {c[1]}")
#     r = np.sum((c[0] * x + c[1] - [results[n] for n in x])**2)
#     print(f"Error cuadrático total: {r}")
#     ax.plot(x, [c[0] * n + c[1] for n in x], 'r--', label="Ajuste")
#     ax.legend()
#     fig.savefig(f"ajuste-n_variable.png", dpi=300, bbox_inches='tight')
#     graficar_error_n_variable(c, results, x)


# def graficar_error_n_variable(c, results, x):
#     ax: plt.Axes
#     fig, ax = plt.subplots()
#     errors = [np.abs(c[0] * n + c[1] - results[n]) for n in x]
#     ax.plot(x, errors)
#     ax.set_title('Error de ajuste')
#     ax.set_xlabel('Largo cadena recibida')
#     ax.set_ylabel('Error absoluto (s)')
#     None
#     fig.savefig(f"error-n_variable.png", dpi=300, bbox_inches='tight')


def obtener_volumenes(minimo, maximo, cantidad):
    return np.linspace(minimo, maximo, cantidad).astype(int)


def generar_grafo(n):
    archivo = f"{n}.txt"
    generar_grafo_txt(n, aristas_extra=n*2)
    return cargar_grafo(archivo)

def obtener_args_algoritmo_k_3(n):
    grafo = generar_grafo(n)
    k=3
    return [grafo,k]

def ejecutar_algoritmo(grafo, k):
    return clustering_optimizacion(grafo, k)

if __name__ == '__main__':
    seed(12345)
    np.random.seed(12345)
    sns.set_theme()

    
    
    x_n = obtener_volumenes(10,20,6)

    results = time_algorithm(ejecutar_algoritmo, x_n, obtener_args_algoritmo_k_3)
    graficar_medicion_k_3(results, x_n)