# UNSAAC - Algoritmos Avanzados (2026-II)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![UNSAAC](https://img.shields.io/badge/UNSAAC-Informatica%20y%20Sistemas-red)
![Status](https://img.shields.io/badge/Status-Activo-success)
![License](https://img.shields.io/badge/License-MIT-green)

**Universidad Nacional de San Antonio Abad del Cusco**  
*Facultad de Ingeniería Eléctrica, Electrónica, Informática y Mecánica*  
*Escuela Profesional de Ingeniería Informática y de Sistemas*

</div>

---

## 📌 Presentación del Repositorio

Este repositorio contiene el desarrollo completo, experimental y riguroso de las guías de laboratorio de la asignatura **Algoritmos Avanzados** (Semestre 2026-II), a cargo del docente **Dr. Héctor Eduardo Ugarte Rojas**.

Cada laboratorio cuenta con:
* 📄 **Guía oficial e informes técnicos** en formato PDF y Markdown.
* 🐍 **Implementaciones modulares en Python** diseñadas para funcionar de forma desacoplada y offline.
* 📓 **Notebooks interactivos** (`.ipynb`) compatibles con Jupyter y Google Colab.
* 🧪 **Pruebas de factibilidad y casos límite** con verificación de garantías teóricas y cotas matemáticas.
* 📊 **Evidencia empírica reproducible:** gráficos en alta resolución y datasets en formato CSV y JSON.

---

## 👥 Integrantes del Equipo (Grupo 5)

| N.° | Apellidos y Nombres | Código |
| :---: | :--- | :---: |
| 1 | Choquenaira Quispe, Noe Franklin | 133962 |
| 2 | Porroa Sivana, Yeni Ruth | 120893 |
| 3 | Quispe Rimachi, Romario | 164257 |
| 4 | Yaranga Achahui, Aldo | 103179 |

---

## 📂 Estructura del Repositorio

```text
UNSAAC-algoritmos-avanzados/
│
├── lab_01/                             # Laboratorio 01: Complejidad y Experimentación
│   ├── Guia 01.pdf                     # Guía oficial del laboratorio
│   ├── INFORME_Y_GUIA_EJECUCION.md     # Informe técnico detallado
│   ├── README.md                       # Documentación rápida del Lab 01
│   ├── Laboratorio_01_Grupo5.ipynb     # Notebook Jupyter reproducible
│   ├── ejecutar_todo.py                # Script maestro de ejecución (Python)
│   ├── ejecutar_todo.bat               # Ejecución directa en Windows (Batch)
│   ├── resuelto_*.py                   # Ejercicios resueltos (Crecimiento, Búsquedas, Subset Sum)
│   ├── propuesto_*.py                  # Ejercicios propuestos (Ordenamientos, Límite exponencial)
│   ├── *.png                           # 6 figuras generadas automáticamente
│   └── *.csv / *.json                  # Resultados experimentales exportados
│
├── lab_02/                             # Laboratorio 02: Scheduling en Máquinas Paralelas (Pm || Cmax)
│   ├── Guia 02.pdf                     # Guía oficial del laboratorio
│   ├── informe_GUIA_02.pdf             # Informe técnico final
│   ├── informe_GUIA_02.zip             # Fuentes completas en LaTeX (.tex)
│   ├── README.md                       # Documentación técnica y suite de pruebas del Lab 02
│   ├── colab/                          # Notebook para Google Colab
│   └── codigo py/                      # Suite modular de 14 scripts
│       ├── ejecutar_todo.py            # Ejecutor maestro de los 14 scripts
│       ├── 01 a 03 (algoritmos)        # List Scheduling, LPT, Branch & Bound
│       ├── 04_pruebas_factibilidad.py  # Suite de pruebas unitarias y casos límite (300 instancias)
│       ├── 05 a 14 (experimentos)      # Complejidad, cotas de Graham, escalabilidad y dominancia
│       ├── figuras/                    # 5 gráficos en alta resolución
│       └── resultados/                 # 10 archivos CSV con métricas empíricas + instancias.json
│
├── .gitignore                          # Exclusión de temporales y proyectos externos
├── requirements.txt                    # Dependencias mínimas
└── README.md                           # Documentación principal
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
   * Instalar la biblioteca necesaria para la generación de gráficos:
     ```bash
     pip install -r requirements.txt
     ```

---

## ⚡ Ejecución Rápida

### Laboratorio 01
Para ejecutar todos los ejercicios y regenerar los 6 gráficos y tablas de datos:
```bash
cd lab_01
python ejecutar_todo.py
```
*(En Windows también se puede hacer doble clic en `ejecutar_todo.bat`)*

### Laboratorio 02
Para ejecutar los 14 scripts modulares, verificar las 300 instancias de prueba y regenerar gráficos y CSVs:
```bash
cd "lab_02/codigo py"
python ejecutar_todo.py
```
Para ejecutar específicamente la **batería de pruebas de factibilidad y casos límite**:
```bash
python 04_pruebas_factibilidad.py
```

---

## 🔄 Flujo para Incorporar Futuros Laboratorios

Para mantener la consistencia en entregas posteriores (`lab_03`, `lab_04`, etc.):
1. Crear una nueva carpeta siguiendo el estándar: `lab_03/`.
2. Guardar dentro:
   * La guía oficial en PDF.
   * El código desacoplado con su script `ejecutar_todo.py`.
   * El informe técnico o `README.md`.
   * El notebook reproducible `.ipynb`.
   * Las figuras y datos resultantes.
3. Actualizar la tabla de contenidos en este `README.md` principal.
4. Subir los cambios a GitHub mediante `git add`, `git commit` y `git push`.
