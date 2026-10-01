#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio 04 - Algoritmos Avanzados (UNSAAC, 2026-II)
Ejercicio Resuelto 2: Consolidación Programada por Grados
"""

from dataclasses import dataclass, field

@dataclass
class Raiz:
    clave: int
    grado: int = 0
    hijos: list = field(default_factory=list)

    def __repr__(self):
        return f"({self.clave}, deg={self.grado})"

def enlazar_raices(a: Raiz, b: Raiz) -> Raiz:
    padre, hijo = (a, b) if a.clave <= b.clave else (b, a)
    padre.hijos.append(hijo)
    padre.grado += 1
    return padre

def consolidar_raices(raices: list[Raiz]) -> list[Raiz]:
    por_grado = {}
    for raiz in raices:
        actual = raiz
        while actual.grado in por_grado:
            otra = por_grado.pop(actual.grado)
            actual = enlazar_raices(actual, otra)
        por_grado[actual.grado] = actual
    return list(por_grado.values())

def main():
    print("=" * 60)
    print(" EJERCICIO RESUELTO 2: CONSOLIDACIÓN POR GRADOS")
    print("=" * 60)

    # Caso de prueba oficial de la Guía 04
    raices_prueba = [
        Raiz(23), Raiz(7), Raiz(21), Raiz(18, 1),
        Raiz(52), Raiz(38, 1), Raiz(17, 1), Raiz(24, 2)
    ]

    print(f"Raíces de entrada ({len(raices_prueba)} árboles):")
    for r in raices_prueba:
        print(f"  - Clave: {r.clave:2d}, Grado inicial: {r.grado}")

    resultado = consolidar_raices(raices_prueba)
    grados_resultado = sorted(r.grado for r in resultado)

    print(f"\nResultado tras consolidación ({len(resultado)} árboles):")
    for r in resultado:
        print(f"  - Raíz clave: {r.clave:2d}, Grado final: {r.grado}, Hijos directos: {len(r.hijos)}")

    print(f"\nEstructura compacta: {[(r.clave, r.grado) for r in resultado]}")

    assert len(grados_resultado) == len(set(grados_resultado)), "Existen grados duplicados"
    assert min(r.clave for r in resultado) == 7, "El mínimo global no se conservó correctamente"

    print("\n[ÉXITO] Ejercicio Resuelto 2 validado y verificado al 100%.")

if __name__ == "__main__":
    main()
