# -*- coding: utf-8 -*-
"""
Propuesto 2: Costo del Ordenamiento Frente a la Mejora del Makespan de LPT
Problema: Pm || Cmax

Pregunta central:
  ¿El costo computacional de ordenar O(n log n) resulta significativo frente a la mejora
  en la calidad del makespan que ofrece LPT respecto a List Scheduling?

Métricas calculadas:
  * sobrecosto de tiempo  = (t_LPT - t_LS) / t_LS %
  * peso del ordenamiento = t_ordenar / t_LPT %
  * mejora del makespan   = (mediana(C_perm) - C_LPT) / mediana(C_perm) %
    (la mejora se mide contra la mediana de órdenes aleatorios, que representa la llegada natural).

Guarda:
  * 'resultados/propuesto2_costo_beneficio.csv'
"""

import csv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)


def formato_tiempo(segundos):
    if segundos < 1e-3:
        return "%.1f us" % (segundos * 1e6)
    if segundos < 1.0:
        return "%.2f ms" % (segundos * 1e3)
    return "%.3f s" % segundos


def cargar_datos_p2():
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto2_escalabilidad.csv")
    if not os.path.exists(ruta_csv):
        import subprocess
        import sys
        script_11 = os.path.join(BASE_DIR, "11_propuesto_2_escalabilidad.py")
        print("Ejecutando propuesto 2 previo para obtener datos de escalabilidad...")
        subprocess.run([sys.executable, script_11], check=True)

    filas = []
    with open(ruta_csv, "r", encoding="utf-8") as f:
        lector = csv.DictReader(f)
        for r in lector:
            filas.append({
                "n": int(r["n"]), "m": int(r["m"]),
                "LB": int(r["LB"]),
                "C_original": int(r["C_original"]), "C_LPT": int(r["C_LPT"]),
                "C_perm_mediana": float(r["C_perm_mediana"]),
                "t_LS": float(r["t_LS"]), "t_LPT": float(r["t_LPT"]), "t_orden": float(r["t_orden"]),
                "sobrecosto_LPT_pct": float(r["sobrecosto_LPT_pct"]),
                "mejora_LPT_pct": float(r["mejora_LPT_pct"]),
            })
    return filas


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
    print("PROPUESTO 2: ANÁLISIS COSTO-BENEFICIO DEL ORDENAMIENTO PREVIO EN LPT")
    print("=" * 85)

    filas_p2 = cargar_datos_p2()
    filas_costo = []

    for f in filas_p2:
        t_extra = f["t_LPT"] - f["t_LS"]
        peso_orden = 100.0 * f["t_orden"] / f["t_LPT"]
        mejora_unid = f["C_perm_mediana"] - f["C_LPT"]
        filas_costo.append([
            f["n"], f["m"], "%.1f" % (f["n"] / f["m"]),
            formato_tiempo(f["t_LS"]), formato_tiempo(f["t_LPT"]),
            formato_tiempo(t_extra),
            "%+.0f %%" % f["sobrecosto_LPT_pct"],
            "%.0f %%" % peso_orden,
            "%g" % mejora_unid,
            "%.3f %%" % f["mejora_LPT_pct"],
        ])

    mostrar_tabla(
        ["n", "m", "n/m", "t LS", "t LPT", "t extra", "sobrecosto",
         "ordenar/t LPT", "mejora unid.", "mejora %"],
        filas_costo,
        "Costo del Ordenamiento frente a la Mejora Obtenida en Makespan")

    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto2_costo_beneficio.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["n", "m", "n_sobre_m", "t_LS", "t_LPT", "t_extra", "sobrecosto_pct",
                    "peso_ordenamiento", "mejora_unidades", "mejora_pct"])
        w.writerows(filas_costo)
    print("\nResultados guardados en:", ruta_csv)

    # Análisis automático de conclusiones
    mas_mejora = max(filas_p2, key=lambda f: f["mejora_LPT_pct"])
    menos_mejora = min(filas_p2, key=lambda f: f["mejora_LPT_pct"])

    print("\n" + "-" * 85)
    print("SÍNTESIS Y CONCLUSIONES PARA EL INFORME:")
    print("-" * 85)
    print("  1. Mayor beneficio de LPT:")
    print("     n = %d, m = %d (n/m = %.1f) -> reduce el makespan en %.2f %% por solo %s extra." % (
        mas_mejora["n"], mas_mejora["m"], mas_mejora["n"] / mas_mejora["m"],
        mas_mejora["mejora_LPT_pct"], formato_tiempo(mas_mejora["t_LPT"] - mas_mejora["t_LS"])))

    print("\n  2. Menor beneficio de LPT (convergencia asintótica):")
    print("     n = %d, m = %d (n/m = %.1f) -> reduce el makespan en %.4f %% por %s extra." % (
        menos_mejora["n"], menos_mejora["m"], menos_mejora["n"] / menos_mejora["m"],
        menos_mejora["mejora_LPT_pct"], formato_tiempo(menos_mejora["t_LPT"] - menos_mejora["t_LS"])))

    min_sc = min(f["sobrecosto_LPT_pct"] for f in filas_p2)
    max_sc = max(f["sobrecosto_LPT_pct"] for f in filas_p2)
    print("\n  3. Rango de sobrecosto temporal de LPT:")
    print("     Entre %+.0f %% y %+.0f %% respecto a List Scheduling." % (min_sc, max_sc))
    print("     Dado que ambos corren en fracciones de segundo (incluso con 100 000 trabajos),")
    print("     el costo de ordenar es insignificante en términos absolutos frente a la garantía")
    print("     y consistencia que proporciona LPT.")


if __name__ == "__main__":
    main()
