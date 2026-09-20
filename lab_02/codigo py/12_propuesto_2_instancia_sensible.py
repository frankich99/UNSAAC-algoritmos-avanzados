# -*- coding: utf-8 -*-
"""
Propuesto 2: Instancia Sensible donde el Orden Afecta Visiblemente a List Scheduling
Problema: Pm || Cmax

Fundamento teórico:
  - Para CUALQUIER orden de llegada, List Scheduling cumple (Graham, 1966):
        C_LS <= sum(p_j)/m + (1 - 1/m) * p_max <= LB + p_max
    debido a que el trabajo que finaliza último inició cuando su máquina era la de menor carga (<= promedio).
  - Por lo tanto:
        C_LS / LB <= 1 + p_max / LB
  - Con pocos trabajos por máquina (n/m pequeño), p_max es comparable con LB y el orden influye enormemente.
  - Con muchos trabajos por máquina (n/m grande), p_max / LB -> 0 y todos los órdenes convergen asintóticamente.

Experimento:
  - n = 100 trabajos, m = 4, 16, 64.
  - 1000 permutaciones aleatorias + orden ascendente + orden original + LPT.
  - Guarda: 'resultados/propuesto2_orden_visible.csv'
"""

import csv
import heapq
import os
from collections import Counter
from random import Random
from statistics import median

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

SEMILLA_GLOBAL = 2026
PERMUTACIONES_ENFOCADAS = 1000
N_ENFOCADO = 100
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


def generar_trabajos_grande(n, semilla):
    gen = Random(semilla)
    return [gen.randint(1, 100) for _ in range(n)]


def mostrar_tabla(encabezados, filas, titulo=None):
    if titulo:
        print("\n" + "=" * 85)
        print(titulo)
        print("=" * 85)
    anchos = [max(len(str(encabezados[i])),
                  max((len(str(f[i])) for f in filas), default=0)) + 2
              for i in range(len(encabezados))]
    print("".join(str(encabezados[i]).ljust(anchos[i]) for i in range(len(encabezados))))
    print("-" * sum(anchos))
    for fila in filas:
        print("".join(str(fila[i]).ljust(anchos[i]) for i in range(len(fila))))


def main():
    print("=" * 85)
    print("PROPUESTO 2: INSTANCIA SENSIBLE Y DEMOSTRACIÓN DE LA COTA DE GRAHAM (n = 100)")
    print("=" * 85)

    semilla_t = SEMILLA_GLOBAL * 1000 + 500
    t_enfocado = generar_trabajos_grande(N_ENFOCADO, semilla_t)
    generador = Random(SEMILLA_GLOBAL + 12)

    enfoque = {}
    filas_enfoque = []

    print("Evaluando 1000 órdenes aleatorios para m = 4, 16, 64...")

    for m in M_P2:
        lb = cota_inferior(t_enfocado, m)
        valores = []
        for _ in range(PERMUTACIONES_ENFOCADAS):
            orden = list(t_enfocado)
            generador.shuffle(orden)
            valores.append(list_scheduling(orden, m)[1])

        c_original = list_scheduling(t_enfocado, m)[1]
        c_lpt = lpt(t_enfocado, m)[1]
        c_asc = list_scheduling(sorted(t_enfocado), m)[1]
        cota_graham = lb + max(t_enfocado)

        enfoque[m] = {
            "lb": lb, "valores": valores, "original": c_original,
            "lpt": c_lpt, "ascendente": c_asc
        }

        # Verificación rigurosa de la cota de Graham
        assert max(valores) <= cota_graham, "Violación detectada de la cota de Graham: C_LS > LB + p_max"

        filas_enfoque.append([
            m, lb, c_lpt, c_original, c_asc, min(valores),
            median(valores), max(valores),
            "%.1f" % (100.0 * (max(valores) - min(valores)) / lb),
            "%d (%.1f)" % (cota_graham, cota_graham / lb),
            "%.1f %%" % (100.0 * sum(v > c_lpt for v in valores) / len(valores))
        ])

    mostrar_tabla(
        ["m", "LB", "C_LPT", "C_orig", "C_asc", "perm_min", "perm_med",
         "perm_max", "rango % LB", "cota LB+pmax", "ordenes > LPT %"],
        filas_enfoque,
        "Análisis de Sensibilidad al Orden con n = 100 trabajos (1 000 permutaciones)")

    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto2_orden_visible.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["m", "LB", "C_LPT", "C_original", "C_ascendente", "perm_min", "perm_mediana",
                    "perm_max", "rango_pct_LB", "cota_LB_mas_pmax", "pct_ordenes_peores_que_LPT"])
        w.writerows(filas_enfoque)
    print("\nResultados guardados en:", ruta_csv)

    print("\nCertificación de optimalidad en la instancia:")
    for m in M_P2:
        if enfoque[m]["lpt"] == enfoque[m]["lb"]:
            print("  m = %d: LPT alcanza la cota LB = %d -> es ÓPTIMO certificado." % (m, enfoque[m]["lb"]))
        else:
            print("  m = %d: LPT = %d > LB = %d -> el óptimo se ubica en [%d, %d]."
                  % (m, enfoque[m]["lpt"], enfoque[m]["lb"], enfoque[m]["lb"], enfoque[m]["lpt"]))


if __name__ == "__main__":
    main()
