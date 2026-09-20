# -*- coding: utf-8 -*-
"""
Laboratorio 01 - Algoritmos Avanzados (UNSAAC 2026-II)
Ejercicio Resuelto 1: Crecimiento Lineal y Cuadrático
Listing 1 de la Guía Oficial

Compara:
  - suma_lineal: O(n)
  - contar_pares_ordenados: Θ(n^2)
Genera:
  - grafico_1.png (Escala lineal y escala log-log)
"""

import os
import sys
import math
from random import Random
from statistics import median
from time import perf_counter
import matplotlib
# Configurar backend no interactivo para entornos sin servidor gráfico / batch
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Configuración visual
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (15, 6)
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
        return f'{segundos * 1e6:8.2f} µs'
    if segundos < 1.0:
        return f'{segundos * 1e3:8.3f} ms'
    return f'{segundos:8.4f} s'

def medir_mediana(funcion, *args, repeticiones=REPETICIONES):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        t_inicio = perf_counter()
        resultado = funcion(*args)
        t_fin = perf_counter()
        tiempos.append(t_fin - t_inicio)
    return resultado, median(tiempos)

def suma_lineal(datos):
    """Suma todos los elementos de la lista en tiempo O(n)."""
    total = 0
    for valor in datos:
        total += valor
    return total

def contar_pares_ordenados(datos):
    """Cuenta pares (i, j) con i < j tales que datos[i] <= datos[j] en tiempo Θ(n^2)."""
    contador = 0
    n = len(datos)
    for i in range(n):
        for j in range(i + 1, n):
            if datos[i] <= datos[j]:
                contador += 1
    return contador

def ejecutar(mostrar_grafico=False):
    print("=" * 80)
    print(" EJERCICIO RESUELTO 1: CRECIMIENTO LINEAL Y CUADRÁTICO (Listing 1)")
    print("=" * 80)

    generador = Random(SEMILLA_GLOBAL)
    tamanos_r1 = [100, 500, 1000, 2000, 4000]

    print(f"{'n':>6} | {'T. Lineal O(n)':>15} | {'T. Cuadrático O(n²)':>20} | {'Factor Lin.':>12} | {'Factor Cuad.':>13}")
    print("-" * 75)

    tiempos_r1_lin = []
    tiempos_r1_cuad = []
    t_lin_ant = t_cuad_ant = None

    for n in tamanos_r1:
        datos = [generador.randint(1, 10_000) for _ in range(n)]
        _, t1 = medir_mediana(suma_lineal, datos)
        _, t2 = medir_mediana(contar_pares_ordenados, datos)

        tiempos_r1_lin.append(t1)
        tiempos_r1_cuad.append(t2)

        f_lin = f"x{t1/t_lin_ant:.2f}" if t_lin_ant else "-"
        f_cuad = f"x{t2/t_cuad_ant:.2f}" if t_cuad_ant else "-"

        print(f"{n:6d} | {formato_tiempo(t1):>15} | {formato_tiempo(t2):>20} | {f_lin:>12} | {f_cuad:>13}")
        t_lin_ant, t_cuad_ant = t1, t2

    # Generar gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Escala lineal
    ax1.plot(tamanos_r1, tiempos_r1_lin, 'o-', color='#1f77b4', lw=2, label='Suma lineal O(n)')
    ax1.plot(tamanos_r1, tiempos_r1_cuad, 's-', color='#d62728', lw=2, label='Contar pares O(n²)')
    ax1.set_title('Resuelto 1: Tiempo vs n (Escala lineal)', fontweight='bold')
    ax1.set_xlabel('Tamaño de entrada (n)')
    ax1.set_ylabel('Tiempo mediano (segundos)')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Escala log-log
    ax2.plot(tamanos_r1, tiempos_r1_lin, 'o-', color='#1f77b4', lw=2, label='Suma lineal (pendiente ≈ 1)')
    ax2.plot(tamanos_r1, tiempos_r1_cuad, 's-', color='#d62728', lw=2, label='Contar pares (pendiente ≈ 2)')
    ax2.set_xscale('log')
    ax2.set_yscale('log')
    ax2.set_title('Resuelto 1: Pendiente Asintótica (Escala Log-Log)', fontweight='bold')
    ax2.set_xlabel('Tamaño de entrada n (escala log)')
    ax2.set_ylabel('Tiempo mediano (s, escala log)')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    ruta_grafico = os.path.join(CARPETA_SALIDA, 'grafico_1.png')
    plt.savefig(ruta_grafico, dpi=200)
    print(f"\n[+] Gráfico guardado exitosamente en: {ruta_grafico}")

    if mostrar_grafico:
        plt.show()

    plt.close()

if __name__ == '__main__':
    ejecutar()
