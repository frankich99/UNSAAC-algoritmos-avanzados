# -*- coding: utf-8 -*-
"""
Pruebas de Factibilidad y Casos Límite
Problema: Pm || Cmax

Verifica rigurosamente:
  1. Validación de planificaciones y detección de anomalías (multiconjunto con Counter).
  2. Detección y rechazo de entradas inválidas.
  3. Casos límite de tamaño (n=0, m=1, m>n, n=m, trabajos idénticos).
  4. Instancias ajustadas que tocan las garantías teóricas (Graham para LS y LPT).
  5. Propiedades de algoritmos (determinismo, inmutabilidad de entrada, control de límite de nodos).
  6. Factibilidad masiva sobre 300 instancias aleatorias (900 soluciones validadas).
"""

import csv
import heapq
import os
from collections import Counter
from random import Random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

SEMILLA_GLOBAL = 2026


# ============================================================================
# Algoritmos y funciones auxiliares
# ============================================================================

def validar_instancia(trabajos, m):
    if not isinstance(m, int) or m <= 0:
        raise ValueError("El numero de maquinas debe ser un entero positivo")
    for p in trabajos:
        if not isinstance(p, int) or p <= 0:
            raise ValueError("Cada tiempo de proceso debe ser un entero positivo: %r" % (p,))


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


def lpt(trabajos, m):
    ordenados = sorted(trabajos, reverse=True)
    return list_scheduling(ordenados, m)


class LimiteNodosExcedido(Exception):
    def __init__(self, nodos):
        super().__init__("Limite de nodos excedido (%d nodos)" % nodos)
        self.nodos = nodos


def branch_and_bound(trabajos, m, limite_nodos=None):
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")

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


def instancia_ajustada_ls(m):
    return [1] * (m * (m - 1)) + [m]


def instancia_ajustada_lpt(m):
    trabajos = []
    for p in range(2 * m - 1, m, -1):
        trabajos += [p, p]
    return trabajos + [m, m, m]


def lanza_error(funcion, *argumentos):
    try:
        funcion(*argumentos)
    except ValueError:
        return True
    return False


