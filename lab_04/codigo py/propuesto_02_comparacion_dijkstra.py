#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio 04 - Algoritmos Avanzados (UNSAAC, 2026-II)
Ejercicio Propuesto 2: Comparación Empírica con heapq y Algoritmo de Dijkstra
"""

import os
import csv
import time
import random
from statistics import median
import matplotlib.pyplot as plt

from resuelto_03_heapq_perezoso import HeapqPriorityQueue
from propuesto_01_fibonacci_heap import FibonacciHeap

SEMILLA_GLOBAL = 2026
DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_FIGURAS = os.path.join(DIR_BASE, "figuras")
DIR_RESULTADOS = os.path.join(DIR_BASE, "resultados")

os.makedirs(DIR_FIGURAS, exist_ok=True)
os.makedirs(DIR_RESULTADOS, exist_ok=True)

def ejecutar_escenario_a():
    print("\n" + "=" * 60)
    print(" ESCENARIO A: OPERACIONES BÁSICAS (10 REPETICIONES)")
    print("=" * 60)
    valores_n = [1000, 5000, 10000, 25000]
    res_a = []
    print("n      | Heapq Ins(ms) [Min-Max] Ext(ms) [Min-Max] | Fib Ins(ms) [Min-Max] Ext(ms) [Min-Max]")
    print("-------+-------------------------------------------+-----------------------------------------")

    for n in valores_n:
        rng = random.Random(SEMILLA_GLOBAL + n)
        claves = [rng.randint(1, 10**8) for _ in range(n)]
        t_ins_h, t_ext_h, t_ins_f, t_ext_f = [], [], [], []
        ord_h, ord_f = None, None

        for rep in range(10):
            # Heapq
            pq = HeapqPriorityQueue(); t0 = time.perf_counter_ns()
            for idx, k in enumerate(claves): pq.insert(idx, k)
            t_ins_h.append((time.perf_counter_ns() - t0) / 1e6)
            ext_h = []; t0 = time.perf_counter_ns()
            while not pq.is_empty(): ext_h.append(pq.extract_min()[1])
            t_ext_h.append((time.perf_counter_ns() - t0) / 1e6)
            if rep == 0: ord_h = ext_h

            # Fibonacci Heap
            fib = FibonacciHeap(); t0 = time.perf_counter_ns()
            for idx, k in enumerate(claves): fib.insert(k, idx)
            t_ins_f.append((time.perf_counter_ns() - t0) / 1e6)
            ext_f = []; t0 = time.perf_counter_ns()
            while not fib.is_empty(): ext_f.append(fib.extract_min().key)
            t_ext_f.append((time.perf_counter_ns() - t0) / 1e6)
            if rep == 0: ord_f = ext_f

        assert ord_h == ord_f, f"Discrepancia para n={n}"
        row = {
            "n": n,
            "ins_h_med": median(t_ins_h), "ins_h_min": min(t_ins_h), "ins_h_max": max(t_ins_h),
            "ext_h_med": median(t_ext_h), "ext_h_min": min(t_ext_h), "ext_h_max": max(t_ext_h),
            "ins_f_med": median(t_ins_f), "ins_f_min": min(t_ins_f), "ins_f_max": max(t_ins_f),
            "ext_f_med": median(t_ext_f), "ext_f_min": min(t_ext_f), "ext_f_max": max(t_ext_f),
        }
        res_a.append(row)
        print(f"{n:6d} | {row['ins_h_med']:6.2f} [{row['ins_h_min']:5.2f}-{row['ins_h_max']:5.2f}] {row['ext_h_med']:6.2f} [{row['ext_h_min']:5.2f}-{row['ext_h_max']:5.2f}] | {row['ins_f_med']:6.2f} [{row['ins_f_min']:5.2f}-{row['ins_f_max']:5.2f}] {row['ext_f_med']:6.2f} [{row['ext_f_min']:5.2f}-{row['ext_f_max']:5.2f}]")

    # Guardar CSV
    ruta_csv_a = os.path.join(DIR_RESULTADOS, "tabla_escenario_a.csv")
    with open(ruta_csv_a, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=res_a[0].keys())
        writer.writeheader(); writer.writerows(res_a)

    # Gráfico 1
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    n_v = [r['n'] for r in res_a]
    ax1.plot(n_v, [r['ins_h_med'] for r in res_a], marker='o', label='Heapq (C-Python)')
    ax1.plot(n_v, [r['ins_f_med'] for r in res_a], marker='s', label='Fibonacci Heap')
    ax1.set_title("Inserción de n Elementos", fontweight='bold'); ax1.set_xlabel("n"); ax1.set_ylabel("Tiempo (ms)"); ax1.legend(); ax1.grid(True)

    ax2.plot(n_v, [r['ext_h_med'] for r in res_a], marker='o', label='Heapq (C-Python)')
    ax2.plot(n_v, [r['ext_f_med'] for r in res_a], marker='s', label='Fibonacci Heap')
    ax2.set_title("Extracción de n Elementos", fontweight='bold'); ax2.set_xlabel("n"); ax2.set_ylabel("Tiempo (ms)"); ax2.legend(); ax2.grid(True)
    plt.tight_layout()
    ruta_fig_a = os.path.join(DIR_FIGURAS, "fig_escenario_a_tiempos.png")
    plt.savefig(ruta_fig_a, dpi=300)
    plt.close()
    return res_a

def ejecutar_escenario_b():
    print("\n" + "=" * 60)
    print(" ESCENARIO B: DISMINUCIONES INTENSIVAS q = 10n (5 REPETICIONES)")
    print("=" * 60)
    valores_n = [1000, 5000, 10000, 20000]
    res_b = []
    print("n      q        | T_Heapq (ms) [Min-Max] Físico Activos | T_Fib (ms) [Min-Max] Cortes Cascadas")
    print("-------+--------+---------------------------------------+-------------------------------------")

    for n in valores_n:
        q = 10 * n
        t_h_reps, t_f_reps = [], []
        fisico_h, activos_h, cortes_f, casc_f = 0, 0, 0, 0

        for rep in range(5):
            rng = random.Random(SEMILLA_GLOBAL + n * 17 + rep)
            claves_init = {i: rng.randint(10**7, 10**8) for i in range(n)}

            # Heapq
            pq = HeapqPriorityQueue()
            for idx, k in claves_init.items(): pq.insert(idx, k)
            claves_h = dict(claves_init); activos_h_list = list(range(n))
            t0 = time.perf_counter_ns()
            for i in range(q):
                target_id = rng.choice(activos_h_list)
                nk = max(1, claves_h[target_id] - rng.randint(1, 1000))
                claves_h[target_id] = nk
                pq.decrease_key(target_id, nk)
                if (i + 1) % 20 == 0 and not pq.is_empty():
                    ext_id, _ = pq.extract_min(); activos_h_list.remove(ext_id)
            t_h_reps.append((time.perf_counter_ns() - t0) / 1e6)
            if rep == 0: fisico_h, activos_h = pq.physical_size, len(pq.entries)

            # Fibonacci
            fib = FibonacciHeap()
            nodos_f = {idx: fib.insert(k, idx) for idx, k in claves_init.items()}
            claves_f = dict(claves_init); activos_f_list = list(range(n))
            rng_f = random.Random(SEMILLA_GLOBAL + n * 17 + rep)
            t0 = time.perf_counter_ns()
            for i in range(q):
                target_id = rng_f.choice(activos_f_list)
                nk = max(1, claves_f[target_id] - rng_f.randint(1, 1000))
                claves_f[target_id] = nk
                fib.decrease_key(nodos_f[target_id], nk)
                if (i + 1) % 20 == 0 and not fib.is_empty():
                    mn = fib.extract_min(); activos_f_list.remove(mn.value); del nodos_f[mn.value]
            t_f_reps.append((time.perf_counter_ns() - t0) / 1e6)
            if rep == 0: cortes_f, casc_f = fib.cuts, fib.cascading_cuts

        row = {
            "n": n, "q": q,
            "th_med": median(t_h_reps), "th_min": min(t_h_reps), "th_max": max(t_h_reps),
            "tf_med": median(t_f_reps), "tf_min": min(t_f_reps), "tf_max": max(t_f_reps),
            "fisico": fisico_h, "activos": activos_h, "cortes": cortes_f, "cascadas": casc_f
        }
        res_b.append(row)
        print(f"{n:6d} {q:8d} | {row['th_med']:7.2f} [{row['th_min']:6.2f}-{row['th_max']:6.2f}] {fisico_h:6d} {activos_h:6d} | {row['tf_med']:7.2f} [{row['tf_min']:6.2f}-{row['tf_max']:6.2f}] {cortes_f:6d} {casc_f:6d}")

    # Guardar CSV
    ruta_csv_b = os.path.join(DIR_RESULTADOS, "tabla_escenario_b.csv")
    with open(ruta_csv_b, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=res_b[0].keys())
        writer.writeheader(); writer.writerows(res_b)

    # Gráficos 2 y 3
    q_v = [r['q'] for r in res_b]
    plt.figure(figsize=(7, 4.5))
    plt.plot(q_v, [r['th_med'] for r in res_b], marker='o', label='Heapq (Perezoso)')
    plt.plot(q_v, [r['tf_med'] for r in res_b], marker='s', label='Fibonacci Heap')
    plt.title("Tiempo Total frente a q Disminuciones", fontweight='bold')
    plt.xlabel("q (Disminuciones)"); plt.ylabel("Tiempo (ms)"); plt.legend(); plt.grid(True)
    plt.tight_layout()
    ruta_fig_b1 = os.path.join(DIR_FIGURAS, "fig_escenario_b_disminuciones.png")
    plt.savefig(ruta_fig_b1, dpi=300)
    plt.close()

    plt.figure(figsize=(7, 4.5))
    plt.plot(q_v, [r['fisico'] for r in res_b], marker='^', color='#ff7f0e', label='Tamaño Físico Heapq')
    plt.plot(q_v, [r['activos'] for r in res_b], marker='v', color='#2ca02c', linestyle='--', label='Entradas Activas')
    plt.fill_between(q_v, [r['activos'] for r in res_b], [r['fisico'] for r in res_b], color='#ff7f0e', alpha=0.15)
    plt.title("Sobrecosto de Memoria en Heapq", fontweight='bold')
    plt.xlabel("q (Disminuciones)"); plt.ylabel("Entradas"); plt.legend(); plt.grid(True)
    plt.tight_layout()
    ruta_fig_b2 = os.path.join(DIR_FIGURAS, "fig_escenario_b_tamano_heapq.png")
    plt.savefig(ruta_fig_b2, dpi=300)
    plt.close()
    return res_b

def generar_grafo(num_v, factor_e, seed=SEMILLA_GLOBAL):
    rng = random.Random(seed)
    num_e_target = int(num_v * factor_e)
    adj = {i: [] for i in range(num_v)}
    edges = set()
    for i in range(1, num_v):
        p = rng.randint(0, i - 1)
        w = rng.randint(1, 100)
        adj[p].append((i, w)); adj[i].append((p, w))
        edges.add((min(p, i), max(p, i)))
    while len(edges) < num_e_target:
        u, v = rng.randint(0, num_v - 1), rng.randint(0, num_v - 1)
        if u != v and (min(u, v), max(u, v)) not in edges:
            edges.add((min(u, v), max(u, v)))
            w = rng.randint(1, 100)
            adj[u].append((v, w)); adj[v].append((u, w))
    return adj, len(edges)

def dijkstra_h(adj, src):
    dist = {u: float('inf') for u in adj}; dist[src] = 0
    pq = HeapqPriorityQueue(); pq.insert(src, 0)
    while not pq.is_empty():
        u, d = pq.extract_min()
        if d > dist[u]: continue
        for v, w in adj[u]:
            if w < 0: raise ValueError("Pesos negativos")
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if v in pq.entries: pq.decrease_key(v, nd)
                else: pq.insert(v, nd)
    return dist

def dijkstra_f(adj, src):
    dist = {u: float('inf') for u in adj}; dist[src] = 0
    fib = FibonacciHeap(); nodes = {src: fib.insert(0, src)}
    while not fib.is_empty():
        min_n = fib.extract_min()
        d, u = min_n.key, min_n.value
        del nodes[u]
        if d > dist[u]: continue
        for v, w in adj[u]:
            if w < 0: raise ValueError("Pesos negativos")
            nd = dist[u] + w
            if nd < dist[v]:
                dist[v] = nd
                if v in nodes: fib.decrease_key(nodes[v], nd)
                else: nodes[v] = fib.insert(nd, v)
    return dist

def ejecutar_escenario_c():
    print("\n" + "=" * 60)
    print(" ESCENARIO C: ALGORITMO DE DIJKSTRA (5 REPETICIONES)")
    print("=" * 60)
    valores_v = [500, 1000, 2000, 4000]
    res_c = []
    for dens in [3.0, 10.0]:
        etiqueta = "Disperso (3V)" if dens == 3.0 else "Intermedio (10V)"
        for v in valores_v:
            adj, e = generar_grafo(v, dens, seed=SEMILLA_GLOBAL + v * int(dens))
            t_h_reps, t_f_reps = [], []
            for rep in range(5):
                t0 = time.perf_counter_ns(); dh = dijkstra_h(adj, 0)
                t_h_reps.append((time.perf_counter_ns() - t0) / 1e6)
                t0 = time.perf_counter_ns(); df = dijkstra_f(adj, 0)
                t_f_reps.append((time.perf_counter_ns() - t0) / 1e6)
                if rep == 0:
                    for u in adj: assert dh[u] == df[u]
            row = {
                "tipo": etiqueta, "factor": dens, "V": v, "E": e,
                "th_med": median(t_h_reps), "th_min": min(t_h_reps), "th_max": max(t_h_reps),
                "tf_med": median(t_f_reps), "tf_min": min(t_f_reps), "tf_max": max(t_f_reps)
            }
            res_c.append(row)
            print(f"[{etiqueta:15s}] |V|={v:4d} |E|={e:5d} -> Heapq={row['th_med']:6.2f}ms [{row['th_min']:5.2f}-{row['th_max']:5.2f}] | Fib={row['tf_med']:6.2f}ms [{row['tf_min']:5.2f}-{row['tf_max']:5.2f}] (100% Idéntico)")

    # Validación de casos frontera
    adj_disc = {0: [(1, 0)], 1: [(0, 0)], 2: []}
    assert dijkstra_h(adj_disc, 0)[2] == float('inf') and dijkstra_f(adj_disc, 0)[2] == float('inf')
    assert dijkstra_h(adj_disc, 0)[1] == 0 and dijkstra_f(adj_disc, 0)[1] == 0
    try:
        dijkstra_h({0: [(1, -1)]}, 0); assert False
    except ValueError:
        pass
    print("[OK] Casos frontera en Dijkstra validados: desconexión, arista peso 0 y rechazo de pesos negativos.")

    # Guardar CSV
    ruta_csv_c = os.path.join(DIR_RESULTADOS, "tabla_dijkstra.csv")
    with open(ruta_csv_c, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=res_c[0].keys())
        writer.writeheader(); writer.writerows(res_c)

    # Gráfico 4
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))
    disp = [r for r in res_c if r['factor'] == 3.0]
    inter = [r for r in res_c if r['factor'] == 10.0]
    ax1.plot([r['V'] for r in disp], [r['th_med'] for r in disp], marker='o', label='Heapq')
    ax1.plot([r['V'] for r in disp], [r['tf_med'] for r in disp], marker='s', label='Fibonacci')
    ax1.set_title("Dijkstra Disperso (|E| ≈ 3|V|)", fontweight='bold'); ax1.set_xlabel("|V|"); ax1.set_ylabel("Tiempo (ms)"); ax1.legend(); ax1.grid(True)
    ax2.plot([r['V'] for r in inter], [r['th_med'] for r in inter], marker='o', label='Heapq')
    ax2.plot([r['V'] for r in inter], [r['tf_med'] for r in inter], marker='s', label='Fibonacci')
    ax2.set_title("Dijkstra Intermedio (|E| ≈ 10|V|)", fontweight='bold'); ax2.set_xlabel("|V|"); ax2.set_ylabel("Tiempo (ms)"); ax2.legend(); ax2.grid(True)
    plt.tight_layout()
    ruta_fig_c = os.path.join(DIR_FIGURAS, "fig_escenario_c_dijkstra.png")
    plt.savefig(ruta_fig_c, dpi=300)
    plt.close()
    return res_c

def main():
    print("=" * 60)
    print(" EJERCICIO PROPUESTO 2: BENCHMARKS Y DIJKSTRA")
    print("=" * 60)
    ejecutar_escenario_a()
    ejecutar_escenario_b()
    ejecutar_escenario_c()

if __name__ == "__main__":
    main()
