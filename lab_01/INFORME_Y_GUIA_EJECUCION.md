# Universidad Nacional de San Antonio Abad del Cusco
## Facultad de Ingeniería Eléctrica, Electrónica, Informática y Mecánica
### Escuela Profesional de Ingeniería Informática y de Sistemas

---

# GUÍA DE EJECUCIÓN E INFORME TÉCNICO: LABORATORIO N.º 01
## Complejidad y Experimentación Algorítmica

| Parámetro | Detalle |
| :--- | :--- |
| **Asignatura:** | Algoritmos Avanzados |
| **Semestre Académico:** | 2026-II |
| **Docente:** | Dr. Héctor Eduardo Ugarte Rojas |
| **Grupo:** | **GRUPO 5** |
| **Entorno de Trabajo:** | Python 3.10+ (100% Offline / Sin conexión a Internet) |

### Integrantes del Equipo

| N.° | Apellidos y Nombres | Código |
| :---: | :--- | :---: |
| 1 | Choquenaira Quispe, Noe Franklin | 133962 |
| 2 | Porroa Sivana, Yeni Ruth | 120893 |
| 3 | Quispe Rimachi, Romario | 164257 |
| 4 | Yaranga Achahui, Aldo | 103179 |

---

## 1. Guía Rápida de Ejecución Offline (Sin Internet)

Todos los códigos han sido desacoplados del notebook de Jupyter para funcionar de manera independiente mediante scripts de Python (`.py`), utilizando la biblioteca estándar y `matplotlib` para la generación autónoma de gráficos y exportación de datos.

### 1.1. Estructura de Archivos del Proyecto

```text
lab_01/
│
├── ejecutar_todo.bat               # Ejecución automática en Windows con doble clic
├── ejecutar_todo.py                # Script maestro de ejecución secuencial
│
├── resuelto_1_crecimiento.py       # Ejercicio 6.1: Crecimiento lineal O(n) y cuadrático Θ(n²)
├── resuelto_2_busquedas.py         # Ejercicio 6.2: Búsquedas lineal O(n) y binaria O(log n)
├── resuelto_3_subset_sum.py        # Ejercicio 6.3: Subset Sum (Fuerza Bruta, DP, Ramificar-Podar)
├── propuesto_1_ordenamientos.py    # Ejercicio 7.1: Insertion Sort vs Merge Sort
├── propuesto_2_subset_sum_limite.py  # Ejercicio 7.2: Límite exponencial de Subset Sum y Podas
│
├── INFORME_Y_GUIA_EJECUCION.md     # Documentación completa y respuestas teóricas
├── Laboratorio_01_Grupo5.ipynb     # Notebook original de referencia
├── Guia 01.pdf                     # Documento oficial del laboratorio
│
├── grafico_1.png                   # Gráficas generadas automáticamente
├── grafico_2.png
├── grafico_3.png
├── grafico_4.png
├── grafico_5.png
├── grafico_6.png
├── propuesto1_ordenamientos.csv    # Tabla de mediciones de ordenamiento
└── propuesto2_instancias.json      # Instancias reproducibles de Subset Sum
```

---

### 1.2. Comandos de Ejecución

Abra una terminal (PowerShell, Símbolo del sistema CMD o Terminal de Linux) posicionada en la carpeta del laboratorio:

#### Opción A: Ejecutar TODO el Laboratorio de una sola vez
```powershell
# En Windows (PowerShell o CMD):
python ejecutar_todo.py

# O simplemente ejecutando el archivo batch:
.\ejecutar_todo.bat
```
*Tiempo aproximado de ejecución:* ~25 a 35 segundos (ejecuta todas las repeticiones estadísticas, genera las 6 figuras PNG, el archivo CSV y el JSON).

#### Opción B: Ejecutar cada ejercicio de forma INDEPENDIENTE

1. **Ejercicio Resuelto 1 (Lineal vs Cuadrático):**
   ```powershell
   python resuelto_1_crecimiento.py
   ```
   *Salida:* Tabla en consola con factores de duplicación + genera `grafico_1.png`.

