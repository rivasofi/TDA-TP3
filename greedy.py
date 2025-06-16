import sys
import os
import time
from grafo import Grafo
from main import cargar_grafo
from backtracking import calcular_distancia_max_cluster

def calcular_modularidad(grafo, lista_comunidades, total_peso_aristas):
    modularidad = 0
    for comunidad in lista_comunidades:
        for nodo_u in comunidad:
            for nodo_v in comunidad:
                peso_uv = grafo.peso_arista(nodo_u, nodo_v) if grafo.estan_unidos(nodo_u, nodo_v) else 0
                grado_u = grafo.grado(nodo_u)
                grado_v = grafo.grado(nodo_v)
                modularidad += peso_uv - (grado_u * grado_v) / (2 * total_peso_aristas)
    return modularidad / (2 * total_peso_aristas)

def maximizar_modularidad(grafo):
    # Inicializar: cada nodo en su propia comunidad
    comunidades = []
    for nodo in grafo.obtener_vertices():
        comunidades.append(set([nodo]))

    total_peso_aristas = sum(grafo.peso_arista(v, w) for v, w in grafo.aristas()) / 2

    # REGLA GREEDY:
    # En cada paso, se consideran todas las fusiones posibles de comunidades,
    # y se elige aquella que más aumenta la modularidad total.
    
    hubo_mejora = True
    while hubo_mejora:
        hubo_mejora = False
        mejor_incremento_modularidad = 0
        mejor_par_a_fusionar = None

        for i in range(len(comunidades)):
            for j in range(i + 1, len(comunidades)):
                comunidad_1 = comunidades[i]
                comunidad_2 = comunidades[j]

                # Simular la fusión
                comunidades_fusionadas = []
                for k in range(len(comunidades)):
                    if k != i and k != j:
                        comunidades_fusionadas.append(comunidades[k])
                nueva_comunidad = comunidad_1.union(comunidad_2)
                comunidades_fusionadas.append(nueva_comunidad)

                modularidad_actual = calcular_modularidad(grafo, comunidades, total_peso_aristas)
                modularidad_fusionada = calcular_modularidad(grafo, comunidades_fusionadas, total_peso_aristas)
                incremento = modularidad_fusionada - modularidad_actual

                if incremento > mejor_incremento_modularidad:
                    mejor_incremento_modularidad = incremento
                    mejor_par_a_fusionar = (i, j)
                    hubo_mejora = True

        if hubo_mejora:
            i, j = mejor_par_a_fusionar
            nueva_comunidad = comunidades[i].union(comunidades[j])
            nuevas_comunidades = []
            for k in range(len(comunidades)):
                if k != i and k != j:
                    nuevas_comunidades.append(comunidades[k])
            nuevas_comunidades.append(nueva_comunidad)
            comunidades = nuevas_comunidades

    return comunidades