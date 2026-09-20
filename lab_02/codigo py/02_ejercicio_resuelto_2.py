# -*- coding: utf-8 -*-
"""
Ejercicio Resuelto 2: List Scheduling y LPT con Cola de Prioridad (Min-Heap)
Problema: Pm || Cmax

Algoritmos:
  1. List Scheduling (LS): asigna en orden de llegada a la máquina con menor carga actual.
     Implementación eficiente mediante min-heap: O(n log m).
  2. LPT (Longest Processing Time First): ordena los trabajos de mayor a menor y aplica LS.
     Complejidad: O(n log n) + O(n log m).
"""

import heapq
from collections import Counter


def cargas(planificacion):
    """L_i = suma de los tiempos asignados a la maquina i."""
    return [sum(maquina) for maquina in planificacion]


def makespan(planificacion):
    """Cmax = maxima carga."""
    return max(cargas(planificacion), default=0)


def es_factible(trabajos, planificacion, m):
    """Comprueba que la planificación use exactamente m máquinas y conserve todos los trabajos."""
    if len(planificacion) != m:
        return False
    asignados = [p for maquina in planificacion for p in maquina]
    return Counter(asignados) == Counter(trabajos)


def cota_inferior(trabajos, m):
    """LB = max( ceil(sum p_j / m), max p_j ) <= OPT."""
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")
    if not trabajos:
        return 0
    return max(-(-sum(trabajos) // m), max(trabajos))


def list_scheduling(trabajos, m):
    """
    Procesa los trabajos en el ORDEN RECIBIDO y asigna cada uno a la maquina
    de menor carga actual. Devuelve (planificacion, makespan).

    Cola de prioridad minima con tuplas (carga, identificador):
      * heap[0] es siempre la maquina de menor carga -> consulta O(1);
      * actualizarla cuesta O(log m)  ->  costo total O(n log m).

    Regla de desempate: con cargas iguales, Python compara el segundo
    elemento de la tupla, asi que gana la maquina de MENOR identificador.
    La eleccion es determinista: dos ejecuciones dan la misma planificacion.
    """
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")

    planificacion = [[] for _ in range(m)]
    heap = [(0, i) for i in range(m)]        # todas vacias: ya es un heap valido
    heapq.heapify(heap)

    for trabajo in trabajos:
        carga, maquina = heap[0]             # maquina menos cargada
        planificacion[maquina].append(trabajo)
        # heapreplace = extraer el minimo e insertar el nuevo en una sola
        # operacion O(log m), mas eficiente que heappop + heappush.
        heapq.heapreplace(heap, (carga + trabajo, maquina))

    return planificacion, max(carga for carga, _ in heap)


def lpt(trabajos, m):
    """
    Longest Processing Time first: ordenar de MAYOR a MENOR y aplicar
    List Scheduling. Costo O(n log n) del ordenamiento + O(n log m).
    sorted() crea una copia: la lista original del usuario no se modifica.
    """
    ordenados = sorted(trabajos, reverse=True)
    return list_scheduling(ordenados, m)


def main():
    print("=" * 70)
    print("EJERCICIO RESUELTO 2: LIST SCHEDULING Y LPT CON COLA DE PRIORIDAD")
    print("=" * 70)

    # --- Ejemplo de la guia ---
    trabajos = [3, 7, 4, 6, 5]
    m = 3

    lb = cota_inferior(trabajos, m)
    plan_ls, valor_ls = list_scheduling(trabajos, m)
    plan_lpt, valor_lpt = lpt(trabajos, m)

    print("Instancia      : trabajos = %s, m = %d" % (trabajos, m))
    print("Cota inferior  : LB = %d\n" % lb)

    print("List Scheduling:")
    print("  Planificación: %s" % plan_ls)
    print("  Cargas       : %s" % cargas(plan_ls))
    print("  Makespan     : %d" % valor_ls)
    print("  Factible     : %s" % es_factible(trabajos, plan_ls, m))

    print("\nLPT (orden descendente: %s):" % sorted(trabajos, reverse=True))
    print("  Planificación: %s" % plan_lpt)
    print("  Cargas       : %s" % cargas(plan_lpt))
    print("  Makespan     : %d" % valor_lpt)
    print("  Factible     : %s" % es_factible(trabajos, plan_lpt, m))

    print("\nConclusiones de la instancia:")
    if valor_ls == lb:
        print("  - List Scheduling alcanzó la cota inferior (Cmax = LB = %d): es ÓPTIMO." % lb)
    if valor_lpt == lb:
        print("  - LPT alcanzó la cota inferior (Cmax = LB = %d): es ÓPTIMO." % lb)

    assert es_factible(trabajos, plan_ls, m)
    assert es_factible(trabajos, plan_lpt, m)
    print("\n[OK] Ambas planificaciones son válidas y factibles.")


if __name__ == "__main__":
    main()