2. **Ejercicio Resuelto 2 (Búsqueda Lineal vs Binaria):**
   ```powershell
   python resuelto_2_busquedas.py
   ```
   *Salida:* Tabla con comparaciones exactas y factor de ahorro + genera `grafico_2.png`.

3. **Ejercicio Resuelto 3 (Subset Sum exacto):**
   ```powershell
   python resuelto_3_subset_sum.py
   ```
   *Salida:* Verificación con instancia oficial de la guía ($T = 42$) y escalado asintótico + genera `grafico_3.png`.

4. **Ejercicio Propuesto 1 (Insertion Sort vs Merge Sort):**
   ```powershell
   python propuesto_1_ordenamientos.py
   ```
   *Salida:* Tabla comparativa para listas Aleatorias, Ordenadas e Inversas (7 repeticiones, mediana) + genera `propuesto1_ordenamientos.csv`, `grafico_4.png` y `grafico_5.png`.

5. **Ejercicio Propuesto 2 (Límite Exponencial de Subset Sum):**
   ```powershell
   python propuesto_2_subset_sum_limite.py
   ```
   *Salida:* Evaluación con paridad matemática rigurosa ($n = 8$ hasta $26$), corte de seguridad de Fuerza Bruta ($> 1.0\text{ s}$), prueba de poda favorable vs desfavorable con $n = 20$ + genera `propuesto2_instancias.json` y `grafico_6.png`.

---

## 2. Respuestas al Trabajo Preparatorio

### a) ¿Por qué una sola medición temporal puede ser poco confiable?
Una sola medición temporal de reloj de pared (*wall-clock time*) está sujeta a perturbaciones externas aleatorias introducidas por el entorno de ejecución:
1. **Planificador del Sistema Operativo:** Interrupciones por cambios de contexto (*context switches*) y procesos concurrentes en segundo plano.
2. **Recolector de Basura (Garbage Collector):** Si el recolector de memoria se activa en medio de una medición, añade latencias ajenas al algoritmo.
3. **Jerarquía de Memoria y Caché:** La primera iteración suele experimentar *cold-start cache misses*; ejecuciones sucesivas se benefician de datos ya residentes en las memorias caché L1/L2/L3.
4. **Variación de Frecuencia de la CPU (Turbo Boost / Throttling):** Las frecuencias de reloj varían de acuerdo a la carga térmica y demanda del procesador.

**Metodología aplicada:** En este laboratorio se realizan al menos 7 repeticiones independientes y se toma la **mediana** como estimador estadístico robusto (insensible a valores extremos atípicos), empleando el temporizador monotónico de alta resolución `time.perf_counter()`.

---

### b) ¿Cuál es la diferencia entre el valor de un entero y su tamaño de representación?
- El **valor numérico** de un entero $N$ es su magnitud matemática en la recta real.
- Su **tamaño de representación** (longitud real de entrada $n$) es la cantidad de bits necesarios para codificarlo en binario:
  $$n = \lceil \log_2(N + 1) \rceil \text{ bits} \implies N \approx 2^n$$

**Impacto en complejidad algorítmica:**  
Un algoritmo cuyo costo crece proporcionalmente al valor $N$ (por ejemplo, el algoritmo de Programación Dinámica para Subset Sum cuyo tiempo es $O(n \cdot T)$, donde $T$ es el objetivo numérico) es **pseudo-polinomial**: parece polinomial respecto al número $T$, pero es estrictamente **exponencial** respecto al tamaño de su entrada en bits ($O(n \cdot 2^b)$, con $b = \lceil \log_2 T \rceil$).

---

