#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de compilación para el informe de Laboratorio 04 (UNSAAC).
Ejecuta las pasadas necesarias de pdflatex para resolver referencias cruzadas,
índices (TOC, LOF, LOT) y marcadores PDF.
"""

import os
import subprocess
import sys

def compilar():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(base_dir)
    
    print("=" * 65)
    print(" Compilando Informe de Laboratorio 04 (UNSAAC - Grupo 5)")
    print(" Tema: Montículos de Fibonacci y Análisis Amortizado")
    print("=" * 65)
    
    cmd = ['pdflatex', '-interaction=nonstopmode', 'main.tex']
    
    for pasada in range(1, 4):
        print(f"[{pasada}/3] Compilando con pdflatex...")
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"Error en pasada {pasada}:")
            print(r.stdout[-1500:])
            return False
        if pasada >= 2 and "Rerun to get" not in r.stdout and "undefined references" not in r.stdout:
            print(f"[OK] Índices y referencias resueltos completamente en pasada {pasada}.")
            break
        
    if os.path.exists('main.pdf'):
        size_kb = os.path.getsize('main.pdf') / 1024
        print(f"\n[OK] Documento PDF generado exitosamente: main.pdf ({size_kb:.1f} KB)")
        return True
    else:
        print("[ERROR] No se encontró el archivo main.pdf.")
        return False

if __name__ == '__main__':
    exito = compilar()
    sys.exit(0 if exito else 1)
