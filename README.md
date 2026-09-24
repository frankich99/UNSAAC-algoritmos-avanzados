# UNSAAC - Algoritmos Avanzados (2026-II)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![LaTeX](https://img.shields.io/badge/LaTeX-pdflatex-green?logo=latex&logoColor=white)
![UNSAAC](https://img.shields.io/badge/UNSAAC-Informatica%20y%20Sistemas-red)
![Status](https://img.shields.io/badge/Status-Activo-success)
![License](https://img.shields.io/badge/License-MIT-green)

**Universidad Nacional de San Antonio Abad del Cusco**  
*Facultad de Ingeniería Eléctrica, Electrónica, Informática y Mecánica*  
*Escuela Profesional de Ingeniería Informática y de Sistemas*

</div>

---

## 📌 Presentación del Repositorio

Este repositorio contiene el desarrollo completo, experimental y riguroso de las guías de laboratorio de la asignatura **Algoritmos Avanzados** (Semestre Académico 2026-II), a cargo del docente **Dr. Héctor Eduardo Ugarte Rojas**.

Cada laboratorio incluye:
* 📄 **Guías oficiales e informes técnicos:** Documentos formales en PDF generados con tipografía APA 7, índices interactivos completos (TOC, LOF, LOT y marcadores PDF) y paquetes compatibles con Overleaf.
* 🐍 **Implementaciones en Python desacopladas:** Código estructurado, tipado y modular listo para ejecución local o en la nube.
* 📓 **Notebooks interactivos reproducible:** Cuadernos `.ipynb` ejecutables en JupyterLab, VS Code y Google Colab.
* 🧪 **Baterías experimentales y casos límite:** Verificación rigurosa de cotas matemáticas, razones de aproximación y garantías teóricas.
* 📊 **Evidencia empírica respaldada:** Gráficos estadísticos vectoriales/alta resolución y tablas de resultados en formato CSV.

---

## 👥 Integrantes del Equipo (Grupo 5)

| N.° | Apellidos y Nombres | Código | Correo Institucional |
| :---: | :--- | :---: | :--- |
| 1 | Choquenaira Quispe, Noe Franklin | 133962 | `133962@unsaac.edu.pe` |
| 2 | Porroa Sivana, Yeni Ruth | 120893 | `120893@unsaac.edu.pe` |
| 3 | Quispe Rimachi, Romario | 164257 | `164257@unsaac.edu.pe` |
| 4 | Yaranga Achahui, Aldo | 103179 | `103179@unsaac.edu.pe` |

---

## 📋 Resumen de Laboratorios Desarrollados

| Laboratorio | Tema Central | Algoritmos y Métodos | Garantías / Cotas |
| :---: | :--- | :--- | :--- |
| **Lab 01** | Complejidad y Análisis Empírico | Búsquedas, ordenamientos, Subset Sum recursivo vs. poda | Análisis asintótico y tiempos reales |
| **Lab 02** | Scheduling en Máquinas Paralelas ($Pm \parallel C_{\max}$) | List Scheduling (LS), Longest Processing Time (LPT), Branch & Bound exacto | Cota de Graham: $r \le 2 - \frac{1}{m}$ (LS) y $r \le \frac{4}{3} - \frac{1}{3m}$ (LPT) |
| **Lab 03** | Aproximación Avanzada: Vertex Cover y FPTAS | Algoritmo 2-Aproximado por Matching Maximal, DP por Valores, Knapsack FPTAS con escalamiento $K = \frac{\varepsilon V_{\max}}{n}$ | Vertex Cover: $|C| \le 2\,\text{OPT}$<br>FPTAS: $\text{ALG}_\varepsilon \ge (1-\varepsilon)\,\text{OPT}$, $O(n^3/\varepsilon)$ |

---

## 📂 Estructura del Repositorio

```text
UNSAAC-algoritmos-avanzados/
│
├── lab_01/                                     # Laboratorio 01: Complejidad y Experimentación
│   ├── Guia 01.pdf                             # Guía oficial del laboratorio
│   ├── INFORME_Y_GUIA_EJECUCION.md             # Informe técnico detallado
│   ├── README.md                               # Documentación rápida del Lab 01
│   ├── Laboratorio_01_Grupo5.ipynb             # Notebook Jupyter reproducible
│   ├── ejecutar_todo.py                        # Script maestro de ejecución (Python)
│   ├── ejecutar_todo.bat                       # Ejecución directa en Windows (Batch)
│   ├── resuelto_*.py                           # Ejercicios resueltos (Crecimiento, Búsquedas, Subset Sum)
│   ├── propuesto_*.py                          # Ejercicios propuestos (Ordenamientos, Límite exponencial)
│   ├── *.png                                   # 6 figuras generadas automáticamente
│   └── *.csv / *.json                          # Resultados experimentales exportados
│
├── lab_02/                                     # Laboratorio 02: Scheduling en Máquinas Paralelas (Pm || Cmax)
│   ├── Guia 02.pdf                             # Guía oficial del laboratorio
│   ├── informe_GUIA_02.pdf                     # Informe técnico final
│   ├── informe_GUIA_02.zip                     # Fuentes completas en LaTeX (.tex)
│   ├── README.md                               # Documentación técnica y suite de pruebas del Lab 02
│   ├── colab/                                  # Notebook para Google Colab
│   └── codigo py/                              # Suite modular de 14 scripts
│       ├── ejecutar_todo.py                    # Ejecutor maestro de los 14 scripts
│       ├── 01 a 03 (algoritmos)                # List Scheduling, LPT, Branch & Bound
│       ├── 04_pruebas_factibilidad.py          # Suite de pruebas unitarias y casos límite (300 instancias)
│       ├── 05 a 14 (experimentos)              # Complejidad, cotas de Graham, escalabilidad y dominancia
│       ├── figuras/                            # 5 gráficos en alta resolución
│       └── resultados/                         # 10 archivos CSV con métricas empíricas + instancias.json
│
├── lab_03/                                     # Laboratorio 03: Vertex Cover, PTAS y FPTAS
│   ├── Guia 03.pdf                             # Guía oficial del laboratorio
│   ├── compilar_informe.bat                    # Compilación automática del informe con 1 solo clic
│   ├── modo_en_vivo.bat                        # Compilador vigilante en tiempo real (Ctrl + S)
│   │
│   ├── codigo y notebook de lab_03/            # Código y experimentación empírica
│   │   ├── grupo 5 guia 03.ipynb               # Notebook interactivo oficial (Jupyter y Colab)
│   │   ├── generate_lab03_notebook.py          # Generador y ejecutor de la suite experimental completa
│   │   ├── README.md                           # Documentación de la suite de código
│   │   ├── resultados_lab03.zip                # Respaldo completo de resultados
│   │   ├── figuras/                            # 5 figuras individuales y 2 paneles consolidados
│   │   │   ├── vc_razon_familia.png            # Distribución de la razón r(I) por familia de grafo
│   │   │   ├── vc_tiempos_comparados.png       # Tiempos exacto O(2^|V|) vs 2-aprox O(|E|)
│   │   │   ├── vc_acierto_densidad.png         # Tasa de acierto del óptimo según densidad
│   │   │   ├── knap_calidad_vs_epsilon.png     # Calidad observada frente a cota teórica (1 - ε)
│   │   │   ├── knap_costo_vs_inv_epsilon.png   # Costo computacional vs 1/ε (lineal en 1/ε)
│   │   │   ├── evaluacion_vertex_cover.png     # Panel consolidado Vertex Cover
│   │   │   └── evaluacion_knapsack_fptas.png   # Panel consolidado Knapsack FPTAS
│   │   └── resultados/                         # Datasets de salida
│   │       ├── tabla_vertex_cover.csv          # 30 grafos x 20 permutaciones (600 corridas)
│   │       ├── tabla_knapsack_fptas.csv        # 20 instancias x 4 valores de ε (80 corridas)
│   │       └── resumen_ejecucion.txt           # Resumen cuantitativo de ejecución
│   │
│   └── informe pdf de lab_03/                  # Informe académico formal en LaTeX (APA 7)
│       ├── main.tex                            # Archivo maestro central
│       ├── main.pdf                            # Documento PDF único y definitivo (17 páginas)
│       ├── informe_overleaf.zip                # Paquete modular listo para compilar en Overleaf
│       ├── compilar.bat / compilar.py          # Script de compilación multi-pasada sin '??'
│       ├── iniciar_modo_en_vivo.bat            # Auto-compilación continua
│       ├── figuras/                            # Gráficos y escudo institucional de la UNSAAC
│       └── secciones/                          # Estructura modular correlativa
│           ├── 00_portada.tex                  # Carátula oficial con datos del Grupo 5
│           ├── 01_trabajo_preparatorio.tex     # Preguntas preparatorias (5.a a 5.d)
│           ├── 02_ejercicios_resueltos.tex     # Ejercicios resueltos (1, 2, 3) con código y consola
│           ├── 03_propuesto_vertex_cover.tex   # Evaluación de 30 grafos y análisis de orden
│           ├── 04_propuesto_knapsack_fptas.tex # Algoritmo FPTAS, trade-off y mesetas de calidad
│           └── 05_conclusiones.tex             # Conclusiones grupales
│
├── .gitignore                                  # Exclusión de temporales y compilados
├── requirements.txt                            # Dependencias necesarias
└── README.md                                   # Documentación principal del repositorio
```

---

## 🚀 Requisitos e Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/frankich99/UNSAAC-algoritmos-avanzados.git
   cd UNSAAC-algoritmos-avanzados
   ```

2. **Requisitos de Python:**
   * Python 3.10 o superior.
   * Instalar las dependencias necesarias:
     ```bash
     pip install -r requirements.txt
     ```

3. **Requisitos para compilar el informe LaTeX (opcional):**
   * Distribución TeX (MiKTeX o TeX Live) con `pdflatex`.
   * Alternativamente, se puede subir [informe_overleaf.zip](lab_03/informe%20pdf%20de%20lab_03/informe_overleaf.zip) directamente a [Overleaf](https://www.overleaf.com).

---

## ⚡ Ejecución Rápida

### Laboratorio 01: Complejidad Empírica
```bash
cd lab_01
python ejecutar_todo.py
```
*(En Windows también se puede hacer doble clic en `ejecutar_todo.bat`)*

### Laboratorio 02: Scheduling en Máquinas Paralelas
```bash
cd "lab_02/codigo py"
python ejecutar_todo.py
```
Para ejecutar la batería de pruebas de factibilidad y casos límite:
```bash
python 04_pruebas_factibilidad.py
```

### Laboratorio 03: Vertex Cover, PTAS y FPTAS

#### 1. Ejecución de los experimentos y regeneración de resultados
```bash
cd "lab_03/codigo y notebook de lab_03"
python generate_lab03_notebook.py
```
O abrir interactivamente el cuaderno `grupo 5 guia 03.ipynb` en JupyterLab, VS Code o Google Colab.

#### 2. Visualización y compilación del informe en PDF
* **Compilación directa (1 clic):** Doble clic en `lab_03/compilar_informe.bat`.
* **Modo en vivo (tiempo real):** Doble clic en `lab_03/modo_en_vivo.bat`. Cada vez que guardes cambios (`Ctrl + S`), el PDF se actualizará automáticamente en menos de un segundo con índices y referencias completamente resueltos.
* **Desde VS Code:** Abrir `main.tex` o cualquier sección en `secciones/` y presionar `Ctrl + S`. La receta de doble pasada automática actualizará `main.pdf`.

#### 3. Sincronización con GitHub
Para enviar todos los avances confirmados a tu repositorio remoto:
```bash
git push origin main
```

---

## 🔬 Aspectos Teóricos Clave Evaluados en Lab 03

### 1. Minimum Vertex Cover (Algoritmo 2-Aproximado)
* **Principio del Matching Maximal:** El algoritmo selecciona codiciosamente aristas disjuntas incorporando ambos extremos a la cobertura $C$.
* **Cota Teórica:** Toda cobertura válida requiere al menos un vértice por arista independiente de un matching $M$. Por ende:
  $$\text{OPT} \ge |M| \implies |C| = 2|M| \le 2\,\text{OPT} \implies r(I) \le 2$$
* **Impacto del orden de aristas:** En caminos y ciclos altera la cardinalidad y los vértices elegidos; en estrellas altera únicamente la hoja seleccionada preservando el tamaño. En las 600 pruebas experimentales la garantía $r(I) \le 2.0$ se satisfizo al 100%.

### 2. Knapsack 0/1 mediante Escalamiento (FPTAS)
* **Programación Dinámica por Valores:** Estado $DP(i, v)$ definido como el peso mínimo para alcanzar exactamente el valor $v$ con objetos $\{1, \dots, i\}$.
* **Discretización:** Con factor $K = \frac{\varepsilon V_{\max}}{n}$, los valores escalados $v'_i = \lfloor v_i / K \rfloor$ acotan la tabla a $O(n^3/\varepsilon)$.
* **Garantía Teórica:** $\text{ALG}_\varepsilon \ge (1 - \varepsilon)\,\text{OPT}$. En las 80 evaluaciones experimentales sobre 20 instancias, la calidad empírica se mantuvo por encima del 98%, confirmando la convergencia al óptimo y el crecimiento lineal del costo respecto a $1/\varepsilon$.
