# Cuaderno Interactivo y Código Experimental - Laboratorio 03
**Asignatura:** Algoritmos Avanzados (UNSAAC, Semestre 2026-II)  
**Tema:** Aproximación avanzada: Vertex Cover, PTAS y FPTAS  
**Equipo:** GRUPO 5  

---

## 1. Contenido de esta Carpeta

* **`grupo 5 guia 03.ipynb`**: Cuaderno interactivo Jupyter/Colab oficial con **todas las celdas ya ejecutadas**, gráficos incrustados y salidas completas.
* **`generate_lab03_notebook.py`**: Script generador en Python puro para recrear o validar el cuaderno de forma automatizada.
* **`figuras/`**: Gráficos generados en alta resolución:
  * `evaluacion_vertex_cover.png`
  * `evaluacion_knapsack_fptas.png`
  * `vc_razon_familia.png`
  * `vc_tiempos_comparados.png`
  * `vc_acierto_densidad.png`
  * `knap_calidad_vs_epsilon.png`
  * `knap_costo_vs_inv_epsilon.png`
* **`resultados/`**: Tablas en formato CSV y resumen:
  * `tabla_vertex_cover.csv`: 30 grafos evaluados con 20 permutaciones cada uno (600 corridas).
  * `tabla_knapsack_fptas.csv`: 20 instancias evaluadas bajo $\varepsilon \in \{0.50, 0.25, 0.10, 0.05\}$ (80 corridas).
  * `resumen_ejecucion.txt`: Métricas globales y confirmación de garantías teóricas al 100%.
* **`resultados_lab03.zip`**: Paquete comprimido con las evidencias para la entrega del laboratorio.

---

## 2. Instrucciones para Google Colab

1. Ingresar a [Google Colab](https://colab.research.google.com/).
2. Ir a la pestaña **Subir** (*Upload*) y seleccionar `grupo 5 guia 03.ipynb`.
3. En la barra superior, hacer clic en **Entorno de ejecución** $\to$ **Ejecutar todas** (`Ctrl + F9`).
4. La totalidad de las 600 pruebas de Vertex Cover y las 80 evaluaciones de Knapsack FPTAS se completan en aproximadamente 20 segundos sin necesidad de instalar librerías adicionales.
5. Gracias a la constante `SEMILLA_GLOBAL = 2026`, todos los resultados numéricos y gráficos son $100\%$ idénticos y reproducibles.
