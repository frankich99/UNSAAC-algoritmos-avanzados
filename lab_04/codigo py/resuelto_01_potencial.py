#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Laboratorio 04 - Algoritmos Avanzados (UNSAAC, 2026-II)
Ejercicio Resuelto 1: Estado del Potencial y Costo Amortizado
"""

from dataclasses import dataclass

@dataclass(frozen=True)
class EstadoPotencial:
    arboles: int
    marcados: int

    def potencial(self) -> int:
        return self.arboles + 2 * self.marcados

def costo_amortizado(costo_real: int, antes: EstadoPotencial, despues: EstadoPotencial):
    delta_phi = despues.potencial() - antes.potencial()
    costo_am = costo_real + delta_phi
    return costo_am, delta_phi

def main():
    print("=" * 60)
    print(" EJERCICIO RESUELTO 1: ANÁLISIS DE POTENCIAL Y AMORTIZACIÓN")
    print("=" * 60)

    # Caso de prueba oficial de la Guía 04
    antes = EstadoPotencial(arboles=4, marcados=3)
    despues = EstadoPotencial(arboles=7, marcados=0)
    costo_real = 4

    amortizado, delta = costo_amortizado(costo_real, antes, despues)

    print(f"Estado inicial : {antes.arboles} árboles, {antes.marcados} marcados -> Phi(H0) = {antes.potencial()}")
    print(f"Estado final   : {despues.arboles} árboles, {despues.marcados} marcados -> Phi(H1) = {despues.potencial()}")
    print(f"Cambio neto    : Delta Phi = {delta:+d}")
    print(f"Costo real     : c_i = {costo_real}")
    print(f"Costo amortiz. : c_hat = c_i + Delta Phi = {costo_real} + ({delta}) = {amortizado}")

    assert antes.potencial() == 10, "Error en cálculo de Phi inicial"
    assert despues.potencial() == 7, "Error en cálculo de Phi final"
    assert delta == -3, "Error en Delta Phi"
    assert amortizado == 1, "Error en Costo Amortizado"

    print("\n[ÉXITO] Ejercicio Resuelto 1 validado y verificado al 100%.")

if __name__ == "__main__":
    main()
