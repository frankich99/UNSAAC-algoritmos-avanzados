# -*- coding: utf-8 -*-
"""
Propuesto 1: Rendimiento y Límite Práctico del Método Exacto (Branch and Bound)
Problema: Pm || Cmax

Metodología:
  - Familia "estrecha" (duraciones homogéneas U[10, 20]) con m = 4 máquinas.
  - Evalúa n = 10, 11, ..., 24 con 6 instancias por valor de n.
  - Tope de seguridad: 1 000 000 de nodos (manejo de LimiteNodosExcedido).
  - Registra: número de nodos explorados, tiempo mediano, casos certificados en la raíz.
  - Genera:
      * CSV: 'resultados/propuesto1_escala_exacto.csv'
      * Figura de 2 paneles: 'figuras/p1_rendimiento_exacto.png'
"""

import csv
import heapq
import os
from collections import Counter
from random import Random
from statistics import median
from time import perf_counter

import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
CARPETA_FIGURAS = os.path.join(BASE_DIR, "figuras")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

SEMILLA_GLOBAL = 2026
LIMITE_NODOS_ESCALA = 1_000_000
M_ESCALA = 4
N_ESCALA = list(range(10, 25))
INSTANCIAS_ESCALA = 6

COLOR = {"LS": "#2a78d6", "LPT": "#eb6834", "BB": "#1baf7a"}
MARCADOR = {"LS": "o", "LPT": "s", "BB": "^"}
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_TENUE = "#898781"
CUADRICULA = "#e1e0d9"
EJE = "#c3c2b7"

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 150,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": EJE,
    "axes.linewidth": 0.8,
    "axes.labelcolor": TINTA_SECUNDARIA,
    "axes.titlecolor": TINTA,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": CUADRICULA,
    "grid.linewidth": 0.8,
    "grid.linestyle": "-",
    "xtick.color": TINTA_TENUE,
    "ytick.color": TINTA_TENUE,
    "xtick.labelcolor": TINTA_SECUNDARIA,
    "ytick.labelcolor": TINTA_SECUNDARIA,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "lines.linewidth": 2,
    "lines.markersize": 6,
    "font.size": 10,
})


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


class LimiteNodosExcedido(Exception):
    def __init__(self, nodos):
        super().__init__("Limite de nodos excedido (%d nodos)" % nodos)
        self.nodos = nodos


