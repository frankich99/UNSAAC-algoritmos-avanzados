#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio 04 - Algoritmos Avanzados (UNSAAC, 2026-II)
Script Maestro: Ejecuta secuencialmente todos los ejercicios resueltos y propuestos
"""

import sys
import resuelto_01_potencial
import resuelto_02_consolidacion
import resuelto_03_heapq_perezoso
import propuesto_01_fibonacci_heap
import propuesto_02_comparacion_dijkstra

def main():
    print("*" * 70)
    print(" INFORME DE LABORATORIO 04: EJECUCIÓN COMPLETA DE EJERCICIOS")
    print(" UNSAAC · Semestre 2026-II · Grupo 5")
    print("*" * 70)

    print("\n>>> EJECUTANDO RESUELTO 1...")
    resuelto_01_potencial.main()

    print("\n>>> EJECUTANDO RESUELTO 2...")
    resuelto_02_consolidacion.main()

    print("\n>>> EJECUTANDO RESUELTO 3...")
    resuelto_03_heapq_perezoso.main()

    print("\n>>> EJECUTANDO PROPUESTO 1...")
    propuesto_01_fibonacci_heap.main()

    print("\n>>> EJECUTANDO PROPUESTO 2...")
    propuesto_02_comparacion_dijkstra.main()

    print("\n" + "*" * 70)
    print(" [ÉXITO TOTAL] Todos los ejercicios resueltos y propuestos ejecutados.")
    print(" Gráficos guardados en 'figuras/' y tablas exportadas a 'resultados/'.")
    print("*" * 70)

if __name__ == "__main__":
    main()