### c) ¿Por qué dos algoritmos con igual complejidad asintótica pueden mostrar tiempos distintos?
La notación asintótica $O(f(n))$ describe el comportamiento del tiempo en el límite cuando $n \to \infty$, suprimiendo deliberadamente constantes multiplicativas $c$ y términos de orden inferior:
1. **Constante oculta ($c$):** Dos algoritmos con complejidades $T_1(n) = 100n$ y $T_2(n) = 2n$ pertenecen ambos a la clase $O(n)$, pero el primero será aproximadamente 50 veces más lento.
2. **Localidad espacial y temporal:** Los algoritmos iterativos que recorren arreglos contiguos en memoria minimizan los fallos de línea de caché, mientras que aquellos con saltos dispersos o alta recursión incurren en sobrecarga de la pila (*call stack overhead*).
3. **Costo de operaciones elementales:** Operaciones a nivel de registros de CPU (como sumas o desplazamientos de bits) son significativamente más rápidas que reservas dinámicas de memoria o copias profundas de objetos.

---

## 3. Análisis de los Ejercicios Resueltos

### 3.1. Ejercicio Resuelto 1: Crecimiento Lineal y Cuadrático
- **Algoritmos:** `suma_lineal` ($O(n)$) frente a `contar_pares_ordenados` ($\Theta(n^2)$).
- **Comportamiento empírico:**
  - Al duplicar $n$ de 1000 a 2000 y de 2000 a 4000:
    - La suma lineal escala por factores de $\approx 1.95\times$ a $2.06\times$ (duplicación lineal).
    - El conteo de pares escala por factores de $\approx 4.01\times$ a $4.29\times$ (cuadruplicación cuadrática).
  - En la gráfica log-log (`grafico_1.png`), la pendiente de la recta lineal es $\approx 1.0$ y la del algoritmo cuadrático es $\approx 2.0$, confirmando visualmente los exponentes asintóticos.

### 3.2. Ejercicio Resuelto 2: Búsquedas Instrumentadas
- **Algoritmos:** Búsqueda lineal ($O(n)$) frente a Búsqueda binaria ($O(\log n)$) sobre arreglos ordenados con objetivo ausente ($T = n + 1$).
- **Comportamiento empírico:**
  - En el peor caso, la búsqueda lineal realiza exactamente $n$ comparaciones.
  - La búsqueda binaria realiza exactamente $\lfloor \log_2 n \rfloor + 1$ comparaciones.
  - Con $n = 1024$, la búsqueda lineal realiza 1024 comparaciones frente a solo 11 de la binaria, lo que representa un **ahorro de trabajo de más de 93 veces** (`grafico_2.png`).

### 3.3. Ejercicio Resuelto 3: Subset Sum Exacto
- **Instancia oficial de prueba:** `valores = [3, 7, 11, 13, 17, 19, 23, 29]`, `objetivo = 42`.
  - **Fuerza Bruta:** evalúa combinaciones hasta encontrar la primera válida (44 candidatos evaluados).
  - **Programación Dinámica:** genera los subconjuntos alcanzables acumulando sumas (56 estados expandidos).
  - **Ramificar y Podar:** ordena decrecientemente y poda ramas inviables (apenas 9 nodos explorados).
- **Resultados de escalado:** En `grafico_3.png`, se constata cómo la Fuerza Bruta escala al ritmo de $2^n$, mientras que DP y Ramificar-Podar resuelven las instancias con un costo computacional órdenes de magnitud menor.

---

## 4. Análisis y Respuestas de los Ejercicios Propuestos

### 4.1. Ejercicio Propuesto 1: Insertion Sort frente a Merge Sort

