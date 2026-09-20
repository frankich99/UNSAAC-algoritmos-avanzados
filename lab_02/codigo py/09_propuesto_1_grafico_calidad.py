# -*- coding: utf-8 -*-
"""
Propuesto 1: Gráfico de Calidad Observada Frente a la Garantía Teórica
Problema: Pm || Cmax

Genera la figura:
  - 'figuras/p1_calidad_razones.png'
  - Diagrama de dispersión con jitter horizontal para r(I) = ALG / OPT.
  - Mediana observada marcada con segmento negro grueso.
  - Garantía teórica punteada con etiqueta directa para cada algoritmo y valor de m.
  - Instancias ajustadas teóricas representadas como marcadores huecos en el límite exacto.
"""

import csv
import os
from random import Random
from statistics import median

import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
CARPETA_FIGURAS = os.path.join(BASE_DIR, "figuras")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

SEMILLA_GLOBAL = 2026
M_P1 = (2, 3, 4)

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


def garantia_ls(m):
    return 2.0 - 1.0 / m


def garantia_lpt(m):
    return 4.0 / 3.0 - 1.0 / (3.0 * m)


def cargar_datos():
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto1_calidad.csv")
    if not os.path.exists(ruta_csv):
        import subprocess
        import sys
        script_07 = os.path.join(BASE_DIR, "07_propuesto_1_calidad.py")
        print("Generando datos previos para el gráfico...")
        subprocess.run([sys.executable, script_07], check=True)

    filas = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for r in lector:
            filas.append({
                "id": r["id"], "familia": r["familia"],
                "n": int(r["n"]), "m": int(r["m"]),
                "r_LS": float(r["r_LS"]), "r_LPT": float(r["r_LPT"])
            })
    return filas


def main():
    print("=" * 70)
    print("PROPUESTO 1: GENERACIÓN DEL GRÁFICO DE CALIDAD OBSERVADA")
    print("=" * 70)

    filas = cargar_datos()
    aleatorias = [f for f in filas if not f["familia"].startswith("ajustada")]
    ajustadas = [f for f in filas if f["familia"].startswith("ajustada")]

    figura, eje = plt.subplots(figsize=(8.6, 5.2))
    jitter = Random(SEMILLA_GLOBAL)
    desplazamiento = {"LS": -0.18, "LPT": 0.18}

    for alg in ("LS", "LPT"):
        for m in M_P1:
            x0 = m + desplazamiento[alg]
            grupo = [f["r_" + alg] for f in aleatorias if f["m"] == m]
            xs = [x0 + jitter.uniform(-0.06, 0.06) for _ in grupo]
            eje.scatter(xs, grupo, s=26, color=COLOR[alg], marker=MARCADOR[alg], alpha=0.75,
                        edgecolors="white", linewidths=0.8, zorder=3,
                        label=("List Scheduling" if alg == "LS" else "LPT") if m == M_P1[0] else None)
            eje.plot([x0 - 0.1, x0 + 0.1], [median(grupo)] * 2, color=TINTA, linewidth=2, zorder=4)

            gar = garantia_ls(m) if alg == "LS" else garantia_lpt(m)
            eje.plot([x0 - 0.13, x0 + 0.13], [gar, gar], color=COLOR[alg], linestyle=(0, (3, 2)),
                     linewidth=1.5, zorder=2)
            eje.annotate("%.3f" % gar, (x0, gar), xytext=(0, 8), textcoords="offset points",
                         ha="center", va="bottom", fontsize=8, color=TINTA_SECUNDARIA)

            for f in ajustadas:
                if f["m"] == m and f["familia"] == ("ajustada_ls" if alg == "LS" else "ajustada_lpt"):
                    eje.scatter([x0], [f["r_" + alg]], s=70, facecolors="white",
                                edgecolors=COLOR[alg], marker=MARCADOR[alg], linewidths=1.8, zorder=5,
                                label="Instancia ajustada" if (m == M_P1[0] and alg == "LS") else None)

    eje.plot([], [], color=TINTA, linewidth=2, label="Mediana")
    eje.plot([], [], color=TINTA_TENUE, linestyle=(0, (3, 2)), linewidth=1.5, label="Garantía teórica")
    eje.set_xticks(list(M_P1))
    eje.set_xticklabels(["m = %d" % m for m in M_P1])
    eje.set_xlim(1.5, 4.5)
    eje.set_ylim(0.97, 1.86)
    eje.grid(axis="x", visible=False)
    eje.set_ylabel("razón observada  r(I) = ALG / OPT")
    eje.set_title("Calidad observada frente a la garantía teórica (%d instancias aleatorias)"
                  % len(aleatorias), loc="left")
    eje.legend(loc="upper left", ncol=3)

    ruta_salida = os.path.join(CARPETA_FIGURAS, "p1_calidad_razones.png")
    figura.savefig(ruta_salida, bbox_inches="tight")
    print("\nFigura generada exitosamente en:", ruta_salida)
    plt.close(figura)


if __name__ == "__main__":
    main()
