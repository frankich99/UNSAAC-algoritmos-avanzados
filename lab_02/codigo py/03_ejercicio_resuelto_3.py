# -*- coding: utf-8 -*-
"""
Ejercicio Resuelto 3: Ramificar-Podar Exacto (Branch and Bound)
Problema: Pm || Cmax

Características del método exacto:
  - Incumbente inicial: solución rápida proporcionada por LPT.
  - Poda por cota inferior: max(carga actual, cota promedio, trabajo restante mas largo).
  - Poda directa si la nueva carga parcial >= mejor makespan conocido.
  - Ruptura de simetría: no se evalúan máquinas con la misma carga actual.
  - Certificación en la raíz: si LPT alcanza LB global, devuelve el óptimo con 0 nodos explorados.
"""

import heapq
from collections import Counter


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
    """Tope de seguridad para no bloquear la sesión con instancias grandes."""
    def __init__(self, nodos):
        super().__init__("Limite de nodos excedido (%d nodos)" % nodos)
        self.nodos = nodos


def branch_and_bound(trabajos, m, limite_nodos=None):
    """
    Calcula una planificación ÓPTIMA mediante Ramificar y Podar.
    Devuelve (mejor_plan, optimo, nodos).
    """
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
            # Ruptura de simetría: dos máquinas con la misma carga son intercambiables
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

            # Si se probó una máquina vacía, las demás vacías son simétricas
            if nueva_carga == trabajo:
                break

    # Si LPT ya alcanza la cota global, es óptima y no hace falta explorar
    if mejor_valor == cota_inferior(trabajos, m):
        return mejor_plan, mejor_valor, nodos

    buscar(0)
    return mejor_plan, mejor_valor, nodos


def main():
    print("=" * 70)
    print("EJERCICIO RESUELTO 3: RAMIFICAR-PODAR EXACTO (BRANCH AND BOUND)")
    print("=" * 70)

    # --- Caso 1: Instancia donde LPT ya es óptimo ---
    t1 = [7, 6, 5, 4, 3]
    m1 = 3
    plan1, opt1, nodos1 = branch_and_bound(t1, m1)
    lb1 = cota_inferior(t1, m1)
    lpt_val1 = lpt(t1, m1)[1]

    print("Instancia 1 : %s en m = %d" % (t1, m1))
    print("  LB        : %d" % lb1)
    print("  LPT       : makespan = %d" % lpt_val1)
    print("  Óptimo    : makespan = %d" % opt1)
    print("  Plan      : %s" % plan1)
    print("  Cargas    : %s" % cargas(plan1))
    print("  Nodos     : %d (0 = certificado por la cota sin explorar el árbol)\n" % nodos1)

    # --- Caso 2: Instancia donde LPT NO es óptimo y se requiere explorar el árbol ---
    t2 = [3, 3, 2, 2, 2]
    m2 = 2
    plan2, opt2, nodos2 = branch_and_bound(t2, m2)
    lb2 = cota_inferior(t2, m2)
    lpt_plan2, lpt_val2 = lpt(t2, m2)

    print("Instancia 2 : %s en m = %d" % (t2, m2))
    print("  LB        : %d" % lb2)
    print("  LPT       : plan = %s -> makespan = %d" % (lpt_plan2, lpt_val2))
    print("  Óptimo    : plan = %s -> makespan = %d" % (plan2, opt2))
    print("  Cargas    : %s" % cargas(plan2))
    print("  Nodos     : %d" % nodos2)
    print("  Diferencia: LPT sobreestima el óptimo por %d unidad(es)" % (lpt_val2 - opt2))


if __name__ == "__main__":
    main()
