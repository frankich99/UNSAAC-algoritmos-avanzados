# -*- coding: utf-8 -*-
"""
Laboratorio 01 - Algoritmos Avanzados (UNSAAC 2026-II)
Ejercicio Propuesto 1: Insertion Sort frente a Merge Sort
Sección 7.1 de la Guía Oficial

Requisitos:
  1. Contar comparaciones entre elementos.
  2. Medir la mediana de al menos 7 ejecuciones con perf_counter.
  3. Usar exactamente las mismas listas para ambos algoritmos.
  4. Comprobar que las salidas coincidan con sorted(datos).
  5. Presentar tabla con n, tipo, comparaciones y tiempo. Guardar CSV.
  6. Generar gráficos de tiempo y comparaciones (grafico_4.png y grafico_5.png).
  7. Analizar la dependencia del orden inicial y el punto de cruce experimental.
"""

import os
import sys
import csv
import math
from random import Random
from statistics import median
from time import perf_counter
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Asegurar UTF-8 en consola
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (16, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['font.size'] = 11

SEMILLA_GLOBAL = 2026
REPETICIONES = 7
CARPETA_SALIDA = os.path.dirname(os.path.abspath(__file__))

def formato_tiempo(segundos):
    if segundos is None or math.isnan(segundos):
        return 'omitido'
    if segundos < 1e-3:
        return f"{segundos * 1e6:8.2f} us"
    if segundos < 1.0:
        return f"{segundos * 1e3:8.3f} ms"
    return f"{segundos:8.4f} s"

def medir_mediana(funcion, *args, repeticiones=REPETICIONES):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        t_inicio = perf_counter()
        resultado = funcion(*args)
        t_fin = perf_counter()
        tiempos.append(t_fin - t_inicio)
    return resultado, median(tiempos)

# ----------------------------------------------------------------------------
# Algoritmos de ordenamiento instrumentados
# ----------------------------------------------------------------------------
def insertion_sort(datos):
    """
    Ordenamiento por inserción directa instrumentado.
    Retorna: (lista_ordenada, total_comparaciones)
    Complejidad teórica:
      - Mejor caso (ordenado): Θ(n) comparaciones, 0 intercambios.
      - Peor caso (inverso): Θ(n^2) comparaciones (n*(n-1)/2).
      - Caso promedio (aleatorio): Θ(n^2) comparaciones (n*(n-1)/4 aprox).
    """
    arr = list(datos)
    n = len(arr)
    comparaciones = 0
    for i in range(1, n):
        clave = arr[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if arr[j] > clave:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = clave
    return arr, comparaciones

def merge_sort(datos):
    """
    Ordenamiento por mezcla (Merge Sort) instrumentado.
    Retorna: (lista_ordenada, total_comparaciones)
    Complejidad teórica:
      - Todos los casos (no adaptativo): Θ(n log n).
    """
    comparaciones = 0

    def mezclar(izq, der):
        nonlocal comparaciones
        resultado = []
        i = j = 0
        while i < len(izq) and j < len(der):
            comparaciones += 1
            if izq[i] <= der[j]:
                resultado.append(izq[i])
                i += 1
            else:
                resultado.append(der[j])
                j += 1
        resultado.extend(izq[i:])
        resultado.extend(der[j:])
        return resultado

    def dividir_y_ordenar(sub):
        if len(sub) <= 1:
            return sub
        medio = len(sub) // 2
        izq = dividir_y_ordenar(sub[:medio])
        der = dividir_y_ordenar(sub[medio:])
        return mezclar(izq, der)

    resultado = dividir_y_ordenar(list(datos))
    return resultado, comparaciones

# ----------------------------------------------------------------------------
# Experimento comparativo
# ----------------------------------------------------------------------------
def ejecutar(mostrar_grafico=False):
    print("=" * 95)
    print(" EJERCICIO PROPUESTO 1: INSERTION SORT VS MERGE SORT (7 REPETICIONES)")
    print("=" * 95)

    tamanos_p1 = [10, 20, 50, 100, 200, 500, 1000, 2000, 3000]
    tipos_entrada = ['Aleatoria', 'Ordenada', 'Inversa']
    gen_sort = Random(SEMILLA_GLOBAL)
    resultados_p1 = []

    print(f"{'n':>6} | {'Tipo':<10} | {'Comp. Ins.':>11} | {'Comp. Merge':>11} | {'T. Ins.':>14} | {'T. Merge':>14} | {'Más Rápido':<11}")
    print("-" * 95)

    for n in tamanos_p1:
        base_aleatoria = [gen_sort.randint(1, 10_000) for _ in range(n)]
        for tipo in tipos_entrada:
            if tipo == 'Aleatoria':
                datos = base_aleatoria.copy()
            elif tipo == 'Ordenada':
                datos = sorted(base_aleatoria)
            else:
                datos = sorted(base_aleatoria, reverse=True)

            esperado = sorted(datos)
            (arr_ins, comp_ins), t_ins = medir_mediana(insertion_sort, datos)
            (arr_mrg, comp_mrg), t_mrg = medir_mediana(merge_sort, datos)

            assert arr_ins == esperado, f"Fallo en Insertion Sort (n={n}, {tipo})"
            assert arr_mrg == esperado, f"Fallo en Merge Sort (n={n}, {tipo})"

            ganador = 'Insertion' if t_ins < t_mrg else 'Merge'
            resultados_p1.append({
                'n': n, 'tipo': tipo,
                'comp_ins': comp_ins, 'comp_mrg': comp_mrg,
                't_ins': t_ins, 't_mrg': t_mrg,
                'ganador': ganador
            })

            print(f"{n:6d} | {tipo:<10} | {comp_ins:11d} | {comp_mrg:11d} | {formato_tiempo(t_ins):>14} | {formato_tiempo(t_mrg):>14} | {ganador:<11}")

    # Guardar resultados en CSV
    ruta_csv = os.path.join(CARPETA_SALIDA, 'propuesto1_ordenamientos.csv')
    with open(ruta_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['n', 'tipo', 'comp_ins', 'comp_mrg', 't_ins_seg', 't_mrg_seg', 'ganador'])
        for r in resultados_p1:
            writer.writerow([r['n'], r['tipo'], r['comp_ins'], r['comp_mrg'], f"{r['t_ins']:.8f}", f"{r['t_mrg']:.8f}", r['ganador']])
    print(f"\n[+] Datos guardados en CSV: {ruta_csv}")

    # ------------------------------------------------------------------------
    # Gráfico 4: Global (Tiempos y Comparaciones en log-log)
    # ------------------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    colores = {'Aleatoria': '#1f77b4', 'Ordenada': '#2ca02c', 'Inversa': '#d62728'}

    for tipo in tipos_entrada:
        sub = [r for r in resultados_p1 if r['tipo'] == tipo]
        ns = [r['n'] for r in sub]
        ax1.plot(ns, [r['t_ins'] for r in sub], 'o--', color=colores[tipo], lw=1.8, label=f'Insertion ({tipo})')
        ax1.plot(ns, [r['t_mrg'] for r in sub], 's-', color=colores[tipo], lw=2.0, label=f'Merge ({tipo})')
        ax2.plot(ns, [r['comp_ins'] for r in sub], 'o--', color=colores[tipo], lw=1.8, label=f'Insertion ({tipo})')
        ax2.plot(ns, [r['comp_mrg'] for r in sub], 's-', color=colores[tipo], lw=2.0, label=f'Merge ({tipo})')

    ax1.set_xscale('log'); ax1.set_yscale('log')
    ax1.set_title('Propuesto 1: Tiempos de Ejecución (Escala log-log)', fontweight='bold')
    ax1.set_xlabel('Tamaño de entrada n (escala log)')
    ax1.set_ylabel('Tiempo mediano (s, escala log)')
    ax1.grid(True, which='both', alpha=0.3)
    ax1.legend(fontsize=9)

    ax2.set_xscale('log'); ax2.set_yscale('log')
    ax2.set_title('Propuesto 1: Comparaciones entre Claves (Escala log-log)', fontweight='bold')
    ax2.set_xlabel('Tamaño de entrada n (escala log)')
    ax2.set_ylabel('Número de comparaciones (escala log)')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend(fontsize=9)

    plt.tight_layout()
    ruta_grafico_4 = os.path.join(CARPETA_SALIDA, 'grafico_4.png')
    plt.savefig(ruta_grafico_4, dpi=200)
    print(f"[+] Gráfico global guardado en: {ruta_grafico_4}")
    plt.close()

    # ------------------------------------------------------------------------
    # Gráfico 5: Desglosado por Tipo de Entrada
    # ------------------------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))
    fig.suptitle('Propuesto 1: Comparativa Detallada de Tiempos por Tipo de Entrada', fontsize=15, fontweight='bold', y=1.02)

    for idx, tipo in enumerate(tipos_entrada):
        ax = axes[idx]
        sub = [r for r in resultados_p1 if r['tipo'] == tipo]
        ns = [r['n'] for r in sub]
        ax.plot(ns, [r['t_ins'] for r in sub], 'o-', color='#d62728', lw=2, label='Insertion Sort')
        ax.plot(ns, [r['t_mrg'] for r in sub], 's-', color='#1f77b4', lw=2, label='Merge Sort')
        ax.set_title(f'Entrada: {tipo}', fontweight='bold')
        ax.set_xlabel('Tamaño de entrada (n)')
        ax.set_ylabel('Tiempo mediano (segundos)')
        ax.grid(True, alpha=0.3)
        ax.legend()

    plt.tight_layout()
    ruta_grafico_5 = os.path.join(CARPETA_SALIDA, 'grafico_5.png')
    plt.savefig(ruta_grafico_5, dpi=200)
    print(f"[+] Gráfico desglosado guardado en: {ruta_grafico_5}")

    if mostrar_grafico:
        plt.show()

    plt.close()
    return resultados_p1

if __name__ == '__main__':
    ejecutar()
