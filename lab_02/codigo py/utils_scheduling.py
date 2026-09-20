# -*- coding: utf-8 -*-
"""
Módulo de utilidades y algoritmos para Scheduling en Máquinas Paralelas Idénticas (Pm || Cmax).
Laboratorio 02 - Algoritmos Avanzados - UNSAAC.

Contiene:
  - Validación y métricas: validar_instancia, cargas, makespan, es_factible, cota_inferior.
  - Heurísticas de aproximación: list_scheduling (min-heap O(n log m)), lpt.
  - Método exacto: branch_and_bound (Ramificar y Podar con podas por LB y ruptura de simetrías).
  - Casos teóricos de peor caso: instancia_ajustada_ls, instancia_ajustada_lpt.
  - Generador reproducible de instancias (familias uniforme, estrecha, sesgada, grande).
  - Métricas de calidad y garantías: garantia_ls, garantia_lpt, respeta_garantia_ls, respeta_garantia_lpt.
  - Utilidades de experimentación: medir_mediana, formato_tiempo, mostrar_tabla, guardar_csv, guardar_figura.
"""

import csv
import heapq
import json
import math
import os
import platform
import sys
from collections import Counter
from itertools import permutations
from math import ceil
from random import Random
from statistics import mean, median
from time import perf_counter

import matplotlib
import matplotlib.pyplot as plt

# pandas para formateo de tablas si está instalado
try:
    import pandas as pd
    from IPython.display import display
    HAY_PANDAS = True
except ImportError:
    HAY_PANDAS = False

# Rutas de almacenamiento locales al directorio del script
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
CARPETA_FIGURAS = os.path.join(BASE_DIR, "figuras")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)
os.makedirs(CARPETA_FIGURAS, exist_ok=True)

# Semilla única global para reproducibilidad
SEMILLA_GLOBAL = 2026
REPETICIONES = 7

# Paleta y estilo de gráficos
COLOR = {"LS": "#2a78d6", "LPT": "#eb6834", "BB": "#1baf7a"}
MARCADOR = {"LS": "o", "LPT": "s", "BB": "^"}
TINTA = "#0b0b0b"
TINTA_SECUNDARIA = "#52514e"
TINTA_TENUE = "#898781"
CUADRICULA = "#e1e0d9"
EJE = "#c3c2b7"

plt.rcParams.update({
    "figure.dpi": 110,
    "savefig.dpi": 150,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "axes.edgecolor": EJE,
    "axes.linewidth": 0.8,
    "axes.labelcolor": TINTA_SECUNDARIA,
    "axes.titlecolor": TINTA,
    "axes.titlesize": 11,
    "axes.titleweight": "bold",
    "axes.labelsize": 10,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.color": CUADRICULA,
    "grid.linewidth": 0.8,
    "grid.linestyle": "-",
    "xtick.color": TINTA_TENUE,
    "ytick.color": TINTA_TENUE,
    "xtick.labelcolor": TINTA_SECUNDARIA,
    "ytick.labelcolor": TINTA_SECUNDARIA,
    "legend.frameon": False,
    "legend.fontsize": 9,
    "lines.linewidth": 2,
    "lines.markersize": 6,
    "font.size": 10,
})


# ============================================================================
# 1. Validación y cotas
# ============================================================================

def validar_instancia(trabajos, m):
    """Rechaza entradas que no pertenecen al problema Pm || Cmax."""
    if not isinstance(m, int) or m <= 0:
        raise ValueError("El numero de maquinas debe ser un entero positivo")
    for p in trabajos:
        if not isinstance(p, int) or p <= 0:
            raise ValueError("Cada tiempo de proceso debe ser un entero positivo: %r" % (p,))


def cargas(planificacion):
    """L_i = suma de los tiempos asignados a la máquina i."""
    return [sum(maquina) for maquina in planificacion]


def makespan(planificacion):
    """Cmax = máxima carga. default=0 cubre el caso sin máquinas/trabajos."""
    return max(cargas(planificacion), default=0)


def es_factible(trabajos, planificacion, m):
    """
    Una planificación es factible si:
      1) tiene exactamente m máquinas;
      2) cada trabajo aparece exactamente una vez (usando Counter para soportar repetidos).
    """
    if len(planificacion) != m:
        return False
    asignados = [p for maquina in planificacion for p in maquina]
    return Counter(asignados) == Counter(trabajos)