def mostrar_tabla(encabezados, filas, titulo=None):
    if titulo:
        print("\n" + "=" * 70)
        print(titulo)
        print("=" * 70)
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
    print("=" * 70)
    print("PRUEBAS DE FACTIBILIDAD Y CASOS LÍMITE")
    print("=" * 70)

    resultados_pruebas = []

    def registrar(nombre, obtenido, esperado):
        ok = obtenido == esperado
        resultados_pruebas.append([len(resultados_pruebas) + 1, nombre, str(obtenido),
                                   str(esperado), "OK" if ok else "FALLA"])
        assert ok, "Falló la prueba '%s': obtenido %r, esperado %r" % (nombre, obtenido, esperado)

    # ---- 1. Validación de planificaciones --------------------------------------
    t = [7, 6, 5, 4, 3]
    registrar("Ejemplo de la guia es factible", es_factible(t, [[7], [6, 3], [5, 4]], 3), True)
    registrar("Cargas del ejemplo", cargas([[7], [6, 3], [5, 4]]), [7, 9, 9])
    registrar("Falta un trabajo -> no factible", es_factible(t, [[7], [6, 3], [5]], 3), False)
    registrar("Trabajo duplicado -> no factible", es_factible(t, [[7, 3], [6, 3], [5, 4]], 3), False)
    registrar("Numero de maquinas incorrecto", es_factible(t, [[7, 6], [5, 4, 3]], 3), False)
    registrar("Trabajo ajeno a la instancia", es_factible(t, [[7], [6, 3], [5, 8]], 3), False)
    registrar("Repetidos: set() aceptaria, Counter no",
              (set([5, 3]) == set([5, 5, 3]), es_factible([5, 5, 3], [[5], [3]], 2)), (True, False))
    registrar("Repetidos bien asignados", es_factible([5, 5, 3], [[5], [5, 3]], 2), True)

    # ---- 2. Entradas invalidas -------------------------------------------------
    registrar("m = 0 en cota_inferior -> ValueError", lanza_error(cota_inferior, [1, 2], 0), True)
    registrar("m < 0 en list_scheduling -> ValueError", lanza_error(list_scheduling, [1, 2], -1), True)
    registrar("m = 0 en Ramificar-Podar -> ValueError", lanza_error(branch_and_bound, [1], 0), True)
    registrar("Tiempo p_j = 0 -> ValueError", lanza_error(validar_instancia, [3, 0, 2], 2), True)
    registrar("Tiempo negativo -> ValueError", lanza_error(validar_instancia, [3, -1], 2), True)
    registrar("Tiempo no entero -> ValueError", lanza_error(validar_instancia, [2.5, 1], 2), True)

    # ---- 3. Casos limite de tamano ---------------------------------------------
    registrar("Sin trabajos: LB = 0", cota_inferior([], 3), 0)
    registrar("Sin trabajos: LS da 3 maquinas vacias", list_scheduling([], 3), ([[], [], []], 0))
    registrar("Sin trabajos: optimo = 0", branch_and_bound([], 3)[1], 0)

    t = [4, 9, 2, 7]
    registrar("m = 1: LS = suma", list_scheduling(t, 1)[1], sum(t))
    registrar("m = 1: optimo = suma", branch_and_bound(t, 1)[1], sum(t))
    registrar("m > n: LS = trabajo mas largo", list_scheduling(t, 6)[1], max(t))
    registrar("m > n: LB = OPT = trabajo mas largo",
              (cota_inferior(t, 6), branch_and_bound(t, 6)[1]), (9, 9))
    registrar("n = m: un trabajo por maquina", lpt(t, 4)[1], 9)
    registrar("Todos iguales, n = 3m: OPT = 3p = LB",
              (branch_and_bound([5] * 9, 3)[1], cota_inferior([5] * 9, 3)), (15, 15))
    registrar("LB < OPT: [2,2,2], m=2",
              (cota_inferior([2, 2, 2], 2), branch_and_bound([2, 2, 2], 2)[1]), (3, 4))

    # ---- 4. Instancias ajustadas: la garantia se alcanza pero no se supera -----
    for m in (2, 3, 4):
        t_ls = instancia_ajustada_ls(m)
        _, c_ls = list_scheduling(t_ls, m)
        _, opt, _ = branch_and_bound(t_ls, m)
        registrar("Ajustada LS m=%d: r = 2 - 1/m" % m, (c_ls, opt, c_ls * m == (2 * m - 1) * opt),
                  (2 * m - 1, m, True))

    for m in (2, 3, 4):
        t_lpt = instancia_ajustada_lpt(m)
        _, c_lpt = lpt(t_lpt, m)
        _, opt, _ = branch_and_bound(t_lpt, m)
        registrar("Ajustada LPT m=%d: r = 4/3 - 1/(3m)" % m, (c_lpt, opt), (4 * m - 1, 3 * m))

    # ---- 5. Propiedades de las implementaciones --------------------------------
    t = [8, 3, 5, 3, 9, 1]
    copia = list(t)
    lpt(t, 2)
    list_scheduling(t, 2)
    registrar("LS y LPT no modifican la entrada", t, copia)
    registrar("Desempate determinista (dos ejecuciones)", list_scheduling(t, 3), list_scheduling(t, 3))
    registrar("Desempate: con cargas iguales gana el menor id", list_scheduling([5, 5, 5], 3)[0],
              [[5], [5], [5]])

    def aborta_por_limite():
        try:
            branch_and_bound(instancia_ajustada_lpt(4), 4, limite_nodos=1)
        except LimiteNodosExcedido:
            return True
        return False

    registrar("Limite de nodos detiene la busqueda", aborta_por_limite(), True)

    # ---- 6. Factibilidad masiva: 300 instancias aleatorias pequenas ------------
    generador = Random(SEMILLA_GLOBAL)
    salidas_validas = 0
    orden_correcto = 0
    for _ in range(300):
        m = generador.randint(1, 4)
        t_rand = [generador.randint(1, 20) for _ in range(generador.randint(0, 9))]
        plan_ls, v_ls = list_scheduling(t_rand, m)
        plan_lpt, v_lpt = lpt(t_rand, m)
        plan_bb, v_bb, _ = branch_and_bound(t_rand, m)
        if all(verificar_solucion(t_rand, m, p, v) for p, v in
               ((plan_ls, v_ls), (plan_lpt, v_lpt), (plan_bb, v_bb))):
            salidas_validas += 1
        if v_bb <= v_lpt and v_bb <= v_ls:
            orden_correcto += 1

    registrar("300 instancias: las 900 salidas son factibles", salidas_validas, 300)
    registrar("300 instancias: OPT <= LPT y OPT <= LS", orden_correcto, 300)

    # Mostrar resultados
    mostrar_tabla(["#", "Prueba", "Obtenido", "Esperado", "Estado"], resultados_pruebas,
                  "Resumen de Pruebas de Factibilidad y Casos Límite")
    print("\n%d de %d pruebas superadas con éxito." % (
        sum(1 for f in resultados_pruebas if f[4] == "OK"), len(resultados_pruebas)))

    guardar_csv("pruebas_factibilidad.csv", ["n", "prueba", "obtenido", "esperado", "estado"],
                resultados_pruebas)


if __name__ == "__main__":
    main()
