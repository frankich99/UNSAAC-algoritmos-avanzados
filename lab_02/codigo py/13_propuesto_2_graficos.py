# -*- coding: utf-8 -*-
"""
Propuesto 2: Gráficos de Distribución, Escala y Tiempos de Ejecución
Problema: Pm || Cmax

Genera las 3 figuras del Propuesto 2:
  1. 'figuras/p2_distribucion_orden.png' : Distribución del makespan según el orden (n = 100).
  2. 'figuras/p2_efecto_orden_escala.png' : Desvanecimiento del efecto del orden al crecer n/m.
  3. 'figuras/p2_tiempos.png'             : Tiempos de ejecución de LS, LPT y ordenamiento.
"""

import csv
import heapq
import os
from collections import Counter
from random import Random

import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
CARPETA_FIGURAS = os.path.join(BASE_DIR, "figuras")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

SEMILLA_GLOBAL = 2026
N_P2 = (100, 1_000, 10_000, 100_000)
M_P2 = (4, 16, 64)
PERMUTACIONES = 30
N_ENFOCADO = 100

COLOR = {"LS": "#2a78d6", "LPT": "#eb6834", "BB": "#1baf7a"}
MARCADOR = {"LS": "o", "LPT": "s", "BB": "^"}
AZUL_M = {4: "#86b6ef", 16: "#2a78d6", 64: "#104281"}
MARCA_M = {4: "o", 16: "s", 64: "D"}
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


def generar_trabajos_grande(n, semilla):
    gen = Random(semilla)
    return [gen.randint(1, 100) for _ in range(n)]


def cargar_o_generar_p2():
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto2_escalabilidad.csv")
    if not os.path.exists(ruta_csv):
        import subprocess
        import sys
        script_11 = os.path.join(BASE_DIR, "11_propuesto_2_escalabilidad.py")
        print("Ejecutando propuesto 2 previo para obtener datos...")
        subprocess.run([sys.executable, script_11], check=True)

    filas_p2 = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for r in lector:
            filas_p2.append({
                "n": int(r["n"]), "m": int(r["m"]), "LB": int(r["LB"]),
                "C_original": int(r["C_original"]), "C_LPT": int(r["C_LPT"]),
                "C_perm_min": int(r["C_perm_min"]), "C_perm_mediana": float(r["C_perm_mediana"]),
                "C_perm_max": int(r["C_perm_max"]),
                "q_original": float(r["q_original"]), "q_LPT": float(r["q_LPT"]),
                "q_perm_min": float(r["q_perm_min"]), "q_perm_mediana": float(r["q_perm_mediana"]),
                "q_perm_max": float(r["q_perm_max"]),
                "t_LS": float(r["t_LS"]), "t_LPT": float(r["t_LPT"]), "t_orden": float(r["t_orden"]),
            })
    return filas_p2