#### 1. ¿Por qué el comportamiento de Insertion Sort depende críticamente del orden inicial?
El bucle interno de Insertion Sort es **adaptativo**: se detiene de forma anticipada tan pronto como encuentra un elemento en el prefijo ordenado que satisface $arr[j] \le \text{clave}$. La cantidad total de desplazamientos realizados es idéntica a la cantidad de **inversiones** $I$ en el arreglo:
$$I = \{(i, j) \mid i < j \text{ y } arr[i] > arr[j]\}$$
- **Entrada Ordenada ($I = 0$):** Cada elemento se compara únicamente 1 vez con su antecesor inmediato y no se produce desplazamiento. Número de comparaciones $= n - 1 \implies \Theta(n)$ (mejor caso lineal).
- **Entrada Inversa ($I = \frac{n(n-1)}{2}$):** Cada nuevo elemento debe desplazarse hasta la primera posición, realizando $i$ comparaciones en la iteración $i$. Total: $\frac{n(n-1)}{2}$ comparaciones $\implies \Theta(n^2)$ (peor caso cuadrático).
- **Entrada Aleatoria ($I \approx \frac{n(n-1)}{4}$):** Cada clave se desplaza en promedio hasta la mitad del subarreglo $\implies \Theta(n^2)$ con aproximadamente la mitad del trabajo del peor caso.

Por el contrario, **Merge Sort** es un algoritmo **no adaptativo**: su esquema divide y vencerás biseca recursivamente el arreglo hasta el caso base y fusiona los subarreglos sin considerar el orden previo, ejecutando siempre $\Theta(n \log n)$ operaciones.

#### 2. Punto de Cruce Experimental (*Crossover Point*)
Analizando la tabla empírica generada en `propuesto1_ordenamientos.csv` y los gráficos `grafico_4.png` y `grafico_5.png`:
- **Entrada Inversa:** Merge Sort es superior prácticamente desde $n \ge 20 \text{ a } 50$, donde el costo cuadrático de Insertion Sort se dispara ($n = 3000$: Insertion tarda $920\text{ ms}$ frente a $8.37\text{ ms}$ de Merge, siendo Merge **más de 100 veces más rápido**).
- **Entrada Aleatoria:** El punto de cruce exacto en este equipo se sitúa en el intervalo **$n \in [50, 100]$**. Para $n \le 20$, Insertion Sort es más rápido debido a su baja sobrecarga en memoria y operaciones *in-place*; para $n \ge 100$, la complejidad $O(n \log n)$ de Merge Sort domina de forma contundente.
- **Entrada Ordenada:** Insertion Sort opera en tiempo lineal $O(n)$ y supera ampliamente a Merge Sort en todas las dimensiones evaluadas (para $n = 3000$, Insertion requiere solo $0.73\text{ ms}$ frente a $8.82\text{ ms}$ de Merge).

> **Conclusión sobre el cruce:** El punto de cruce **no es una constante universal**. Depende de la sobrecarga de asignación de memoria dinámica del lenguaje (copias de sublistas en `merge`), la eficiencia de la memoria caché y la arquitectura del procesador. Este principio fundamenta algoritmos híbridos de producción industrial como **Timsort** (el algoritmo estándar de Python y Java), que ejecuta Insertion Sort sobre bloques pequeños ($n < 64$) y Merge Sort para la combinación global.

---

### 4.2. Ejercicio Propuesto 2: Límite Práctico del Crecimiento Exponencial

#### 1. Límite Práctico de la Fuerza Bruta
La Fuerza Bruta examina exhaustivamente las $2^n$ combinaciones posibles. En nuestro entorno:
- Para $n = 18$ evalúa $262,144$ candidatos en $\approx 0.71\text{ s}$.
- Para $n = 20$ evalúa $1{,}048{,}576$ candidatos en $\approx 3.47\text{ s}$, superando con holgura el límite de seguridad establecido ($1.0\text{ s}$).
- Por consiguiente, el **límite práctico de Fuerza Bruta se determinó en $n = 20$**, desactivándose de forma segura para tamaños superiores a fin de evitar el congelamiento del sistema.
- **Implicancia de hardware:** Si se duplicara la velocidad del procesador, solo se lograría procesar $+1$ elemento adicional ($2^{n+1}/2 = 2^n$). Incluso un supercomputador $1000\times$ más veloz solo añadiría $\approx 10$ elementos a la capacidad ($2^{10} = 1024$), evidenciando la barrera insalvable del crecimiento exponencial.

