# -*- coding: utf-8 -*-
"""
Complejidad de List Scheduling: Versión de la Guía vs. Versión Optimizada
Problema: Pm || Cmax

Análisis algorítmico:
  - Versión de la guía (Listing 2):
      Almacena la lista de trabajos en la tupla del heap y la copia en cada asignación
      (asignados + [trabajo]). Copiar una lista de k elementos cuesta O(k).
      Una máquina que termina con n/m trabajos acumula 1 + 2 + ... + n/m = O((n/m)^2).
      Para m máquinas, el costo asciende a O(n^2 / m) cuando dominan las copias.
  - Versión optimizada:
      El min-heap almacena únicamente pares livianos (carga, id_maquina). Las asignaciones
      se realizan mediante append O(1) en listas externas dedicadas.
      Costo total garantizado: O(n log m).
"""

import csv
import heapq
import os
from random import Random
from statistics import median
from time import perf_counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

SEMILLA_GLOBAL = 2026


def list_scheduling(trabajos, m):
    """Versión optimizada: heap almacena sólo (carga, id), listas externas con append O(1)."""
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")
    planificacion = [[] for _ in range(m)]
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)
    for trabajo in trabajos:
        carga, maquina = heap[0]
        planificacion[maquina].append(trabajo)
        heapq.heapreplace(heap, (carga + trabajo, maquina))
    return planificacion, max(carga for carga, _ in heap)


def list_scheduling_guia(trabajos, m):
    """Transcripción literal del Listing 2 de la guía (copia listas en cada inserción)."""
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")
    heap = [(0, i, []) for i in range(m)]
    heapq.heapify(heap)
    for trabajo in trabajos:
        carga, maquina, asignados = heapq.heappop(heap)
        nuevos = asignados + [trabajo]          # <- copia O(len(asignados))
        heapq.heappush(heap, (carga + trabajo, maquina, nuevos))
    resultado = sorted(heap, key=lambda x: x[1])
    planificacion = [asignados for _, _, asignados in resultado]
    return planificacion, max(carga for carga, _, _ in resultado)


def medir_mediana(funcion, *argumentos, repeticiones=3):
    inicio = perf_counter()
    resultado = funcion(*argumentos)
    unica = perf_counter() - inicio
    lazos = 1 if unica >= 2e-3 else min(1000, max(1, int(2e-3 / max(unica, 1e-7))))

    tiempos = []
    for _ in range(repeticiones):
        inicio = perf_counter()
        for _ in range(lazos):
            resultado = funcion(*argumentos)
        tiempos.append((perf_counter() - inicio) / lazos)
    return resultado, median(tiempos)


def formato_tiempo(segundos):
    if segundos < 1e-3:
        return "%.1f us" % (segundos * 1e6)
    if segundos < 1.0:
        return "%.2f ms" % (segundos * 1e3)
    return "%.3f s" % segundos


def mostrar_tabla(encabezados, filas, titulo=None):
    if titulo:
        print("\n" + "=" * 75)
        print(titulo)
        print("=" * 75)
    anchos = [max(len(str(encabezados[i])),
                  max((len(str(f[i])) for f in filas), default=0)) + 2
              for i in range(len(encabezados))]
    print("".join(str(encabezados[i]).ljust(anchos[i]) for i in range(len(encabezados))))
    print("-" * sum(anchos))
    for fila in filas:
        print("".join(str(fila[i]).ljust(anchos[i]) for i in range(len(fila))))


def guardar_csv(nombre_archivo, encabezados, filas):
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(encabezados)
        escritor.writerows(filas)
    print("\nCSV guardado en:", ruta)


def main():
    print("=" * 75)
    print("COMPLEJIDAD DE LIST SCHEDULING: GUÍA (O(n^2/m)) vs OPTIMIZADA (O(n log m))")
    print("=" * 75)

    # ---- 1. Verificación de equivalencia funcional ----
    print("\n1. Verificando equivalencia funcional en 500 instancias aleatorias...")
    generador = Random(SEMILLA_GLOBAL + 5)
    iguales = 0
    for _ in range(500):
        m = generador.randint(1, 8)
        t = [generador.randint(1, 50) for _ in range(generador.randint(0, 40))]
        if list_scheduling(t, m) == list_scheduling_guia(t, m):
            iguales += 1
    print("-> Salidas idénticas en %d de 500 instancias aleatorias." % iguales)
    assert iguales == 500, "Error: Las versiones difieren en sus resultados"

    # ---- 2. Medición empírica de escalabilidad (m = 4) ----
    print("\n2. Evaluando crecimiento de tiempo al cuadruplicar n (m = 4)...")
    TAMANOS_LS = [1_000, 4_000, 16_000, 64_000]
    filas_ls = []
    previo = None

    for n in TAMANOS_LS:
        t = [Random(SEMILLA_GLOBAL + n).randint(1, 100) for _ in range(n)]
        _, t_opt = medir_mediana(list_scheduling, t, 4, repeticiones=3)
        _, t_guia = medir_mediana(list_scheduling_guia, t, 4, repeticiones=3)
        factor = "" if previo is None else "x%.1f / x%.1f" % (t_opt / previo[0], t_guia / previo[1])
        filas_ls.append([n, formato_tiempo(t_opt), formato_tiempo(t_guia),
                         "%.1f" % (t_guia / t_opt), factor])
        previo = (t_opt, t_guia)

    mostrar_tabla(["n", "t optimizada", "t guia", "guia / optimizada",
                   "crecimiento opt. / guia"], filas_ls,
                  "Comparación con m = 4 (mediana de 3 repeticiones)")

    print("\nConclusión teórica y empírica:")
    print("  - Al multiplicar n por 4, la versión optimizada crece ~x4 (comportamiento lineal O(n log m)).")
    print("  - La versión de la guía se acerca a un factor ~x16 (comportamiento cuadrático O(n^2/m))")
    print("    debido al costo acumulado de copiar listas en el heap.")

    guardar_csv("complejidad_list_scheduling.csv",
                ["n", "tiempo_optimizada", "tiempo_guia", "razon", "crecimiento"], filas_ls)


if __name__ == "__main__":
    main()