def branch_and_bound(trabajos, m, limite_nodos=None):
    trabajos = sorted(trabajos, reverse=True)
    n = len(trabajos)
    mejor_plan, mejor_valor = lpt(trabajos, m)
    cargas_actuales = [0] * m
    plan_actual = [[] for _ in range(m)]
    nodos = 0
    cota_promedio = -(-sum(trabajos) // m)

    def buscar(k):
        nonlocal mejor_plan, mejor_valor, nodos
        nodos += 1
        if limite_nodos is not None and nodos > limite_nodos:
            raise LimiteNodosExcedido(nodos)

        if k == n:
            valor = max(cargas_actuales, default=0)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_plan = [x.copy() for x in plan_actual]
            return

        trabajo = trabajos[k]
        cargas_probadas = set()

        for i in range(m):
            if cargas_actuales[i] in cargas_probadas:
                continue
            cargas_probadas.add(cargas_actuales[i])

            nueva_carga = cargas_actuales[i] + trabajo
            if nueva_carga >= mejor_valor:
                continue

            cargas_actuales[i] = nueva_carga
            plan_actual[i].append(trabajo)

            restante_mas_largo = trabajos[k + 1] if k + 1 < n else 0
            lb = max(max(cargas_actuales), cota_promedio, restante_mas_largo)
            if lb < mejor_valor:
                buscar(k + 1)

            plan_actual[i].pop()
            cargas_actuales[i] -= trabajo

            if nueva_carga == trabajo:
                break

    if mejor_valor == cota_inferior(trabajos, m):
        return mejor_plan, mejor_valor, nodos

    buscar(0)
    return mejor_plan, mejor_valor, nodos


def formato_tiempo(segundos):
    if segundos is None:
        return "abortado"
    if segundos < 1e-3:
        return "%.1f us" % (segundos * 1e6)
    if segundos < 1.0:
        return "%.2f ms" % (segundos * 1e3)
    return "%.3f s" % segundos


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
    print("PROPUESTO 1: RENDIMIENTO Y LÍMITE PRÁCTICO DEL MÉTODO EXACTO")
    print("=" * 80)

    filas_escala = []
    print("Ejecutando batería de experimentos con Branch & Bound (n = 10..24, m = 4)...")

    for n in N_ESCALA:
        for rep in range(INSTANCIAS_ESCALA):
            semilla = SEMILLA_GLOBAL * 1000 + 900 + 10 * n + rep
            gen = Random(semilla)
            t = [gen.randint(10, 20) for _ in range(n)]

            inicio = perf_counter()
            try:
                plan, opt, nodos = branch_and_bound(t, M_ESCALA, LIMITE_NODOS_ESCALA)
                estado = "ok"
                assert verificar_solucion(t, M_ESCALA, plan, opt)
            except LimiteNodosExcedido as error:
                opt, nodos, estado = None, error.nodos, "abortada"
            duracion = perf_counter() - inicio

            filas_escala.append([M_ESCALA, n, rep, semilla, cota_inferior(t, M_ESCALA), opt,
                                 lpt(t, M_ESCALA)[1], nodos, duracion, estado])

    # Guardar CSV
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto1_escala_exacto.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["m", "n", "rep", "semilla", "LB", "OPT", "C_LPT", "nodos", "tiempo_s", "estado"])
        writer.writerows(filas_escala)
    print("\nCSV guardado en:", ruta_csv)

    # Resumen por n
    resumen_escala = []
    for n in N_ESCALA:
        g = [f for f in filas_escala if f[1] == n]
        nodos = sorted(f[7] for f in g)
        centro = nodos[(len(nodos) - 1) // 2: len(nodos) // 2 + 1]
        prefijo = ">= " if any(v > LIMITE_NODOS_ESCALA for v in centro) else ""
        maximo = nodos[-1]
        resumen_escala.append([n, sum(v == 0 for v in nodos), prefijo + "%g" % median(nodos),
                               "tope" if maximo > LIMITE_NODOS_ESCALA else maximo,
                               formato_tiempo(max(float(f[8]) for f in g)),
                               sum(f[9] == "abortada" for f in g)])

    mostrar_tabla(["n", "certificadas_raiz", "nodos_mediana", "nodos_max", "t_max", "abortadas"],
                  resumen_escala,
                  "Comportamiento de Branch and Bound según tamaño n (m = 4)")

    con_trabajo = [f for f in filas_escala if f[7] >= 1000 and f[9] == "ok"]
    us_por_nodo = median(1e6 * float(f[8]) / f[7] for f in con_trabajo) if con_trabajo else 0.0
    print("\nCosto mediano por nodo explorado (instancias con >= 1000 nodos): %.2f us" % us_por_nodo)

    # ---- Generación del Gráfico de 2 Paneles ----
    print("\nGenerando figura de rendimiento exacto...")
    figura, (eje_n, eje_t) = plt.subplots(1, 2, figsize=(10.5, 4.3),
                                          gridspec_kw={"width_ratios": [1.45, 1]})
    jitter = Random(SEMILLA_GLOBAL + 10)
    resueltas = [f for f in filas_escala if f[9] == "ok"]
    abortadas = [f for f in filas_escala if f[9] == "abortada"]

    # Panel 1: Nodos (+1 para escala logarítmica)
    eje_n.scatter([f[1] + jitter.uniform(-0.18, 0.18) for f in resueltas],
                  [f[7] + 1 for f in resueltas], s=22, color=COLOR["BB"], marker=MARCADOR["BB"],
                  alpha=0.7, edgecolors="white", linewidths=0.6, zorder=3, label="cada instancia")
    if abortadas:
        eje_n.scatter([f[1] for f in abortadas], [LIMITE_NODOS_ESCALA + 1] * len(abortadas),
                      s=40, color=TINTA, marker="x", zorder=4, label="abortada por tope")
    eje_n.plot(N_ESCALA, [max(f[7] for f in filas_escala if f[1] == n) + 1 for n in N_ESCALA],
               color=TINTA, linewidth=1.6, zorder=2, label="peor caso de cada n")
    eje_n.axhline(LIMITE_NODOS_ESCALA, color=TINTA_TENUE, linestyle=(0, (3, 2)), linewidth=1.2)
    eje_n.annotate("tope: 1 000 000 nodos", (N_ESCALA[0], LIMITE_NODOS_ESCALA),
                   xytext=(0, 5), textcoords="offset points", fontsize=8, color=TINTA_SECUNDARIA)
    eje_n.set_yscale("log")
    eje_n.set_ylim(0.6, 1e7)
    eje_n.set_xticks(N_ESCALA[::2])
    eje_n.set_xlabel("n (número de trabajos)")
    eje_n.set_ylabel("nodos explorados + 1 (escala log)")
    eje_n.set_title("Nodos explorados, m = %d, familia estrecha" % M_ESCALA, loc="left")
    eje_n.legend(loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3)

    # Panel 2: Tiempo frente a nodos
    xs = [f[7] for f in resueltas if f[7] > 0]
    ys = [float(f[8]) for f in resueltas if f[7] > 0]
    if xs:
        eje_t.scatter(xs, ys, s=22, color=COLOR["BB"], marker=MARCADOR["BB"], alpha=0.7,
                      edgecolors="white", linewidths=0.6, zorder=3)
        referencia = [min(xs), max(xs)]
        eje_t.plot(referencia, [x * us_por_nodo * 1e-6 for x in referencia], color=TINTA,
                   linewidth=1.2, zorder=2, label="%.1f µs/nodo" % us_por_nodo)
    eje_t.set_xscale("log")
    eje_t.set_yscale("log")
    eje_t.set_xlabel("nodos explorados (escala log)")
    eje_t.set_ylabel("tiempo (s, escala log)")
    eje_t.set_title("Tiempo frente a nodos", loc="left")
    eje_t.legend(loc="upper left")
    figura.tight_layout()

    ruta_fig = os.path.join(CARPETA_FIGURAS, "p1_rendimiento_exacto.png")
    figura.savefig(ruta_fig, bbox_inches="tight")
    print("Figura guardada en:", ruta_fig)
    plt.close(figura)


if __name__ == "__main__":
    main()