def main():
    print("=" * 70)
    print("PROPUESTO 2: GENERACIÓN DE GRÁFICOS (DISTRIBUCIÓN, ESCALA Y TIEMPOS)")
    print("=" * 70)

    filas_p2 = cargar_o_generar_p2()

    # Reconstruir trabajos para cota de Graham
    conjuntos_p2 = []
    for n in N_P2:
        semilla = SEMILLA_GLOBAL * 1000 + 500 + len(conjuntos_p2)
        conjuntos_p2.append({"id": "P2-n%d" % n, "n": n, "semilla": semilla,
                             "trabajos": generar_trabajos_grande(n, semilla)})

    # ---- Gráfico 1: Distribución del makespan (n = 100) ----
    print("\n1. Generando Gráfico 1: p2_distribucion_orden.png...")
    t_enfocado = conjuntos_p2[0]["trabajos"]
    generador = Random(SEMILLA_GLOBAL + 12)
    enfoque = {}

    for m in M_P2:
        lb = cota_inferior(t_enfocado, m)
        valores = []
        for _ in range(1000):
            orden = list(t_enfocado)
            generador.shuffle(orden)
            valores.append(list_scheduling(orden, m)[1])
        c_orig = list_scheduling(t_enfocado, m)[1]
        c_lpt = lpt(t_enfocado, m)[1]
        enfoque[m] = {"lb": lb, "valores": valores, "original": c_orig, "lpt": c_lpt}

    figura1, ejes1 = plt.subplots(1, 3, figsize=(11.5, 4.1))
    for eje, m in zip(ejes1, M_P2):
        e = enfoque[m]
        valores = e["valores"]
        bordes = range(min(valores), max(valores) + 2)
        eje.hist(valores, bins=bordes, color=COLOR["LS"], alpha=0.85, edgecolor="white",
                 linewidth=0.6, label="LS, %d órdenes aleatorios" % len(valores))
        eje.axvline(e["lb"], color=TINTA_TENUE, linestyle=(0, (3, 2)), linewidth=1.3,
                    label="cota inferior LB")
        eje.axvline(e["lpt"], color=COLOR["LPT"], linewidth=2.2, label="LPT")
        eje.axvline(e["original"], color=TINTA, linewidth=1.3, linestyle=(0, (1, 1.5)),
                    label="LS, orden original")

        altura = max(Counter(valores).values())
        eje.set_ylim(0, altura * 1.32)
        fondo = dict(boxstyle="square,pad=0.15", facecolor="white", edgecolor="none")
        texto_lpt = "LPT = LB = %d" % e["lpt"] if e["lpt"] == e["lb"] else "LPT = %d" % e["lpt"]
        eje.annotate(texto_lpt, (e["lpt"], altura * 1.27), xytext=(4, 0), textcoords="offset points",
                     ha="left", va="center", fontsize=8, color=TINTA_SECUNDARIA, bbox=fondo)
        eje.annotate("original = %d" % e["original"], (e["original"], altura * 1.12),
                     xytext=(4, 0), textcoords="offset points", ha="left", va="center",
                     fontsize=8, color=TINTA_SECUNDARIA, bbox=fondo)
        eje.set_title("m = %d   (n/m = %.1f)" % (m, N_ENFOCADO / m), loc="left")
        eje.set_xlabel("makespan")
        eje.grid(axis="x", visible=False)
        ancho = max(valores) - e["lb"]
        eje.set_xlim(e["lb"] - 0.06 * ancho, max(valores) + 0.04 * ancho)

    ejes1[0].set_ylabel("número de órdenes")
    manejadores, etiquetas = ejes1[1].get_legend_handles_labels()
    figura1.legend(manejadores, etiquetas, loc="lower center", ncol=4)
    figura1.suptitle("n = %d trabajos: el mismo conjunto, distinto orden, distinto makespan"
                     % N_ENFOCADO, x=0.01, ha="left", fontsize=10, color=TINTA_SECUNDARIA)
    figura1.tight_layout(rect=(0, 0.07, 1, 1))

    ruta_fig1 = os.path.join(CARPETA_FIGURAS, "p2_distribucion_orden.png")
    figura1.savefig(ruta_fig1, bbox_inches="tight")
    plt.close(figura1)
    print("  -> Guardado:", ruta_fig1)

    # ---- Gráfico 2: Efecto del orden al crecer n/m ----
    print("\n2. Generando Gráfico 2: p2_efecto_orden_escala.png...")
    figura2, eje2 = plt.subplots(figsize=(8.6, 4.8))
    for m in M_P2:
        g = [f for f in filas_p2 if f["m"] == m]
        ns = [f["n"] for f in g]
        minimo = [100.0 * (f["q_perm_min"] - 1) for f in g]
        maximo = [100.0 * (f["q_perm_max"] - 1) for f in g]
        mediana = [100.0 * (f["q_perm_mediana"] - 1) for f in g]
        cota = [100.0 * max(c["trabajos"]) / f["LB"] for c, f in zip(conjuntos_p2, g)]

        eje2.fill_between(ns, minimo, maximo, color=AZUL_M[m], alpha=0.15, linewidth=0)
        eje2.plot(ns, mediana, color=AZUL_M[m], marker=MARCA_M[m], markersize=6,
                  label="m = %d: mediana de %d órdenes (banda: mín.–máx.)" % (m, PERMUTACIONES))
        eje2.plot(ns, cota, color=AZUL_M[m], linestyle=(0, (3, 2)), linewidth=1.2)

    eje2.plot([], [], color=TINTA_TENUE, linestyle=(0, (3, 2)), linewidth=1.2,
              label="cota de Graham para cualquier orden: p_max / LB")
    eje2.set_xscale("log")
    eje2.set_yscale("log")
    eje2.set_xlabel("n (número de trabajos, escala log)")
    eje2.set_ylabel("exceso sobre LB  100·(C − LB)/LB  [%]")
    eje2.set_title("List Scheduling: el efecto del orden se desvanece cuando crece n/m", loc="left")
    lpt_en_lb = sum(f["C_LPT"] == f["LB"] for f in filas_p2)
    eje2.annotate("LPT: exceso 0 %% (C = LB) en %d de %d casos,\n"
                  "no representable en escala log" % (lpt_en_lb, len(filas_p2)),
                  (0.99, 0.97), xycoords="axes fraction", ha="right", va="top", fontsize=8.5,
                  color=TINTA_SECUNDARIA)
    eje2.legend(loc="lower left", fontsize=8.5)

    ruta_fig2 = os.path.join(CARPETA_FIGURAS, "p2_efecto_orden_escala.png")
    figura2.savefig(ruta_fig2, bbox_inches="tight")
    plt.close(figura2)
    print("  -> Guardado:", ruta_fig2)

    # ---- Gráfico 3: Tiempos de ejecución ----
    print("\n3. Generando Gráfico 3: p2_tiempos.png...")
    figura3, ejes3 = plt.subplots(1, 3, figsize=(11.5, 3.9), sharey=True)
    for eje, m in zip(ejes3, M_P2):
        g = [f for f in filas_p2 if f["m"] == m]
        ns = [f["n"] for f in g]
        eje.plot(ns, [f["t_LS"] for f in g], color=COLOR["LS"], marker=MARCADOR["LS"],
                 label="List Scheduling")
        eje.plot(ns, [f["t_LPT"] for f in g], color=COLOR["LPT"], marker=MARCADOR["LPT"],
                 label="LPT (ordenar + LS)")
        eje.plot(ns, [f["t_orden"] for f in g], color=TINTA_TENUE, marker="^",
                 linestyle=(0, (3, 2)), linewidth=1.4, label="solo ordenar")
        eje.set_xscale("log")
        eje.set_yscale("log")
        eje.set_title("m = %d" % m, loc="left")
        eje.set_xlabel("n (escala log)")

    ejes3[0].set_ylabel("tiempo mediano (s, escala log)")
    ejes3[0].legend(loc="upper left")
    figura3.suptitle("Tiempo de ejecución: ambos crecen casi linealmente; LPT paga además el "
                     "ordenamiento O(n log n)", x=0.01, ha="left", fontsize=10,
                     color=TINTA_SECUNDARIA)
    figura3.tight_layout()

    ruta_fig3 = os.path.join(CARPETA_FIGURAS, "p2_tiempos.png")
    figura3.savefig(ruta_fig3, bbox_inches="tight")
    plt.close(figura3)
    print("  -> Guardado:", ruta_fig3)


if __name__ == "__main__":
    main()
