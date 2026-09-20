# -*- coding: utf-8 -*-
"""
Ejercicio Resuelto 1: Representación y Validación de Instancias y Planificaciones
Problema: Pm || Cmax (Programación de Trabajos en Máquinas Paralelas Idénticas)

Representación adoptada:
  * trabajos      : lista de enteros positivos p_j (puede haber repetidos)
  * m             : número de máquinas idénticas (entero >= 1)
  * planificacion : lista de m listas; la lista i contiene los trabajos asignados a la máquina i.
"""

from collections import Counter


def validar_instancia(trabajos, m):
    """
    Rechaza entradas que no pertenecen al problema Pm || Cmax.
    El marco teórico exige m >= 1 y tiempos p_j > 0 enteros.
    """
    if not isinstance(m, int) or m <= 0:
        raise ValueError("El numero de maquinas debe ser un entero positivo")
    for p in trabajos:
        if not isinstance(p, int) or p <= 0:
            raise ValueError("Cada tiempo de proceso debe ser un entero positivo: %r" % (p,))


def cargas(planificacion):
    """L_i = suma de los tiempos asignados a la maquina i."""
    return [sum(maquina) for maquina in planificacion]


def makespan(planificacion):
    """Cmax = maxima carga. default=0 cubre el caso sin maquinas/trabajos."""
    return max(cargas(planificacion), default=0)


def es_factible(trabajos, planificacion, m):
    """
    Una planificacion es factible si:
      1) tiene exactamente m maquinas;
      2) cada trabajo aparece exactamente una vez (ni falta ni sobra).
    Se compara con Counter (multiconjunto) y NO con set: una instancia puede
    tener trabajos con la misma duracion, y set() perderia las repeticiones.
    """
    if len(planificacion) != m:
        return False
    asignados = [p for maquina in planificacion for p in maquina]
    return Counter(asignados) == Counter(trabajos)


def cota_inferior(trabajos, m):
    """
    LB = max( ceil(sum p_j / m), max p_j ) <= OPT
      * carga promedio: alguna maquina recibe al menos el promedio;
      * trabajo mas largo: no se interrumpe, cabe entero en una maquina.
    Se usa aritmetica entera (-(-a // b) == ceil(a / b)) para evitar errores
    de redondeo de punto flotante con sumas grandes.
    """
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")
    if not trabajos:
        return 0
    return max(-(-sum(trabajos) // m), max(trabajos))


def main():
    print("=" * 70)
    print("EJERCICIO RESUELTO 1: REPRESENTACIÓN Y VALIDACIÓN")
    print("=" * 70)

    # --- Ejemplo de la guia ---
    trabajos = [7, 6, 5, 4, 3]
    m = 3
    planificacion = [[7], [6, 3], [5, 4]]

    validar_instancia(trabajos, m)
    lb = cota_inferior(trabajos, m)
    c = cargas(planificacion)
    cmax = makespan(planificacion)
    factible = es_factible(trabajos, planificacion, m)

    print("Instancia       : trabajos = %s, m = %d" % (trabajos, m))
    print("Planificación   : %s" % planificacion)
    print("Factible        :", factible)
    print("Cargas (L_i)    :", c)
    print("Makespan (Cmax) :", cmax)
    print("Cota inferior   :", lb)

    # Si el makespan alcanza una cota inferior valida, la planificacion es optima:
    # ninguna planificacion puede bajar de LB, y esta ya la alcanzo.
    if cmax == lb:
        print("-> El makespan alcanza la cota inferior (Cmax = LB = %d): la planificación es ÓPTIMA." % lb)
    else:
        print("-> Cmax (%d) > LB (%d): la planificación es factible pero no garantiza optimalidad." % (cmax, lb))

    # Prueba con una solución no factible (falta un trabajo)
    plan_invalida = [[7], [6], [5, 4]]
    print("\nValidación con plan incompleta %s:" % plan_invalida)
    print("Factible        :", es_factible(trabajos, plan_invalida, m))


if __name__ == "__main__":
    main()
