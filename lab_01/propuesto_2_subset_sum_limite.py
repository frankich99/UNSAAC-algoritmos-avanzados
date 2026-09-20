# -*- coding: utf-8 -*-
"""
Laboratorio 01 - Algoritmos Avanzados (UNSAAC 2026-II)
Ejercicio Propuesto 2: Límite Práctico del Crecimiento Exponencial en Subset Sum
Sección 7.2 de la Guía Oficial

Requisitos:
  1. Usar semilla fija (SEMILLA_GLOBAL = 2026) y conservar las instancias en JSON.
  2. Evaluar casos con solución y sin solución rigurosos (paridad matemática).
  3. Evitar bloquear el equipo mediante límite de seguridad (LIMITE_TIEMPO_FB = 1.0 s).
  4. Registrar tiempo, resultado y métrica interna (candidatos, estados, nodos).
  5. Incluir un caso favorable y otro desfavorable para la poda con n = 20.
  6. Analizar por qué Ramificar-Podar depende de las cotas y del orden de exploración.
  7. Relacionar el crecimiento observado con el espacio de 2^n subconjuntos.
Genera:
  - propuesto2_instancias.json
  - grafico_6.png (4 subgráficos comparativos)
"""

import os
import sys
import json
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
plt.rcParams['figure.figsize'] = (18, 12)
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['font.size'] = 11

SEMILLA_GLOBAL = 2026
LIMITE_TIEMPO_FB = 1.0
LIMITE_NODOS_RP = 2_000_000
CARPETA_SALIDA = os.path.dirname(os.path.abspath(__file__))

def formato_tiempo(segundos):
    if segundos is None or math.isnan(segundos):
        return 'omitido'
    if segundos < 1e-3:
        return f"{segundos * 1e6:8.2f} us"
    if segundos < 1.0:
        return f"{segundos * 1e3:8.3f} ms"
    return f"{segundos:8.4f} s"

def medir_mediana(funcion, *args, repeticiones=3):
    tiempos = []
    resultado = None
    for _ in range(repeticiones):
        t_inicio = perf_counter()
        resultado = funcion(*args)
        t_fin = perf_counter()
        tiempos.append(t_fin - t_inicio)
    return resultado, median(tiempos)

# ----------------------------------------------------------------------------
# Algoritmos de Subset Sum exactos
# ----------------------------------------------------------------------------
def subset_sum_fuerza_bruta(valores, objetivo):
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

def subset_sum_dp(valores, objetivo):
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

def subset_sum_ramificar_podar(valores, objetivo):
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
        seleccion.append(valores[i])
        solucion = buscar(i + 1, suma + valores[i], seleccion)
        if solucion is not None:
            return solucion
        seleccion.pop()
        return buscar(i + 1, suma, seleccion)

    solucion = buscar(0, 0, [])
    return solucion is not None, solucion or [], nodos

