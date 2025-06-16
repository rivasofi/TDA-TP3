# TDA-TP3
---

## Grupo integrado por
---
##### Barletta Brenda - 112184

##### Docampo Torrico Daniel Rodolfo - 112395

##### Rivas Sofia Belen - 112216

## Ejecución del Programa
---
Por defecto, haciendo `python3 main.py <archivo> <k>`, se ejecutará el algoritmo de backtracking, con el grafo del archivo pasado (la ruta predefinida es archivos_catedra/, por ende si se quiere probar con otro archivo, se debe pasar la ruta completa, relativa a esta carpeta), y un determinado valor de k.


Tanto el algoritmo de programación lineal como el de Louvain, se pueden correr con:
```bash
python3 pl.py
python3 louvain.py
```

Esto ejecutará, en caso de el de programación lineal, el algoritmo, con todos los archivos provistos por la cátedra, uno por uno, comparando la salida del algoritmo con la salida esperada.


En el caso del de louvain, se ejecutará el algoritmo con los archivos que creamos nosotros para probarlo, todos los que estén en la carpeta archivos_para_probar_louvain, y se compara la asignación que hace el algoritmo con la que esperamos que haga (como generamos n cliques, esperamos que asigne n clusters).


Si se quieren probar ambos algoritmos, pasando un archivo en particular, se debe hacer lo siguiente:
- Comentar el main actual de cada uno, y descomentar el que dejamos justo abajo.
- Una vez hecho esto, se pueden correr los algoritmos de la siguiente manera:
    - Para el de programación lineal: `python3 pl.py <ruta_al_archivo.txt> <k>`
    - Para el de Louvain: `python3 louvain.py <ruta_al_archivo.txt>`
