# -*- coding: utf-8 -*-
"""
Script Maestro: Ejecución Integral de Todo el Laboratorio 02
Problema: Pm || Cmax (Algoritmos Avanzados - UNSAAC)

Ejecuta secuencialmente los 14 scripts del laboratorio, garantizando:
  - Generación de todos los datos y archivos CSV en 'resultados/'
  - Generación de todas las figuras en alta resolución en 'figuras/'
  - Verificación formal de todas las afirmaciones, cotas y garantías.
"""

import os
import subprocess
import sys
from time import perf_counter

SCRIPTS = [
    ("01_ejercicio_resuelto_1.py", "Ejercicio Resuelto 1: Representación y validación"),
    ("02_ejercicio_resuelto_2.py", "Ejercicio Resuelto 2: List Scheduling y LPT"),
    ("03_ejercicio_resuelto_3.py", "Ejercicio Resuelto 3: Ramificar-Podar exacto"),
    ("04_pruebas_factibilidad.py", "Pruebas de factibilidad y casos límite"),
    ("05_complejidad_list_scheduling.py", "Complejidad: versión de la guía vs optimizada"),
    ("06_generador_instancias.py", "Generador reproducible de instancias (JSON)"),
    ("07_propuesto_1_calidad.py", "Propuesto 1: Evaluación de calidad frente al óptimo"),
    ("08_propuesto_1_resumen_dominancia.py", "Propuesto 1: Resumen estadístico y dominancia"),
    ("09_propuesto_1_grafico_calidad.py", "Propuesto 1: Gráfico de calidad observada"),
    ("10_propuesto_1_rendimiento_exacto.py", "Propuesto 1: Rendimiento y límite práctico de B&B"),
    ("11_propuesto_2_escalabilidad.py", "Propuesto 2: Efecto del orden y escalabilidad"),
    ("12_propuesto_2_instancia_sensible.py", "Propuesto 2: Instancia sensible y cota de Graham"),
    ("13_propuesto_2_graficos.py", "Propuesto 2: Gráficos de distribución, escala y tiempos"),
    ("14_propuesto_2_costo_ordenamiento.py", "Propuesto 2: Análisis costo-beneficio de ordenar"),
]


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print("=" * 80)
    print("EJECUTOR MAESTRO DEL LABORATORIO 02 - UNSAAC")
    print("=" * 80)
    print("Directorio de trabajo:", base_dir)
    print("Total de scripts a procesar: %d\n" % len(SCRIPTS))

    t_inicio_total = perf_counter()
    exitosos = 0

    for idx, (archivo, descripcion) in enumerate(SCRIPTS, start=1):
        ruta_script = os.path.join(base_dir, archivo)
        print("-" * 80)
        print("[%02d/%02d] Ejecutando: %s" % (idx, len(SCRIPTS), archivo))
        print("        Descripción: %s" % descripcion)
        print("-" * 80)

        t_inicio = perf_counter()
        resultado = subprocess.run([sys.executable, ruta_script], cwd=base_dir)
        duracion = perf_counter() - t_inicio

        if resultado.returncode == 0:
            print(">>> [EXITOSO] %s finalizado en %.2f segundos.\n" % (archivo, duracion))
            exitosos += 1
        else:
            print(">>> [ERROR] %s falló con código de salida %d.\n" % (archivo, resultado.returncode))
            sys.exit(resultado.returncode)

    duracion_total = perf_counter() - t_inicio_total
    print("=" * 80)
    print("RESUMEN GENERAL: %d de %d scripts ejecutados con éxito en %.2f segundos."
          % (exitosos, len(SCRIPTS), duracion_total))
    print("=" * 80)

    # Listar archivos generados
    carpeta_res = os.path.join(base_dir, "resultados")
    carpeta_fig = os.path.join(base_dir, "figuras")

    if os.path.exists(carpeta_res):
        print("\nArchivos en 'resultados/':")
        for f in sorted(os.listdir(carpeta_res)):
            print("  -", f)

    if os.path.exists(carpeta_fig):
        print("\nFiguras generadas en 'figuras/':")
        for f in sorted(os.listdir(carpeta_fig)):
            print("  -", f)


if __name__ == "__main__":
    main()
