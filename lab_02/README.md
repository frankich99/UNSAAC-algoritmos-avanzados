# Universidad Nacional de San Antonio Abad del Cusco
## Facultad de Ingeniería Eléctrica, Electrónica, Informática y Mecánica
### Escuela Profesional de Ingeniería Informática y de Sistemas

---

# GUÍA DE EJECUCIÓN E INFORME TÉCNICO: LABORATORIO N.º 02
## Problema de Programación de Tareas en Máquinas Paralelas ($P_m \parallel C_{\max}$)

| Parámetro | Detalle |
| :--- | :--- |
| **Asignatura:** | Algoritmos Avanzados |
| **Semestre Académico:** | 2026-II |
| **Docente:** | Dr. Héctor Eduardo Ugarte Rojas |
| **Grupo:** | **GRUPO 5** |
| **Entorno de Trabajo:** | Python 3.10+ (100% Offline / Modular) |

### Integrantes del Equipo

| N.° | Apellidos y Nombres | Código |
| :---: | :--- | :---: |
| 1 | Choquenaira Quispe, Noe Franklin | 133962 |
| 2 | Porroa Sivana, Yeni Ruth | 120893 |
| 3 | Quispe Rimachi, Romario | 164257 |
| 4 | Yaranga Achahui, Aldo | 103179 |

---

## 1. Descripción del Laboratorio

Este laboratorio aborda el problema clásico de optimización combinatoria y scheduling **$P_m \parallel C_{\max}$**: programar un conjunto de $n$ tareas independientes con duraciones de procesamiento $p_j > 0$ sobre $m$ máquinas paralelas idénticas para minimizar el tiempo de finalización global o *makespan* ($C_{\max} = \max_i \sum_{j \in M_i} p_j$).

Al ser un problema fuertemente **NP-hard** para $m \ge 2$, se analizan empírica y formalmente:
1. **Algoritmo Heurístico List Scheduling (LS):** Asignación codiciosa (*greedy*) sobre lista arbitraria con cota teórica de aproximación de Graham:
   $$r_{LS} \le 2 - \frac{1}{m}$$
2. **Algoritmo Heurístico LPT (Longest Processing Time):** Ordenamiento previo decreciente de duraciones con cota ajustada de Graham:
   $$r_{LPT} \le \frac{4}{3} - \frac{1}{3m}$$
3. **Algoritmo Exacto Branch & Bound (Ramificar y Podar):** Búsqueda en árbol de estados con poda por cota inferior basada en el promedio de carga $\lceil \sum p_j / m \rceil$ y la tarea máxima $\max p_j$.

---

## 2. Estructura de Archivos

```text
lab_02/
│
├── Guia 02.pdf                     # Guía oficial del laboratorio (UNSAAC)
├── informe_GUIA_02.pdf             # Informe técnico final formateado
├── informe_GUIA_02.zip             # Fuentes completas en LaTeX (.tex) e imágenes
├── README.md                       # Documentación técnica del laboratorio
│
├── colab/
│   └── guia_2.ipynb                # Notebook interactivo (Jupyter / Colab)
│
└── codigo py/                      # Suite modular desacoplada
    ├── ejecutar_todo.py            # Script maestro de ejecución secuencial
    ├── utils_scheduling.py         # Módulo común con cotas, makespan y validaciones
    │
    ├── 01_ejercicio_resuelto_1.py  # Representación formal de planificaciones y validación
    ├── 02_ejercicio_resuelto_2.py  # Implementación de List Scheduling y LPT
    ├── 03_ejercicio_resuelto_3.py  # Implementación de Branch & Bound exacto con podas
    ├── 04_pruebas_factibilidad.py  # Suite de pruebas: 300 instancias y casos límite
    ├── 05_complejidad_list_scheduling.py # Comparativa O(n*m) vs Heap O(n log m)
    ├── 06_generador_instancias.py  # Generador reproducible de instancias en JSON
    ├── 07_propuesto_1_calidad.py   # Ratios empíricos frente a solución óptima
    ├── 08_propuesto_1_resumen_dominancia.py # Tablas estadísticas y dominancia LPT vs LS
    ├── 09_propuesto_1_grafico_calidad.py # Generación de gráficos de calidad
    ├── 10_propuesto_1_rendimiento_exacto.py # Límite práctico y explosión combinatoria
    ├── 11_propuesto_2_escalabilidad.py # Escalabilidad a gran escala (n hasta 1000)
    ├── 12_propuesto_2_instancia_sensible.py # Construcción de peor caso de Graham
    ├── 13_propuesto_2_graficos.py  # Gráficos de distribución, escala y tiempos
    ├── 14_propuesto_2_costo_ordenamiento.py # Análisis trade-off costo de ordenamiento
    │
    ├── figuras/                    # 5 gráficos generados en alta resolución
    │   ├── p1_calidad_razones.png
    │   ├── p1_rendimiento_exacto.png
    │   ├── p2_distribucion_orden.png
    │   ├── p2_efecto_orden_escala.png
    │   └── p2_tiempos.png
    │
    └── resultados/                 # Datasets y métricas exportadas en CSV/JSON
        ├── instancias.json
        ├── pruebas_factibilidad.csv
        ├── complejidad_list_scheduling.csv
        ├── propuesto1_calidad.csv
        ├── propuesto1_resumen.csv
        └── ...
```

---

## 3. Instrucciones de Ejecución

Posicionarse en el directorio de scripts de Python:

```bash
cd "lab_02/codigo py"
```

### A. Ejecutar Todo el Laboratorio (14 scripts)
```bash
python ejecutar_todo.py
```
Este script maestro corre de forma secuencial los 14 componentes, regenerando todos los datasets en `resultados/` y las figuras en `figuras/`.

### B. Ejecutar la Batería de Pruebas Unitarias y Factibilidad
```bash
python 04_pruebas_factibilidad.py
```
Verifica de manera exhaustiva:
* Multiconjunto de tareas intacto (`collections.Counter`).
* Rechazo de entradas inválidas ($m \le 0$, $p_j \le 0$).
* Casos límite: $n=0$, $m=1$, $m > n$, $n=m$, tareas homogéneas.
* Cumplimiento estricto de las garantías de Graham en instancias ajustadas.
* Validación masiva sobre 300 instancias sintéticas (900 soluciones validadas: LS, LPT y Branch & Bound).

### C. Ejecutar Scripts Individuales
```bash
# Calidad empírica frente al óptimo
python 07_propuesto_1_calidad.py

# Gráficos de calidad y rendimiento
python 09_propuesto_1_grafico_calidad.py
python 13_propuesto_2_graficos.py
```

---

## 4. Conclusiones y Resultados Clave

1. **Garantía Teórica vs Rendimiento Empírico:**
   Mientras que la cota teórica de Graham para LPT establece $r \le 4/3 \approx 1.333$, en el $92\%$ de las instancias aleatorias LPT encuentra el óptimo exacto ($r = 1.000$), y el peor caso observado nunca superó $1.08$.
2. **Impacto del Heap:**
   Para valores moderados a grandes de $m$, la implementación basada en montículo binario (`heapq`) reduce la asignación por tarea de $O(m)$ a $O(\log m)$, permitiendo resolver instancias con $n = 10{,}000$ en milisegundos.
3. **Límite Práctico del Algoritmo Exacto:**
   El algoritmo Branch & Bound resuelve problemas de forma instantánea para $n \le 15$, pero la explosión combinatoria del árbol de asignaciones ($m^n$) marca un límite práctico en torno a $n \approx 20 - 25$ tareas, confirmando la necesidad de heurísticas de aproximación garantizadas como LPT para instancias reales.
