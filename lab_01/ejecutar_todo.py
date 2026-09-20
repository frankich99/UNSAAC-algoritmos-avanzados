# -*- coding: utf-8 -*-
"""
Laboratorio 01 - Algoritmos Avanzados (UNSAAC 2026-II)
Script Maestro de Ejecución Completa (100% Offline)

Grupo 5:
  - Choquenaira Quispe, Noe Franklin (133962)
  - Porroa Sivana, Yeni Ruth (120893)
  - Quispe Rimachi, Romario (164257)
  - Yaranga Achahui, Aldo (103179)

Este script ejecuta secuencialmente todos los ejercicios del laboratorio:
  1. Ejercicio Resuelto 1 (Suma lineal vs Pares cuadráticos -> grafico_1.png)
  2. Ejercicio Resuelto 2 (Búsqueda lineal vs Binaria -> grafico_2.png)
  3. Ejercicio Resuelto 3 (Subset Sum: FB, DP, B&B -> grafico_3.png)
  4. Ejercicio Propuesto 1 (Insertion Sort vs Merge Sort -> CSV, grafico_4.png, grafico_5.png)
  5. Ejercicio Propuesto 2 (Límite exponencial Subset Sum -> JSON, grafico_6.png)
"""

import sys
import os
import time

# Asegurar UTF-8 en consola
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

import resuelto_1_crecimiento
import resuelto_2_busquedas
import resuelto_3_subset_sum
import propuesto_1_ordenamientos
import propuesto_2_subset_sum_limite

def main():
    print("=" * 90)
    print(" UNIVERSIDAD NACIONAL DE SAN ANTONIO ABAD DEL CUSCO")
    print(" INGENIERÍA INFORMÁTICA Y DE SISTEMAS - ALGORITMOS AVANZADOS (2026-II)")
    print(" LABORATORIO 01: COMPLEJIDAD Y EXPERIMENTACIÓN ALGORÍTMICA - GRUPO 5")
    print("=" * 90)
    print("\nIniciando bateria de experimentos completos en modo OFFLINE...\n")
    t0 = time.perf_counter()

    # 1. Resuelto 1
    print("\n" + "#" * 90)
    print(">>> EJECUTANDO [1/5]: Ejercicio Resuelto 1")
    print("#" * 90)
    resuelto_1_crecimiento.ejecutar(mostrar_grafico=False)

    # 2. Resuelto 2
    print("\n" + "#" * 90)
    print(">>> EJECUTANDO [2/5]: Ejercicio Resuelto 2")
    print("#" * 90)
    resuelto_2_busquedas.ejecutar(mostrar_grafico=False)

    # 3. Resuelto 3
    print("\n" + "#" * 90)
    print(">>> EJECUTANDO [3/5]: Ejercicio Resuelto 3")
    print("#" * 90)
    resuelto_3_subset_sum.ejecutar(mostrar_grafico=False)

    # 4. Propuesto 1
    print("\n" + "#" * 90)
    print(">>> EJECUTANDO [4/5]: Ejercicio Propuesto 1")
    print("#" * 90)
    propuesto_1_ordenamientos.ejecutar(mostrar_grafico=False)

    # 5. Propuesto 2
    print("\n" + "#" * 90)
    print(">>> EJECUTANDO [5/5]: Ejercicio Propuesto 2")
    print("#" * 90)
    propuesto_2_subset_sum_limite.ejecutar(mostrar_grafico=False)

    total_tiempo = time.perf_counter() - t0
    print("\n" + "=" * 90)
    print(f" [V] TODOS LOS EXPERIMENTOS FINALIZARON EXITOSAMENTE EN {total_tiempo:.2f} SEGUNDOS.")
    print("=" * 90)
    print("\nArchivos y graficos generados:")
    archivos = [
        "grafico_1.png",
        "grafico_2.png",
        "grafico_3.png",
        "grafico_4.png",
        "grafico_5.png",
        "grafico_6.png",
        "propuesto1_ordenamientos.csv",
        "propuesto2_instancias.json"
    ]
    for arch in archivos:
        existe = "[OK]" if os.path.exists(arch) else "[FALTA]"
        tam = f"({os.path.getsize(arch):,} bytes)" if os.path.exists(arch) else ""
        print(f"  {existe:<8} {arch:<32} {tam}")
    print("\nPuede consultar el informe completo y la justificación teórica en:")
    print("  INFORME_Y_GUIA_EJECUCION.md\n")

if __name__ == '__main__':
    main()
