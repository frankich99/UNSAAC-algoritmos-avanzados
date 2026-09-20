# -*- coding: utf-8 -*-
"""
Propuesto 1: Resumen Estadístico, Garantías Teóricas y Análisis de Dominancia
Problema: Pm || Cmax

Responde a las preguntas de investigación:
  1. ¿Las heurísticas respetan las garantías de aproximación (2 - 1/m y 4/3 - 1/(3m))?
  2. ¿Con qué frecuencia la cota inferior LB certifica el óptimo en la raíz (0 nodos)?
  3. ¿LPT domina estrictamente a List Scheduling en todas las instancias?
  4. Análisis exhaustivo: evaluación de TODOS los órdenes posibles (permutaciones)
     en la instancia ajustada de LPT para entender por qué LS puede superar a LPT.
"""

import csv
import heapq
import os
from collections import Counter
from itertools import permutations
from statistics import mean, median

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

M_P1 = (2, 3, 4)


def garantia_ls(m):
    return 2.0 - 1.0 / m


def garantia_lpt(m):
    return 4.0 / 3.0 - 1.0 / (3.0 * m)


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


def cota_inferior(trabajos, m):
    if not trabajos:
        return 0
    return max(-(-sum(trabajos) // m), max(trabajos))


def branch_and_bound(trabajos, m):
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
            nueva = cargas_actuales[i] + trabajo
            if nueva >= mejor_valor:
                continue
            cargas_actuales[i] = nueva
            plan_actual[i].append(trabajo)
            restante = trabajos[k + 1] if k + 1 < n else 0
            if max(max(cargas_actuales), cota_promedio, restante) < mejor_valor:
                buscar(k + 1)
            plan_actual[i].pop()
            cargas_actuales[i] -= trabajo
            if nueva == trabajo:
                break

    if mejor_valor == cota_inferior(trabajos, m):
        return mejor_plan, mejor_valor, nodos
    buscar(0)
    return mejor_plan, mejor_valor, nodos


def instancia_ajustada_lpt(m):
    trabajos = []
    for p in range(2 * m - 1, m, -1):
        trabajos += [p, p]
    return trabajos + [m, m, m]


def cargar_o_generar_filas_p1():
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto1_calidad.csv")
    if os.path.exists(ruta_csv):
        filas = []
        with open(ruta_csv, "r", encoding="utf-8") as f:
            lector = csv.DictReader(f)
            for row in lector:
                filas.append({
                    "id": row["id"],
                    "familia": row["familia"],
                    "n": int(row["n"]),
                    "m": int(row["m"]),
                    "LB": int(row["LB"]),
                    "OPT": int(row["OPT"]),
                    "C_LS": int(row["C_LS"]),
                    "C_LPT": int(row["C_LPT"]),
                    "r_LS": float(row["r_LS"]),
                    "r_LPT": float(row["r_LPT"]),
                    "dev_LS": float(row["dev_LS"]),
                    "dev_LPT": float(row["dev_LPT"]),
                    "nodos": int(row["nodos"]),
                    "LS_optimo": row["LS_optimo"] in ("True", "1"),
                    "LPT_optimo": row["LPT_optimo"] in ("True", "1"),
                    "OPT_igual_LB": row["OPT_igual_LB"] in ("True", "1"),
                    "garantia_LS_ok": row["garantia_LS_ok"] in ("True", "1"),
                    "garantia_LPT_ok": row["garantia_LPT_ok"] in ("True", "1"),
                })
        return filas

    # Si no existe, ejecutar script 07 o generarlas al vuelo
    import subprocess
    import sys
    script_07 = os.path.join(BASE_DIR, "07_propuesto_1_calidad.py")
    if os.path.exists(script_07):
        print("Ejecutando evaluación de calidad previa...")
        subprocess.run([sys.executable, script_07], check=True)
        return cargar_o_generar_filas_p1()
    raise FileNotFoundError("No se encontró propuesto1_calidad.csv ni el generador 07.")


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


def guardar_csv(nombre_archivo, encabezados, filas):
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    with open(ruta, "w", newline="", encoding="utf-8") as f:
        escritor = csv.writer(f)
        escritor.writerow(encabezados)
        escritor.writerows(filas)
    print("CSV guardado en:", ruta)


def main():
    print("=" * 80)
    print("PROPUESTO 1: RESUMEN, GARANTÍAS TEÓRICAS Y ANÁLISIS DE DOMINANCIA")
    print("=" * 80)

    filas_p1 = cargar_o_generar_filas_p1()
    aleatorias = [f for f in filas_p1 if not f["familia"].startswith("ajustada")]
    ajustadas = [f for f in filas_p1 if f["familia"].startswith("ajustada")]

    def resumir(grupo, etiqueta):
        filas = []
        for alg, gar in (("LS", garantia_ls), ("LPT", garantia_lpt)):
            razones = [f["r_" + alg] for f in grupo]
            desv = [f["dev_" + alg] for f in grupo]
            gs = sorted({gar(f["m"]) for f in grupo})
            texto_gar = "%.3f" % gs[0] if len(gs) == 1 else "%.3f - %.3f" % (gs[0], gs[-1])
            filas.append([etiqueta, alg, len(grupo),
                          "%d (%.0f %%)" % (sum(f[alg + "_optimo"] for f in grupo),
                                            100 * sum(f[alg + "_optimo"] for f in grupo) / len(grupo)),
                          "%.4f" % mean(razones), "%.4f" % median(razones), "%.4f" % max(razones),
                          "%.2f" % mean(desv), texto_gar,
                          sum(not f["garantia_%s_ok" % alg] for f in grupo)])
        return filas

    encabezado_resumen = ["grupo", "alg", "instancias", "veces optimo", "r promedio",
                          "r mediana", "r maxima", "desv. prom. %", "garantia", "violaciones"]
    resumen_p1 = []
    for m in M_P1:
        resumen_p1 += resumir([f for f in aleatorias if f["m"] == m], "aleatorias m=%d" % m)
    resumen_p1 += resumir(aleatorias, "aleatorias (todas)")
    resumen_p1 += resumir(ajustadas, "ajustadas")

    mostrar_tabla(encabezado_resumen, resumen_p1, "Resumen de Calidad Observada vs. Garantía Teórica")
    guardar_csv("propuesto1_resumen.csv", encabezado_resumen, resumen_p1)

    # ---- 1. Verificación de Garantías Teóricas ----
    violaciones = sum(not f["garantia_LS_ok"] or not f["garantia_LPT_ok"] for f in filas_p1)
    print("\n1. Verificación de garantías teóricas en %d instancias:" % len(filas_p1))
    print("   Total de violaciones observadas: %d" % violaciones)
    assert violaciones == 0, "Error crítico: Se detectaron violaciones a la cota teórica de Graham"

    print("\n   Comportamiento en instancias ajustadas (deben tocar exactamente la cota):")
    for f in ajustadas:
        alg = "LS" if f["familia"] == "ajustada_ls" else "LPT"
        gar = garantia_ls(f["m"]) if alg == "LS" else garantia_lpt(f["m"])
        print("     %s m=%d: r_%s = %d/%d = %.4f | garantia = %.4f" % (
            f["familia"], f["m"], alg, f["C_" + alg], f["OPT"], f["r_" + alg], gar))

    # ---- 2. Cota Inferior como Certificado ----
    certificadas = sum(f["OPT_igual_LB"] for f in filas_p1)
    sin_explorar = sum(f["nodos"] == 0 for f in filas_p1)
    print("\n2. Cota inferior como certificado:")
    print("   - OPT = LB en %d de %d instancias." % (certificadas, len(filas_p1)))
    print("   - En %d instancias, Branch & Bound exploró 0 nodos porque LPT ya alcanzaba LB."
          % sin_explorar)

    # ---- 3. Pregunta de Análisis: ¿LPT Domina a List Scheduling? ----
    lpt_mejor = [f for f in aleatorias if f["C_LPT"] < f["C_LS"]]
    empates = [f for f in aleatorias if f["C_LPT"] == f["C_LS"]]
    ls_mejor = [f for f in aleatorias if f["C_LS"] < f["C_LPT"]]

    print("\n3. Comparación directa entre LPT y LS (%d instancias aleatorias):" % len(aleatorias))
    print("   - LPT mejor que LS : %d instancias" % len(lpt_mejor))
    print("   - Empate           : %d instancias (en %d de ellas, ambos óptimos)"
          % (len(empates), sum(f["LS_optimo"] for f in empates)))
    print("   - LS mejor que LPT : %d instancias  <-- EXCEPCIONES" % len(ls_mejor))

    if ls_mejor:
        mostrar_tabla(
            ["id", "familia", "n", "m", "OPT", "C_LS", "C_LPT", "diferencia"],
            [[f["id"], f["familia"], f["n"], f["m"], f["OPT"], f["C_LS"], f["C_LPT"],
              f["C_LPT"] - f["C_LS"]] for f in ls_mejor],
            "Casos excepcionales donde List Scheduling supera a LPT")

    # ---- 4. Análisis exhaustivo de todos los órdenes posibles en instancia ajustada ----
    print("\n4. Evaluación de TODOS los órdenes en la instancia ajustada de LPT:")
    analisis_ordenes = []
    for m in (2, 3):
        t = instancia_ajustada_lpt(m)
        _, c_lpt = lpt(t, m)
        _, opt, _ = branch_and_bound(t, m)
        conteo = Counter(list_scheduling(list(orden), m)[1] for orden in permutations(t))
        total = sum(conteo.values())
        mejores = sum(v for k, v in conteo.items() if k < c_lpt)
        analisis_ordenes.append([m, str(t), total, opt, c_lpt,
                                 str(dict(sorted(conteo.items()))),
                                 "%d (%.1f %%)" % (mejores, 100.0 * mejores / total)])

    mostrar_tabla(["m", "trabajos", "total_ordenes", "OPT", "C_LPT",
                   "distribucion_makespans", "ordenes_donde_LS_supera_LPT"],
                  analisis_ordenes,
                  "Distribución exhaustiva de makespans según el orden")
    guardar_csv("propuesto1_ordenes_ajustada_lpt.csv",
                ["m", "trabajos", "ordenes", "OPT", "C_LPT", "distribucion", "LS_mejor_que_LPT"],
                analisis_ordenes)


if __name__ == "__main__":
    main()
