# -*- coding: utf-8 -*-
"""
Laboratorio 01 - Algoritmos Avanzados (UNSAAC 2026-II)
Ejercicio Resuelto 3: Subset Sum mediante Tres Estrategias Exactas
Listings 3, 4, 5 y 6 de la Guía Oficial

Estrategias exactas:
  1. Fuerza Bruta (evalúa 2^n combinaciones) -> Métrica: Candidatos
  2. Programación Dinámica (subproblemas alcanzables) -> Métrica: Estados
  3. Ramificar y Podar (Branch & Bound con cotas) -> Métrica: Nodos
Genera:
  - grafico_3.png (Tiempo vs n y Trabajo Interno vs n en escala logarítmica)
"""

import os
import sys
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
CARPETA_SALIDA = os.path.dirname(os.path.abspath(__file__))

def medir_mediana(funcion, *args, repeticiones=3):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        t_inicio = perf_counter()
        resultado = funcion(*args)
        t_fin = perf_counter()
        tiempos.append(t_fin - t_inicio)
    return resultado, median(tiempos)

def formato_tiempo(segundos):
    if segundos is None or math.isnan(segundos):
        return 'omitido'
    if segundos < 1e-3:
        return f"{segundos * 1e6:8.2f} us"
    if segundos < 1.0:
        return f"{segundos * 1e3:8.3f} ms"
    return f"{segundos:8.4f} s"

# ----------------------------------------------------------------------------
# Listing 3: Fuerza Bruta
# ----------------------------------------------------------------------------
def subset_sum_fuerza_bruta(valores, objetivo):
    """
    Evalúa sistemáticamente el espacio de 2^n subconjuntos usando máscaras binarias.
    Métrica contada: candidatos evaluados.
    """
    n = len(valores)
    candidatos = 0
    for mascara in range(1 << n):
        candidatos += 1
        suma = 0
        seleccion = []
        for i in range(n):
            if mascara & (1 << i):
                suma += valores[i]
                seleccion.append(valores[i])
        if suma == objetivo:
            return True, seleccion, candidatos
    return False, [], candidatos

# ----------------------------------------------------------------------------
# Listing 4: Programación Dinámica
# ----------------------------------------------------------------------------
def subset_sum_dp(valores, objetivo):
    """
    Construye las sumas alcanzables mediante una tabla/diccionario de estados.
    Métrica contada: transiciones de estados evaluadas.
    """
    alcanzable = {0: []}
    estados = 0
    for valor in valores:
        nuevos = dict(alcanzable)
        for suma, seleccion in alcanzable.items():
            estados += 1
            nueva_suma = suma + valor
            if nueva_suma <= objetivo and nueva_suma not in nuevos:
                nuevos[nueva_suma] = seleccion + [valor]
        alcanzable = nuevos
        if objetivo in alcanzable:
            return True, alcanzable[objetivo], estados
    return False, [], estados

# ----------------------------------------------------------------------------
# Listing 5: Ramificar y Podar (Branch & Bound)
# ----------------------------------------------------------------------------
def subset_sum_ramificar_podar(valores, objetivo):
    """
    Explora el árbol de decisiones binario ordenado decrecientemente con 2 cotas:
      1. Cota de exceso: suma > objetivo
      2. Cota optimista restante: suma + restante[i] < objetivo
    Métrica contada: nodos visitados en el árbol de búsqueda.
    """
    valores = sorted(valores, reverse=True)
    n = len(valores)
    restante = [0] * (n + 1)
    for i in range(n - 1, -1, -1):
        restante[i] = restante[i + 1] + valores[i]
    nodos = 0

    def buscar(i, suma, seleccion):
        nonlocal nodos
        nodos += 1
        if suma == objetivo:
            return seleccion.copy()
        if i == n or suma > objetivo:
            return None
        if suma + restante[i] < objetivo:
            return None
        # Rama 1: Incluir valores[i]
        seleccion.append(valores[i])
        solucion = buscar(i + 1, suma + valores[i], seleccion)
        if solucion is not None:
            return solucion
        # Backtracking
        seleccion.pop()
        # Rama 2: Excluir valores[i]
        return buscar(i + 1, suma, seleccion)

    solucion = buscar(0, 0, [])
    return solucion is not None, solucion or [], nodos