# ----------------------------------------------------------------------------
# Generación de instancias reproducibles
# ----------------------------------------------------------------------------
def generar_instancia_subset(n, con_solucion, semilla=SEMILLA_GLOBAL):
    gen = Random(semilla * 1000 + n)
    # Todos pares: suma de subconjunto siempre será par
    valores = [2 * gen.randint(1, 200) for _ in range(n)]
    if con_solucion:
        k = max(1, n // 3)
        indices = gen.sample(range(n), k)
        objetivo = sum(valores[i] for i in indices)
        return valores, objetivo
    else:
        # Objetivo impar garantizado: matemáticamente imposible sumar impar con números pares
        objetivo = sum(valores) // 2
        if objetivo % 2 == 0:
            objetivo += 1
        return valores, objetivo

def generar_casos_poda(n, favorable, semilla=SEMILLA_GLOBAL):
    gen = Random(semilla + (7 if favorable else 13) + n)
    if favorable:
        valores = [gen.randint(1, 30) for _ in range(n)]
        valores[:3] = [5000, 4000, 3000]
        gen.shuffle(valores)
        objetivo = 12000
        return valores, objetivo
    else:
        valores = [2 * gen.randint(100, 110) for _ in range(n)]
        objetivo = sum(valores) // 2
        if objetivo % 2 == 0:
            objetivo += 1
        return valores, objetivo

# ----------------------------------------------------------------------------
# Ejecución del experimento
# ----------------------------------------------------------------------------
def ejecutar(mostrar_grafico=False):
    print("=" * 105)
    print(" EJERCICIO PROPUESTO 2: LÍMITE PRÁCTICO DEL CRECIMIENTO EXPONENCIAL (SUBSET SUM)")
    print("=" * 105)

    tamanos_p2 = list(range(8, 27, 2))
    resultados_p2 = []
    instancias_guardadas = {}
    fb_activa = True
    limite_practico_fb = None

    print(f"{'n':>4} | {'Caso':<13} | {'Candidatos FB':>13} | {'T. FB':>12} | {'Estados DP':>11} | {'T. DP':>12} | {'Nodos RP':>11} | {'T. RP':>12}")
    print("-" * 105)

    for n in tamanos_p2:
        for con_solucion in (True, False):
            etiqueta = 'con_solucion' if con_solucion else 'sin_solucion'
            vals, obj = generar_instancia_subset(n, con_solucion)
            instancias_guardadas[f"n{n}_{etiqueta}"] = {'valores': vals, 'objetivo': obj}

            if fb_activa:
                (res_fb, sel_fb, w_fb), t_fb = medir_mediana(
                    subset_sum_fuerza_bruta, vals, obj, repeticiones=1 if n >= 20 else 3
                )
                assert not res_fb or sum(sel_fb) == obj
                if not con_solucion and t_fb > LIMITE_TIEMPO_FB:
                    limite_practico_fb = n
                    fb_activa = False
            else:
                w_fb, t_fb = None, float('nan')

            (res_dp, sel_dp, w_dp), t_dp = medir_mediana(subset_sum_dp, vals, obj, repeticiones=3)
            assert not res_dp or sum(sel_dp) == obj
            assert res_dp == con_solucion

            (res_rp, sel_rp, w_rp), t_rp = medir_mediana(subset_sum_ramificar_podar, vals, obj, repeticiones=3)
            assert not res_rp or sum(sel_rp) == obj
            assert res_rp == con_solucion

            resultados_p2.append({
                'n': n, 'caso': etiqueta, 'con_solucion': con_solucion,
                'w_fb': w_fb, 't_fb': t_fb,
                'w_dp': w_dp, 't_dp': t_dp,
                'w_rp': w_rp, 't_rp': t_rp
            })

            w_fb_str = f"{w_fb:13,d}" if w_fb is not None else "---"
            t_fb_str = formato_tiempo(t_fb) if not math.isnan(t_fb) else "> limite"

            print(f"{n:4d} | {etiqueta:<13} | {w_fb_str:>13} | {t_fb_str:>12} | {w_dp:11,d} | {formato_tiempo(t_dp):>12} | {w_rp:11,d} | {formato_tiempo(t_rp):>12}")

    print(f"\n[+] Limite practico alcanzado por Fuerza Bruta: n = {limite_practico_fb} (supero {LIMITE_TIEMPO_FB} s).")
    print("    Programacion Dinamica y Ramificar-Podar completaron satisfactoriamente hasta n = 26.")

    # Guardar instancias en JSON
    ruta_json = os.path.join(CARPETA_SALIDA, 'propuesto2_instancias.json')
    with open(ruta_json, 'w', encoding='utf-8') as f:
        json.dump({'semilla': SEMILLA_GLOBAL, 'instancias': instancias_guardadas}, f, indent=2)
    print(f"[+] Instancias experimentales guardadas en: {ruta_json}")

    # ------------------------------------------------------------------------
    # Evaluación: Caso Favorable vs Caso Desfavorable para la Poda
    # ------------------------------------------------------------------------
    n_poda_test = 20
    print(f"\n[+] Comparacion de Podas con n = {n_poda_test} (Espacio total: 2^{n_poda_test} = {2**n_poda_test:,} subconjuntos)")
    print("-" * 95)

    res_poda_list = []
    for favorable in (True, False):
        etiqueta = 'Favorable' if favorable else 'Desfavorable'
        vals_p, obj_p = generar_casos_poda(n_poda_test, favorable)
        (res_rp, sel_rp, nodos_rp), t_rp = medir_mediana(subset_sum_ramificar_podar, vals_p, obj_p)
        (res_dp, sel_dp, estados_dp), t_dp = medir_mediana(subset_sum_dp, vals_p, obj_p)
        fraccion = nodos_rp / (2**(n_poda_test + 1) - 1)
        res_poda_list.append({
            'caso': etiqueta, 'nodos_rp': nodos_rp, 't_rp': t_rp,
            'estados_dp': estados_dp, 't_dp': t_dp, 'fraccion': fraccion
        })
        print(f"Caso {etiqueta:<13} | Nodos B&B: {nodos_rp:9,d} | T. B&B: {formato_tiempo(t_rp):>12} | Fraccion arbol: {fraccion:.2e} | Estados DP: {estados_dp:9,d}")

    # ------------------------------------------------------------------------
    # Generación de Gráfico 6 (2x2)
    # ------------------------------------------------------------------------
    fig, axes = plt.subplots(2, 2, figsize=(18, 12))

    # 1. Peor Caso (Sin Solución)
    ax1 = axes[0, 0]
    sub_sin = [r for r in resultados_p2 if not r['con_solucion']]
    ns_sin = [r['n'] for r in sub_sin]
    ns_fb = [r['n'] for r in sub_sin if not math.isnan(r['t_fb'])]
    ts_fb = [r['t_fb'] for r in sub_sin if not math.isnan(r['t_fb'])]

    ax1.plot(ns_fb, ts_fb, 'o-', color='#d62728', lw=2, label='Fuerza Bruta')
    ax1.plot(ns_sin, [r['t_dp'] for r in sub_sin], 's-', color='#1f77b4', lw=2, label='Programación Dinámica')
    ax1.plot(ns_sin, [r['t_rp'] for r in sub_sin], '^-', color='#2ca02c', lw=2, label='Ramificar y Podar')
    ax1.axhline(LIMITE_TIEMPO_FB, color='black', linestyle='--', alpha=0.6, label=f'Límite seguro ({LIMITE_TIEMPO_FB}s)')
    ax1.set_yscale('log')
    ax1.set_title('Subset Sum: Tiempo en el Peor Caso (Sin Solución)', fontweight='bold')
    ax1.set_xlabel('Tamaño de entrada (n)')
    ax1.set_ylabel('Tiempo mediano (s, escala log)')
    ax1.grid(True, which='both', alpha=0.3)
    ax1.legend()

    # 2. Con Solución Presente
    ax2 = axes[0, 1]
    sub_con = [r for r in resultados_p2 if r['con_solucion']]
    ns_con = [r['n'] for r in sub_con]
    ns_fb_c = [r['n'] for r in sub_con if not math.isnan(r['t_fb'])]
    ts_fb_c = [r['t_fb'] for r in sub_con if not math.isnan(r['t_fb'])]

    ax2.plot(ns_fb_c, ts_fb_c, 'o-', color='#d62728', lw=2, label='Fuerza Bruta')
    ax2.plot(ns_con, [r['t_dp'] for r in sub_con], 's-', color='#1f77b4', lw=2, label='Programación Dinámica')
    ax2.plot(ns_con, [r['t_rp'] for r in sub_con], '^-', color='#2ca02c', lw=2, label='Ramificar y Podar')
    ax2.set_yscale('log')
    ax2.set_title('Subset Sum: Tiempo con Solución Presente', fontweight='bold')
    ax2.set_xlabel('Tamaño de entrada (n)')
    ax2.set_ylabel('Tiempo mediano (s, escala log)')
    ax2.grid(True, which='both', alpha=0.3)
    ax2.legend()

    # 3. Trabajo Interno vs Espacio 2^n
    ax3 = axes[1, 0]
    ax3.plot(ns_fb, [r['w_fb'] for r in sub_sin if r['w_fb'] is not None], 'o-', color='#d62728', lw=2, label='Candidatos (F. Bruta)')
    ax3.plot(ns_sin, [r['w_dp'] for r in sub_sin], 's-', color='#1f77b4', lw=2, label='Estados (DP)')
    ax3.plot(ns_sin, [r['w_rp'] for r in sub_sin], '^-', color='#2ca02c', lw=2, label='Nodos (B&B)')
    ax3.plot(ns_sin, [2**n for n in ns_sin], 'k--', alpha=0.5, label=r'Cota teórica $2^n$')
    ax3.set_yscale('log')
    ax3.set_title(r'Trabajo Interno vs Espacio de $2^n$ Subconjuntos', fontweight='bold')
    ax3.set_xlabel('Tamaño de entrada (n)')
    ax3.set_ylabel('Unidades de trabajo interno (escala log)')
    ax3.grid(True, which='both', alpha=0.3)
    ax3.legend()

    # 4. Bar chart de Efectividad de Podas (n = 20)
    ax4 = axes[1, 1]
    etiquetas_poda = [r['caso'] for r in res_poda_list]
    nodos_poda = [r['nodos_rp'] for r in res_poda_list]
    bars = ax4.bar(etiquetas_poda, nodos_poda, color=['#2ca02c', '#d62728'], width=0.5)
    ax4.axhline(2**n_poda_test, color='black', linestyle='--', label=f'Espacio total $2^{{20}} = {2**n_poda_test:,}$')
    ax4.set_yscale('log')
    ax4.set_title(f'Efectividad de Podas: Nodos en B&B (n = {n_poda_test})', fontweight='bold')
    ax4.set_ylabel('Nodos explorados (escala log)')
    ax4.grid(True, which='both', alpha=0.3)
    ax4.legend()
    for bar in bars:
        yval = bar.get_height()
        ax4.text(bar.get_x() + bar.get_width()/2.0, yval * 1.5, f'{int(yval):,}', ha='center', va='bottom', fontweight='bold')

    plt.tight_layout()
    ruta_grafico_6 = os.path.join(CARPETA_SALIDA, 'grafico_6.png')
    plt.savefig(ruta_grafico_6, dpi=200)
    print(f"\n[+] Gráfico de 4 paneles guardado exitosamente en: {ruta_grafico_6}")

    if mostrar_grafico:
        plt.show()

    plt.close()

if __name__ == '__main__':
    ejecutar()