#### 2. Eficacia de Cotas y Orden de Exploración en Ramificar y Podar
Ramificar y Podar opera sobre un árbol de decisiones binario optimizado mediante dos cotas:
1. **Cota de Exceso:** Si $\text{suma} > \text{objetivo}$, se poda la rama inmediatamente.
2. **Cota Superior Optimista:** Si $\text{suma} + \text{restante}[i] < \text{objetivo}$, es matemáticamente imposible alcanzar la meta y la rama se descarta.

En la prueba comparativa con $n = 20$ ($2^{20} = 1{,}048{,}576$ combinaciones):
- **Caso Favorable (valores decrecientes con elementos grandes al inicio):** El algoritmo activa las cotas en los primeros niveles del árbol, hallando la solución con tan solo **4 nodos explorados** en $18.4\ \mu\text{s}$ (explorando únicamente el $0.00019\%$ del árbol).
- **Caso Desfavorable (valores homogéneos sin solución posible):** Las cotas tardan en activarse y el algoritmo debe recorrer **565,987 nodos** en $192.5\text{ ms}$ ($27.0\%$ del árbol completo).
- **Orden de exploración:** Ordenar el arreglo de forma decreciente (`reverse=True`) sitúa los elementos con mayor peso en la parte superior del árbol. Esto maximiza la probabilidad de disparar tempranamente la cota $\text{suma} > \text{objetivo}$, eliminando de un solo golpe subárboles enteros con $2^{n - i}$ hojas.

#### 3. Relación con el Espacio de $2^n$ Subconjuntos
En `grafico_6.png` (panel inferior izquierdo), la curva de Fuerza Bruta coincide milimétricamente con la función teórica $2^n$. La técnica de Ramificar y Podar permanece siempre por debajo de $2^n$; sin embargo, en instancias desfavorables sin solución, su pendiente converge hacia la tasa exponencial. En contraste, la Programación Dinámica exhibe un comportamiento casi insensible a la explosión combinatoria: al ser de complejidad pseudo-polinomial $O(n \cdot T)$, todas las combinaciones distintas que suman el mismo valor numérico colapsan en un único estado alcanzable.

---

## 5. Conclusiones Grupales

La experimentación sistemática desarrollada en este laboratorio permitió validar de manera práctica los postulados del análisis asintótico de algoritmos, evidenciando el impacto directo de las constantes multiplicativas y la arquitectura de hardware sobre el rendimiento computacional. En el primer ejercicio propuesto se comprobó que Insertion Sort, con complejidad teórica cuadrática $O(n^2)$ en el peor caso, es superado de forma consistente por Merge Sort $O(n \log n)$ a partir de un punto de cruce experimental situado en el rango $n \in [50, 100]$ para entradas aleatorias. No obstante, se constató el carácter adaptativo de Insertion Sort ante colecciones ordenadas, donde su costo lineal $O(n)$ supera a Merge Sort en todo el dominio evaluado, justificando el diseño de algoritmos híbridos reales como Timsort.

En el segundo ejercicio propuesto, el estudio del problema Subset Sum demostró la barrera infranqueable del crecimiento exponencial $O(2^n)$ inherente a la fuerza bruta, la cual alcanzó su límite práctico admisible en $n = 20$. Asimismo, se demostró que la eficiencia de la técnica de Ramificar y Podar es fuertemente condicional: bajo cotas efectivas y ordenamiento decreciente reduce la exploración a una fracción ínfima del espacio de estados, pero degenera hacia la complejidad exponencial en instancias desfavorables. Finalmente, se constató la naturaleza pseudo-polinomial de la Programación Dinámica, cuyo costo depende del valor numérico del objetivo y no de su longitud binaria, ratificando la necesidad de aplicar una metodología de medición reproducible basada en medianas para aislar perturbaciones del entorno.

---
*UNSAAC - Carrera Profesional de Ingeniería Informática y de Sistemas - 2026*