# ----------------------------------------------------------------------------
# Ejecución y Pruebas
# ----------------------------------------------------------------------------
def ejecutar(mostrar_grafico=False):
    print("=" * 88)
    print(" EJERCICIO RESUELTO 3: SUBSET SUM MEDIANTE TRES ESTRATEGIAS EXACTAS")
    print("=" * 88)

    # 1. Prueba oficial de la guía (Listing 6)
    valores_oficiales = [3, 7, 11, 13, 17, 19, 23, 29]
    objetivo_oficial = 42

    print(f"\n[1] Instancia oficial de la Guia: valores = {valores_oficiales}, objetivo = {objetivo_oficial}")
    print(f"{'Algoritmo':<30} | {'Existe':>7} | {'Selección':<20} | {'Métrica':<12} | {'Trabajo':>8}")
    print("-" * 88)

    metricas = {
        'subset_sum_fuerza_bruta': 'candidatos',
        'subset_sum_dp': 'estados',
        'subset_sum_ramificar_podar': 'nodos'
    }

    for algoritmo in [subset_sum_fuerza_bruta, subset_sum_dp, subset_sum_ramificar_podar]:
        existe, seleccion, trabajo = algoritmo(valores_oficiales, objetivo_oficial)
        assert not existe or sum(seleccion) == objetivo_oficial, 'Error: la selección no suma el objetivo'
        met = metricas[algoritmo.__name__]
        print(f"{algoritmo.__name__:<30} | {str(existe):>7} | {str(sorted(seleccion)):<20} | {met:<12} | {trabajo:8d}")

    # 2. Experimento comparativo de escalado temporal y trabajo interno
    print("\n[2] Experimento de escalado asintótico (n de 8 a 20)...")
    gen_r3 = Random(SEMILLA_GLOBAL)
    tamanos_r3 = [8, 10, 12, 14, 16, 18, 20]
    t_fb_list, t_dp_list, t_rp_list = [], [], []
    w_fb_list, w_dp_list, w_rp_list = [], [], []

    print(f"{'n':>4} | {'T. FB':>12} | {'Candidatos':>11} | {'T. DP':>12} | {'Estados':>10} | {'T. B&B':>12} | {'Nodos':>10}")
    print("-" * 88)

    for n in tamanos_r3:
        vals = [gen_r3.randint(1, 100) for _ in range(n)]
        obj = sum(vals[:n//3])  # Solución garantizada
        _, t_fb = medir_mediana(subset_sum_fuerza_bruta, vals, obj, repeticiones=3)
        _, t_dp = medir_mediana(subset_sum_dp, vals, obj, repeticiones=3)
        _, t_rp = medir_mediana(subset_sum_ramificar_podar, vals, obj, repeticiones=3)
        _, _, w_fb = subset_sum_fuerza_bruta(vals, obj)
        _, _, w_dp = subset_sum_dp(vals, obj)
        _, _, w_rp = subset_sum_ramificar_podar(vals, obj)

        t_fb_list.append(t_fb); w_fb_list.append(w_fb)
        t_dp_list.append(t_dp); w_dp_list.append(w_dp)
        t_rp_list.append(t_rp); w_rp_list.append(w_rp)

        print(f"{n:4d} | {formato_tiempo(t_fb):>12} | {w_fb:11,d} | {formato_tiempo(t_dp):>12} | {w_dp:10,d} | {formato_tiempo(t_rp):>12} | {w_rp:10,d}")

    # 3. Generación de gráficos
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

    ax1.plot(tamanos_r3, t_fb_list, 'o-', color='#d62728', lw=2, label='Fuerza Bruta')
    ax1.plot(tamanos_r3, t_dp_list, 's-', color='#1f77b4', lw=2, label='Programación Dinámica')
    ax1.plot(tamanos_r3, t_rp_list, '^-', color='#2ca02c', lw=2, label='Ramificar y Podar')
    ax1.set_yscale('log')
    ax1.set_title('Resuelto 3: Tiempo vs Tamaño n (Escala log)', fontweight='bold')
    ax1.set_xlabel('Tamaño de entrada (n)')
    ax1.set_ylabel('Tiempo mediano (s, escala log)')
    ax1.grid(True, which='both', alpha=0.3)
    ax1.legend()

    ax2.plot(tamanos_r3, w_fb_list, 'o-', color='#d62728', lw=2, label='Candidatos (F. Bruta)')
    ax2.plot(tamanos_r3, w_dp_list, 's-', color='#1f77b4', lw=2, label='Estados (DP)')
    ax2.plot(tamanos_r3, w_rp_list, '^-', color='#2ca02c', lw=2, label='Nodos (B&B)')
    ax2.plot(tamanos_r3, [2**n for n in tamanos_r3], '--', color='black', alpha=0.5, label=r'Cota teórica $2^n$')
    ax2.set_yscale('log')
    ax2.set_title('Resuelto 3: Trabajo Interno vs Tamaño n (Escala log)', fontweight='bold')
    ax2.set_xlabel('Tamaño de entrada (n)')
    ax2.set_ylabel('Cantidad de operaciones (escala log)')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend()

    plt.tight_layout()
    ruta_grafico = os.path.join(CARPETA_SALIDA, 'grafico_3.png')
    plt.savefig(ruta_grafico, dpi=200)
    print(f"\n[+] Gráfico guardado exitosamente en: {ruta_grafico}")

    if mostrar_grafico:
        plt.show()

    plt.close()

if __name__ == '__main__':
    ejecutar()
