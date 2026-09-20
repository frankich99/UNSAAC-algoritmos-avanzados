# -*- coding: utf-8 -*-
"""
Propuesto 1: Evaluación de Calidad de List Scheduling y LPT Frente al Óptimo
Problema: Pm || Cmax

Métricas evaluadas:
  * r(I)     = ALG(I) / OPT(I)               (razón observada >= 1)
  * delta(I) = (ALG(I) - OPT(I)) / OPT(I) %  (desviación relativa porcentual)
  * Garantías teóricas:
      - List Scheduling: r <= 2 - 1/m          <=>  m * C_LS <= (2m - 1) * OPT
      - LPT:             r <= 4/3 - 1/(3m)     <=>  3m * C_LPT <= (4m - 1) * OPT
  * Verificación formal de todas las planificaciones y comparación con cota inferior LB.
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
REPETICIONES = 7
LIMITE_NODOS_P1 = 5_000_000


# ============================================================================
# Funciones fundamentales
# ============================================================================

def validar_instancia(trabajos, m):
    if not isinstance(m, int) or m <= 0:
        raise ValueError("El numero de maquinas debe ser un entero positivo")
    for p in trabajos:
        if not isinstance(p, int) or p <= 0:
            raise ValueError("Cada tiempo de proceso debe ser un entero positivo")


def cargas(planificacion):
    return [sum(maquina) for maquina in planificacion]


def makespan(planificacion):
    return max(cargas(planificacion), default=0)


def es_factible(trabajos, planificacion, m):
    if len(planificacion) != m:
        return False
    asignados = [p for maquina in planificacion for p in maquina]
    return Counter(asignados) == Counter(trabajos)


def cota_inferior(trabajos, m):
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")
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


def verificar_solucion(trabajos, m, plan, valor):
    return (es_factible(trabajos, plan, m)
            and makespan(plan) == valor
            and valor >= cota_inferior(trabajos, m))


def garantia_ls(m):
    return 2.0 - 1.0 / m


def garantia_lpt(m):
    return 4.0 / 3.0 - 1.0 / (3.0 * m)


def respeta_garantia_ls(c, opt, m):
    return m * c <= (2 * m - 1) * opt


def respeta_garantia_lpt(c, opt, m):
    return 3 * m * c <= (4 * m - 1) * opt


def medir_mediana(funcion, *argumentos, repeticiones=REPETICIONES):
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


def generar_instancias_p1():
    familias = ("uniforme", "estrecha", "sesgada")
    m_vals = (2, 3, 4)
    n_vals = (6, 9, 12, 15)
    instancias = []
    contador = 0

    def gen_trabajos(n, familia, semilla):
        g = Random(semilla)
        if familia == "uniforme":
            return [g.randint(1, 20) for _ in range(n)]
        if familia == "estrecha":
            return [g.randint(10, 20) for _ in range(n)]
        if familia == "sesgada":
            return [g.randint(1, 5) if g.random() < 0.75 else g.randint(15, 30) for _ in range(n)]

    for familia in familias:
        for m in m_vals:
            for n in n_vals:
                for _ in range(2):
                    contador += 1
                    sem = SEMILLA_GLOBAL * 1000 + contador
                    instancias.append({
                        "id": "P1-%03d" % contador, "familia": familia, "n": n, "m": m,
                        "semilla": sem, "trabajos": gen_trabajos(n, familia, sem)})

    # Ajustadas
    for m in m_vals:
        contador += 1
        t_ls = [1] * (m * (m - 1)) + [m]
        instancias.append({"id": "P1-%03d" % contador, "familia": "ajustada_ls",
                           "n": len(t_ls), "m": m, "semilla": None, "trabajos": t_ls})
        contador += 1
        t_lpt = []
        for p in range(2 * m - 1, m, -1):
            t_lpt += [p, p]
        t_lpt += [m, m, m]
        instancias.append({"id": "P1-%03d" % contador, "familia": "ajustada_lpt",
                           "n": len(t_lpt), "m": m, "semilla": None, "trabajos": t_lpt})

    return instancias


def mostrar_tabla(encabezados, filas, titulo=None, max_filas=20):
    if titulo:
        print("\n" + "=" * 80)
        print(titulo)
        print("=" * 80)
    if max_filas is not None and len(filas) > max_filas:
        print("(Mostrando %d de %d filas; el archivo CSV contiene todas)" % (max_filas, len(filas)))
        filas = filas[:max_filas]
    anchos = [max(len(str(encabezados[i])),
                  max((len(str(f[i])) for f in filas), default=0)) + 2
              for i in range(len(encabezados))]
    print("".join(str(encabezados[i]).ljust(anchos[i]) for i in range(len(encabezados))))
    print("-" * sum(anchos))
    for fila in filas:
        print("".join(str(fila[i]).ljust(anchos[i]) for i in range(len(fila))))


def main():
    print("=" * 80)
    print("PROPUESTO 1: EVALUACIÓN EXPERIMENTAL DE CALIDAD FRENTE AL ÓPTIMO")
    print("=" * 80)

    instancias_p1 = generar_instancias_p1()
    print("Total de instancias a evaluar: %d (72 aleatorias + 6 ajustadas)" % len(instancias_p1))

    filas_p1 = []
    for inst in instancias_p1:
        t, m = inst["trabajos"], inst["m"]
        validar_instancia(t, m)

        (plan_ls, c_ls), t_ls = medir_mediana(list_scheduling, t, m)
        (plan_lpt, c_lpt), t_lpt = medir_mediana(lpt, t, m)
        (plan_bb, opt, nodos), t_bb = medir_mediana(branch_and_bound, t, m, LIMITE_NODOS_P1)
        lb = cota_inferior(t, m)

        # Validación formal
        assert verificar_solucion(t, m, plan_ls, c_ls), inst["id"]
        assert verificar_solucion(t, m, plan_lpt, c_lpt), inst["id"]
        assert verificar_solucion(t, m, plan_bb, opt), inst["id"]
        assert lb <= opt <= min(c_ls, c_lpt), inst["id"]

        filas_p1.append({
            "id": inst["id"], "familia": inst["familia"], "n": inst["n"], "m": m,
            "LB": lb, "OPT": opt, "C_LS": c_ls, "C_LPT": c_lpt,
            "r_LS": c_ls / opt, "r_LPT": c_lpt / opt,
            "dev_LS": 100.0 * (c_ls - opt) / opt, "dev_LPT": 100.0 * (c_lpt - opt) / opt,
            "t_LS": t_ls, "t_LPT": t_lpt, "t_BB": t_bb, "nodos": nodos,
            "LS_optimo": c_ls == opt, "LPT_optimo": c_lpt == opt, "OPT_igual_LB": opt == lb,
            "garantia_LS_ok": respeta_garantia_ls(c_ls, opt, m),
            "garantia_LPT_ok": respeta_garantia_lpt(c_lpt, opt, m),
        })

    # Guardar en CSV
    columnas = list(filas_p1[0].keys())
    ruta_csv = os.path.join(CARPETA_RESULTADOS, "propuesto1_calidad.csv")
    with open(ruta_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(columnas)
        for fila in filas_p1:
            writer.writerow([("%.9g" % fila[c]) if isinstance(fila[c], float) else fila[c] for c in columnas])
    print("\nResultados detallados guardados en:", ruta_csv)

    # Mostrar tabla resumen de primeras 20 instancias
    tabla_mostrar = [
        [f["id"], f["familia"], f["n"], f["m"], f["LB"], f["OPT"], f["C_LS"], f["C_LPT"],
         "%.3f" % f["r_LS"], "%.3f" % f["r_LPT"], f["nodos"], formato_tiempo(f["t_BB"])]
        for f in filas_p1
    ]
    mostrar_tabla(["id", "familia", "n", "m", "LB", "OPT", "C_LS", "C_LPT", "r_LS", "r_LPT", "nodos", "t_BB"],
                  tabla_mostrar, "Extracto de Instancias Evaluadas en Propuesto 1", max_filas=20)


if __name__ == "__main__":
    main()
