# -*- coding: utf-8 -*-
"""
Laboratorio 01 - Algoritmos Avanzados (UNSAAC 2026-II)
Ejercicio Resuelto 2: Búsqueda Lineal y Binaria Instrumentadas
Listing 2 de la Guía Oficial

Compara:
  - busqueda_lineal: O(n) comparaciones
  - busqueda_binaria: O(log n) comparaciones (⌊log2 n⌋ + 1 en peor caso)
Genera:
  - grafico_2.png (Escala lineal y escala semilogarítmica)
"""

import os
import sys
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['figure.figsize'] = (15, 6)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['font.size'] = 11

# Asegurar compatibilidad UTF-8 en consola de Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

CARPETA_SALIDA = os.path.dirname(os.path.abspath(__file__))

def busqueda_lineal(datos, objetivo):
    """
    Búsqueda secuencial en lista.
    Retorna (índice, comparaciones).
    """
    comparaciones = 0
    for indice, valor in enumerate(datos):
        comparaciones += 1
        if valor == objetivo:
            return indice, comparaciones
    return -1, comparaciones

def busqueda_binaria(datos, objetivo):
    """
    Búsqueda dicotómica en lista ordenada.
    Retorna (índice, comparaciones).
    """
    izquierda = 0
    derecha = len(datos) - 1
    comparaciones = 0
    while izquierda <= derecha:
        medio = (izquierda + derecha) // 2
        comparaciones += 1
        if datos[medio] == objetivo:
            return medio, comparaciones
        if datos[medio] < objetivo:
            izquierda = medio + 1
        else:
            derecha = medio - 1
    return -1, comparaciones

def ejecutar(mostrar_grafico=False):
    print("=" * 80)
    print(" EJERCICIO RESUELTO 2: BÚSQUEDAS INSTRUMENTADAS (Listing 2)")
    print("=" * 80)

    tamanos_r2 = [16, 32, 64, 128, 256, 512, 1024]

    print(f"{'n':>6} | {'Comp. Lineal':>14} | {'Comp. Binaria':>15} | {'Cota Teórica floor(lg n)+1':>28} | {'Ahorro Factor':>15}")
    print("-" * 88)

    comp_lineales = []
    comp_binarias = []

    for n in tamanos_r2:
        datos = list(range(n))
        objetivo = n + 1  # Elemento ausente para forzar el peor caso
        idx_lin, lin = busqueda_lineal(datos, objetivo)
        idx_bin, bin_ = busqueda_binaria(datos, objetivo)
        assert idx_lin == -1 and idx_bin == -1, 'Error: elemento ausente encontrado'

        comp_lineales.append(lin)
        comp_binarias.append(bin_)
        cota = math.floor(math.log2(n)) + 1
        ahorro = f"{lin / bin_:.1f}x"
        print(f"{n:6d} | {lin:14d} | {bin_:15d} | {cota:25d} | {ahorro:>15}")

    # Generar gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

    # Escala lineal
    ax1.plot(tamanos_r2, comp_lineales, 'o-', color='#d62728', lw=2, label='Búsqueda lineal (n)')
    ax1.plot(tamanos_r2, comp_binarias, 's-', color='#2ca02c', lw=2, label=r'Búsqueda binaria ($\lfloor\log_2 n\rfloor + 1$)')
    ax1.set_title('Resuelto 2: Comparaciones vs n (Escala lineal)', fontweight='bold')
    ax1.set_xlabel('Tamaño de entrada (n)')
    ax1.set_ylabel('Número de comparaciones')
    ax1.grid(True, alpha=0.3)
    ax1.legend()

    # Escala semilogarítmica en X
    ax2.plot(tamanos_r2, comp_lineales, 'o-', color='#d62728', lw=2, label='Búsqueda lineal O(n)')
    ax2.plot(tamanos_r2, comp_binarias, 's-', color='#2ca02c', lw=2, label='Búsqueda binaria O(log n)')
    ax2.set_xscale('log')
    ax2.set_title('Resuelto 2: Comparaciones vs n (Eje X logarítmico)', fontweight='bold')
    ax2.set_xlabel(r'Tamaño de entrada n (escala $\log_2$)')
    ax2.set_ylabel('Número de comparaciones')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    ruta_grafico = os.path.join(CARPETA_SALIDA, 'grafico_2.png')
    plt.savefig(ruta_grafico, dpi=200)
    print(f"\n[+] Gráfico guardado exitosamente en: {ruta_grafico}")

    if mostrar_grafico:
        plt.show()

    plt.close()

if __name__ == '__main__':
    ejecutar()
