# -*- coding: utf-8 -*-
"""
Propuesto 2: Efecto del Orden y Escalabilidad en Grandes Instancias
Problema: Pm || Cmax

Metodología:
  - Conjuntos de trabajos con n = 100, 1 000, 10 000, 100 000 y m = 4, 16, 64.
  - 30 permutaciones aleatorias reproducibles por cada tamaño n.
  - Compara:
      * List Scheduling con orden original.
      * List Scheduling sobre las 30 permutaciones (mínimo, mediana, máximo).
      * LPT (ordenamiento descendente + List Scheduling).
      * Medición aislada del costo de ordenar (sorted).
  - Guarda:
      * 'resultados/propuesto2_escalabilidad.csv'
      * 'resultados/propuesto2_makespans_permutaciones.csv'
"""

import csv
import heapq
import os
from collections import Counter
from random import Random
from statistics import median
from time import perf_counter

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

SEMILLA_GLOBAL = 2026
REPETICIONES_P2 = 5
PERMUTACIONES = 30
N_P2 = (100, 1_000, 10_000, 100_000)
M_P2 = (4, 16, 64)


def cota_inferior(trabajos, m):
    if not trabajos:
        return 0
    return max(-(-sum(trabajos) // m), max(trabajos))


def list_scheduling(trabajos, m):
    planificacion = [[] for _ in range(m)]
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)
    for trabajo in trabajos:
        carga, maquina = heap[0]
        planificacion[maquina].append(trabajo)
        heapq.heapreplace(heap, (carga + trabajo, maquina))
    return planificacion, max(carga for carga, _ in heap)


def lpt(trabajos, m):
    return list_scheduling(sorted(trabajos, reverse=True), m)


def es_factible(trabajos, planificacion, m):
    if len(planificacion) != m:
        return False
    asignados = [p for maquina in planificacion for p in maquina]
    return Counter(asignados) == Counter(trabajos)


def makespan(planificacion):
    return max([sum(m) for m in planificacion], default=0)


def verificar_solucion(trabajos, m, plan, valor):
    return (es_factible(trabajos, plan, m)
            and makespan(plan) == valor
            and valor >= cota_inferior(trabajos, m))


def medir_mediana(funcion, *argumentos, repeticiones=REPETICIONES_P2):
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


def generar_trabajos_grande(n, semilla):
    gen = Random(semilla)
    return [gen.randint(1, 100) for _ in range(n)]


def mostrar_tabla(encabezados, filas, titulo=None):
    if titulo:
        print("\n" + "=" * 80)
        print(titulo)
        print("=" * 80)
    anchos = [max(len(str(encabezados[i])),
                  max((len(str(f[i])) for f in filas), default=0)) + 2
              for i in range(len(encabezados))]
    print("".join(str(encabezados[i]).ljust(anchos[i]) for i in range(len(encabezados))))
    print("-" * sum(anchos))
    for fila in filas:
        print("".join(str(fila[i]).ljust(anchos[i]) for i in range(len(fila))))


def main():
    print("=" * 80)
    print("PROPUESTO 2: EFECTO DEL ORDEN Y ESCALABILIDAD")
    print("=" * 80)

    conjuntos_p2 = []
    for n in N_P2:
        semilla = SEMILLA_GLOBAL * 1000 + 500 + len(conjuntos_p2)
        conjuntos_p2.append({"id": "P2-n%d" % n, "n": n, "semilla": semilla,
                             "trabajos": generar_trabajos_grande(n, semilla)})

    filas_p2 = []
    makespans_perm = {}

    print("Evaluando %d combinaciones de (n, m) con %d permutaciones aleatorias..."
          % (len(N_P2) * len(M_P2), PERMUTACIONES))

    for conjunto in conjuntos_p2:
        t = conjunto["trabajos"]
        n = conjunto["n"]

        # Generar permutaciones una sola vez por n
        generador = Random(conjunto["semilla"] + 1)
        ordenes = []
        for _ in range(PERMUTACIONES):
            orden = list(t)
            generador.shuffle(orden)
            ordenes.append(orden)

        _, t_orden = medir_mediana(sorted, t, repeticiones=REPETICIONES_P2)

        for m in M_P2:
            lb = cota_inferior(t, m)
            (plan_ls, c_ls), t_ls = medir_mediana(list_scheduling, t, m, repeticiones=REPETICIONES_P2)
            (plan_lpt, c_lpt), t_lpt = medir_mediana(lpt, t, m, repeticiones=REPETICIONES_P2)
            assert verificar_solucion(t, m, plan_ls, c_ls)
            assert verificar_solucion(t, m, plan_lpt, c_lpt)

            valores = []
            for orden in ordenes:
                plan, c = list_scheduling(orden, m)
                assert c >= lb and makespan(plan) == c
                valores.append(c)
            makespans_perm[(n, m)] = valores

            filas_p2.append({
                "n": n, "m": m, "LB": lb,
                "C_original": c_ls, "C_LPT": c_lpt,
                "C_perm_min": min(valores), "C_perm_mediana": median(valores),
                "C_perm_max": max(valores),
                "q_original": c_ls / lb, "q_LPT": c_lpt / lb,
                "q_perm_min": min(valores) / lb, "q_perm_mediana": median(valores) / lb,
                "q_perm_max": max(valores) / lb,
                "rango_perm_pct": 100.0 * (max(valores) - min(valores)) / lb,
                "t_LS": t_ls, "t_LPT": t_lpt, "t_orden": t_orden,
                "sobrecosto_LPT_pct": 100.0 * (t_lpt - t_ls) / t_ls,
                "mejora_LPT_pct": 100.0 * (median(valores) - c_lpt) / median(valores),
            })

    # Guardar CSVs
    columnas_p2 = list(filas_p2[0].keys())
    ruta_p2 = os.path.join(CARPETA_RESULTADOS, "propuesto2_escalabilidad.csv")
    with open(ruta_p2, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(columnas_p2)
        for fila in filas_p2:
            w.writerow([("%.9g" % fila[c]) if isinstance(fila[c], float) else fila[c] for c in columnas_p2])

    ruta_perm = os.path.join(CARPETA_RESULTADOS, "propuesto2_makespans_permutaciones.csv")
    with open(ruta_perm, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "m", "permutacion", "makespan"])
        for (n, m), vals in makespans_perm.items():
            for k, v in enumerate(vals):
                w.writerow([n, m, k + 1, v])

    print("\nResultados guardados en:")
    print("  -", ruta_p2)
    print("  -", ruta_perm)

    # Mostrar tabla
    mostrar_tabla(
        ["n", "m", "LB", "C_orig", "C_perm (min-med-max)", "C_LPT",
         "C/LB orig", "C/LB med", "C/LB LPT", "t LS", "t LPT", "t orden"],
        [[f["n"], f["m"], f["LB"], f["C_original"],
          "%d - %g - %d" % (f["C_perm_min"], f["C_perm_mediana"], f["C_perm_max"]), f["C_LPT"],
          "%.4f" % f["q_original"], "%.4f" % f["q_perm_mediana"], "%.4f" % f["q_LPT"],
          formato_tiempo(f["t_LS"]), formato_tiempo(f["t_LPT"]), formato_tiempo(f["t_orden"])]
         for f in filas_p2],
        "Resultados de Escalabilidad y Efecto del Orden (Propuesto 2)")


if __name__ == "__main__":
    main()