def cota_inferior(trabajos, m):
    """
    LB = max( ceil(sum p_j / m), max p_j ) <= OPT
    Aritmética entera (-(-a // b) == ceil(a / b)) para evitar imprecisión de float.
    """
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")
    if not trabajos:
        return 0
    return max(-(-sum(trabajos) // m), max(trabajos))


# ============================================================================
# 2. Algoritmos de aproximación
# ============================================================================

def list_scheduling(trabajos, m):
    """
    List Scheduling: asigna cada trabajo en el orden recibido a la máquina de menor carga.
    Usa min-heap con tuplas (carga, id_maquina): O(n log m).
    Devuelve (planificacion, makespan).
    """
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")

    planificacion = [[] for _ in range(m)]
    heap = [(0, i) for i in range(m)]
    heapq.heapify(heap)

    for trabajo in trabajos:
        carga, maquina = heap[0]
        planificacion[maquina].append(trabajo)
        heapq.heapreplace(heap, (carga + trabajo, maquina))

    return planificacion, max(carga for carga, _ in heap)


def lpt(trabajos, m):
    """
    Longest Processing Time first: ordena de mayor a menor y aplica List Scheduling.
    Costo O(n log n) + O(n log m).
    """
    ordenados = sorted(trabajos, reverse=True)
    return list_scheduling(ordenados, m)


# ============================================================================
# 3. Método exacto: Ramificar y Podar (Branch and Bound)
# ============================================================================

class LimiteNodosExcedido(Exception):
    """Tope de seguridad para evitar bloqueos en instancias complejas."""
    def __init__(self, nodos):
        super().__init__("Limite de nodos excedido (%d nodos)" % nodos)
        self.nodos = nodos


def branch_and_bound(trabajos, m, limite_nodos=None):
    """
    Calcula una planificación ÓPTIMA mediante Branch and Bound.
    Devuelve (mejor_plan, mejor_makespan, nodos_explorados).
    """
    if m <= 0:
        raise ValueError("El numero de maquinas debe ser positivo")

    trabajos = sorted(trabajos, reverse=True)
    n = len(trabajos)
    mejor_plan, mejor_valor = lpt(trabajos, m)
    cargas_actuales = [0] * m
    plan_actual = [[] for _ in range(m)]
    nodos = 0

    cota_promedio = -(-sum(trabajos) // m)

    def buscar(k):
        nonlocal mejor_plan, mejor_valor, nodos
        nodos += 1
        if limite_nodos is not None and nodos > limite_nodos:
            raise LimiteNodosExcedido(nodos)

        if k == n:
            valor = max(cargas_actuales, default=0)
            if valor < mejor_valor:
                mejor_valor = valor
                mejor_plan = [x.copy() for x in plan_actual]
            return

        trabajo = trabajos[k]
        cargas_probadas = set()

        for i in range(m):
            # Ruptura de simetría: no repetir máquinas con idéntica carga
            if cargas_actuales[i] in cargas_probadas:
                continue
            cargas_probadas.add(cargas_actuales[i])

            nueva_carga = cargas_actuales[i] + trabajo
            if nueva_carga >= mejor_valor:
                continue

            cargas_actuales[i] = nueva_carga
            plan_actual[i].append(trabajo)

            restante_mas_largo = trabajos[k + 1] if k + 1 < n else 0
            lb = max(max(cargas_actuales), cota_promedio, restante_mas_largo)
            if lb < mejor_valor:
                buscar(k + 1)

            plan_actual[i].pop()
            cargas_actuales[i] -= trabajo

            # Si se exploró una máquina vacía, todas las demás vacías son simétricas
            if nueva_carga == trabajo:
                break

    # Si LPT ya alcanza la cota inferior global, es óptimo demostrado (0 nodos)
    if mejor_valor == cota_inferior(trabajos, m):
        return mejor_plan, mejor_valor, nodos

    buscar(0)
    return mejor_plan, mejor_valor, nodos


# ============================================================================
# 4. Instancias ajustadas (casos teóricos de peor caso)
# ============================================================================

def instancia_ajustada_ls(m):
    """
    Instancia ajustada de Graham para List Scheduling:
    m(m - 1) trabajos de duración 1 seguidos de 1 trabajo de duración m.
    Makespan LS = 2m - 1, OPT = m -> r = 2 - 1/m.
    """
    return [1] * (m * (m - 1)) + [m]


def instancia_ajustada_lpt(m):
    """
    Instancia ajustada para LPT:
    Dos trabajos de cada duración 2m-1, ..., m+1 y tres trabajos de duración m (2m+1 trabajos).
    Makespan LPT = 4m - 1, OPT = 3m -> r = 4/3 - 1/(3m).
    """
    trabajos = []
    for p in range(2 * m - 1, m, -1):
        trabajos += [p, p]
    return trabajos + [m, m, m]


# ============================================================================
# 5. Generador reproducible de instancias
# ============================================================================

FAMILIAS = ("uniforme", "estrecha", "sesgada")

def generar_trabajos(n, familia, semilla):
    """Genera n duraciones de trabajos según la familia de distribución."""
    generador = Random(semilla)
    if familia == "uniforme":
        return [generador.randint(1, 20) for _ in range(n)]
    if familia == "estrecha":
        return [generador.randint(10, 20) for _ in range(n)]
    if familia == "sesgada":
        return [generador.randint(1, 5) if generador.random() < 0.75
                else generador.randint(15, 30) for _ in range(n)]
    if familia == "grande":
        return [generador.randint(1, 100) for _ in range(n)]
    raise ValueError("Familia desconocida: " + familia)


# ============================================================================
# 6. Garantías teóricas y verificación
# ============================================================================

def garantia_ls(m):
    return 2.0 - 1.0 / m


def garantia_lpt(m):
    return 4.0 / 3.0 - 1.0 / (3.0 * m)


def respeta_garantia_ls(c, opt, m):
    # m * C_LS <= (2m - 1) * OPT
    return m * c <= (2 * m - 1) * opt


def respeta_garantia_lpt(c, opt, m):
    # 3m * C_LPT <= (4m - 1) * OPT
    return 3 * m * c <= (4 * m - 1) * opt


def verificar_solucion(trabajos, m, plan, valor):
    """Verifica factibilidad, makespan devuelto y cumplimiento de la cota inferior."""
    return (es_factible(trabajos, plan, m)
            and makespan(plan) == valor
            and valor >= cota_inferior(trabajos, m))


# ============================================================================
# 7. Medición y presentación
# ============================================================================

def medir_mediana(funcion, *argumentos, repeticiones=REPETICIONES):
    """Mide la mediana de tiempo de ejecución de una función."""
    inicio = perf_counter()
    resultado = funcion(*argumentos)
    unica = perf_counter() - inicio
    lazos = 1 if unica >= 2e-3 else min(1000, max(1, int(2e-3 / max(unica, 1e-7))))

    tiempos = []
    for _ in range(repeticiones):
        inicio = perf_counter()
        for _ in range(lazos):
            resultado = funcion(*argumentos)
        tiempos.append((perf_counter() - inicio) / lazos)
    return resultado, median(tiempos)


def formato_tiempo(segundos):
    """Formatea tiempo en s, ms o µs con formato legible."""
    if segundos != segundos or segundos is None:
        return "abortado"
    if segundos < 1e-3:
        return "%.1f us" % (segundos * 1e6)
    if segundos < 1.0:
        return "%.2f ms" % (segundos * 1e3)
    return "%.3f s" % segundos


def mostrar_tabla(encabezados, filas, titulo=None, max_filas=None):
    """Muestra una tabla con formato tabular limpio."""
    if titulo:
        print("\n" + "=" * len(titulo))
        print(titulo)
        print("=" * len(titulo))
    if max_filas is not None and len(filas) > max_filas:
        print("(mostrando %d de %d filas; todas se guardan en el archivo)" % (max_filas, len(filas)))
        filas = filas[:max_filas]
    if HAY_PANDAS:
        try:
            pd.set_option("display.max_columns", None)
            pd.set_option("display.width", 1000)
            print(pd.DataFrame(filas, columns=encabezados).to_string(index=False))
            return
        except Exception:
            pass
    anchos = [max(len(str(encabezados[i])),
                  max((len(str(f[i])) for f in filas), default=0)) + 2
              for i in range(len(encabezados))]
    print("".join(str(encabezados[i]).ljust(anchos[i]) for i in range(len(encabezados))))
    print("-" * sum(anchos))
    for fila in filas:
        print("".join(str(fila[i]).ljust(anchos[i]) for i in range(len(fila))))


def guardar_csv(nombre_archivo, encabezados, filas):
    """Guarda filas en un archivo CSV dentro de la carpeta de resultados."""
    ruta = os.path.join(CARPETA_RESULTADOS, nombre_archivo)
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(encabezados)
        escritor.writerows(filas)
    print("CSV guardado: " + ruta)
    return ruta


def guardar_figura(figura, nombre_archivo):
    """Guarda la figura matplotlib en PNG dentro de la carpeta de figuras."""
    ruta = os.path.join(CARPETA_FIGURAS, nombre_archivo)
    figura.savefig(ruta, bbox_inches="tight")
    print("Figura guardada: " + ruta)
    plt.close(figura)
