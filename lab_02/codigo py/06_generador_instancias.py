# -*- coding: utf-8 -*-
"""
Generador Reproducible de Instancias de Prueba
Problema: Pm || Cmax

Características del generador:
  - Semilla fija global y derivación unívoca por instancia.
  - Permite regenerar cualquier instancia aisladamente sin ejecutar las previas.
  - Conserva todas las instancias en un archivo estandarizado JSON.

Familias de distribución:
  1. "uniforme" : p_j ~ U[1, 20]   (duraciones con amplia variabilidad).
  2. "estrecha" : p_j ~ U[10, 20]  (duraciones homogéneas; caso difícil para LPT y Branch and Bound).
  3. "sesgada"  : 75% U[1, 5] y 25% U[15, 30] (castiga severamente a List Scheduling si los largos llegan al final).
  4. "grande"   : p_j ~ U[1, 100]  (para pruebas de escalabilidad en propuesto 2).
  5. "ajustada" : instancias teóricas de peor caso de Graham (LS) y LPT.
"""

import json
import os
from random import Random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARPETA_RESULTADOS = os.path.join(BASE_DIR, "resultados")
os.makedirs(CARPETA_RESULTADOS, exist_ok=True)

SEMILLA_GLOBAL = 2026
FAMILIAS = ("uniforme", "estrecha", "sesgada")


def generar_trabajos(n, familia, semilla):
    """Devuelve n tiempos de proceso según la familia de distribución solicitada."""
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


def instancia_ajustada_ls(m):
    """Instancia de peor caso para List Scheduling (Graham, 1966)."""
    return [1] * (m * (m - 1)) + [m]


def instancia_ajustada_lpt(m):
    """Instancia de peor caso para LPT (Graham, 1969)."""
    trabajos = []
    for p in range(2 * m - 1, m, -1):
        trabajos += [p, p]
    return trabajos + [m, m, m]


def construir_bateria_instancias():
    """Genera las instancias del Propuesto 1 y los conjuntos del Propuesto 2."""
    M_P1 = (2, 3, 4)
    N_P1 = (6, 9, 12, 15)
    INSTANCIAS_POR_COMBINACION = 2

    instancias_p1 = []
    contador = 0
    for familia in FAMILIAS:
        for m in M_P1:
            for n in N_P1:
                for _ in range(INSTANCIAS_POR_COMBINACION):
                    contador += 1
                    semilla = SEMILLA_GLOBAL * 1000 + contador
                    instancias_p1.append({
                        "id": "P1-%03d" % contador, "familia": familia, "n": n, "m": m,
                        "semilla": semilla, "trabajos": generar_trabajos(n, familia, semilla)})

    # Instancias ajustadas teóricas
    for m in M_P1:
        for nombre, funcion in (("ajustada_ls", instancia_ajustada_ls),
                                ("ajustada_lpt", instancia_ajustada_lpt)):
            contador += 1
            t = funcion(m)
            instancias_p1.append({
                "id": "P1-%03d" % contador, "familia": nombre, "n": len(t),
                "m": m, "semilla": None, "trabajos": t})

    # Conjuntos del Propuesto 2
    N_P2 = (100, 1_000, 10_000, 100_000)
    conjuntos_p2 = []
    for n in N_P2:
        semilla = SEMILLA_GLOBAL * 1000 + 500 + len(conjuntos_p2)
        conjuntos_p2.append({
            "id": "P2-n%d" % n, "familia": "grande", "n": n,
            "semilla": semilla, "trabajos": generar_trabajos(n, "grande", semilla)})

    return instancias_p1, conjuntos_p2


def main():
    print("=" * 70)
    print("GENERADOR REPRODUCIBLE DE INSTANCIAS (JSON)")
    print("=" * 70)

    instancias_p1, conjuntos_p2 = construir_bateria_instancias()

    # Guardar en JSON para reproducibilidad independiente del sistema
    ruta_json = os.path.join(CARPETA_RESULTADOS, "instancias.json")
    datos_guardar = {
        "semilla_global": SEMILLA_GLOBAL,
        "propuesto_1": instancias_p1,
        "propuesto_2": [{k: v for k, v in c.items() if k != "trabajos"} for c in conjuntos_p2]
    }
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(datos_guardar, f, indent=2)

    print("Propuesto 1: %d instancias totales (%d aleatorias + %d ajustadas)"
          % (len(instancias_p1), len(instancias_p1) - 6, 6))
    print("Propuesto 2: %d conjuntos de trabajos (n = %s)"
          % (len(conjuntos_p2), [c["n"] for c in conjuntos_p2]))
    print("\nArchivo generado con éxito:", ruta_json)

    # Verificación de reproducibilidad
    muestra = instancias_p1[17]
    regenerado = generar_trabajos(muestra["n"], muestra["familia"], muestra["semilla"])
    assert regenerado == muestra["trabajos"], "Fallo en reproducibilidad de semilla"
    print("\n[OK] Verificación de reproducibilidad exacta superada.")
    print("Ejemplo de instancia %s (%s, n=%d, m=%d, semilla=%d):"
          % (muestra["id"], muestra["familia"], muestra["n"], muestra["m"], muestra["semilla"]))
    print("  Trabajos:", muestra["trabajos"])


if __name__ == "__main__":
    main()
