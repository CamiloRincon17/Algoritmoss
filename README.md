# Guía unificada — segundo parcial de Análisis de Algoritmos

Material de estudio con explicaciones, complejidades, ejemplos y código ejecutable en Python. Las implementaciones completas están en [`algoritmos_parcial.py`](./algoritmos_parcial.py); no requieren instalar paquetes externos y se pueden ejecutar en una computadora, VS Code o Google Colab.

> **Corrección importante sobre el esquema:** no hay un algoritmo que sea “el mejor” en todos los tamaños. Merge sort ofrece tiempo `O(n log n)` garantizado; quick sort suele ser muy rápido en arreglos medianos o grandes, pero puede degradarse a `O(n²)`; radix sort puede ser excelente para enteros no negativos de longitud limitada, pero su rendimiento depende de la cantidad de dígitos y la base. Para arreglos realmente pequeños, los costos constantes importan mucho y insertion sort puede ganar.

## Cómo ejecutar

En una terminal:

```bash
python algoritmos_parcial.py
```

El script comprueba resultados con ejemplos pequeños, muestra trazas de algunos algoritmos e imprime una comparación de tiempos. Para cambiar los números de las pruebas, edita la lista `VALUES_TO_TEST` al inicio de `algoritmos_parcial.py`. En Google Colab, sube `algoritmos_parcial.py` y ejecuta:

```python
%run algoritmos_parcial.py
```

Para importar las implementaciones en otra celda:

```python
from algoritmos_parcial import merge_sort, binary_search, BFS

print(merge_sort([8, 3, 5, 1]))
print(binary_search([1, 3, 5, 8], 5))
```

Los tiempos dependen del equipo, la versión de Python, el estado del sistema y los datos. La sección de benchmark mide varias repeticiones con `time.perf_counter()` y reporta la mediana para los algoritmos de ordenamiento, búsqueda y recorridos de grafos; no se deben presentar esos resultados como una ley universal.

---

## 1. Ordenamiento básico

Un algoritmo de ordenamiento reorganiza elementos según una relación, por ejemplo, de menor a mayor. Estos tres son fáciles de seguir, pero su tiempo cuadrático los hace poco convenientes para entradas grandes.

### Bubble sort (ordenamiento burbuja)

- **Necesidad:** ordenar una secuencia mediante comparaciones entre elementos vecinos.
- **Qué hace:** recorre la lista, compara cada pareja contigua e intercambia la pareja si está al revés. Repite pasadas hasta que no haya intercambios.
- **Traza** con `[5, 1, 4]`: primera pasada: compara `5,1` e intercambia → `[1,5,4]`; compara `5,4` e intercambia → `[1,4,5]`. Segunda pasada: no intercambia; termina.
- **Complejidad:** peor caso `O(n²)`, promedio `O(n²)`, mejor caso `O(n)` con la detección de una pasada sin intercambios. Espacio auxiliar `O(1)`.
- **Ventajas:** sencillo, estable y puede detectar que una lista ya está ordenada.
- **Desventajas / uso:** lento al crecer `n`; útil para aprender o para entradas diminutas, no para ordenar grandes volúmenes.
- **Código:** `bubble_sort` en el script.

### Selection sort (ordenamiento por selección)

- **Necesidad:** ordenar usando pocas escrituras/intercambios.
- **Qué hace:** busca el mínimo de la parte no ordenada y lo coloca en la siguiente posición libre.
- **Traza** con `[5, 1, 4]`: mínimo de toda la lista `1` → `[1,5,4]`; mínimo del resto `4` → `[1,4,5]`.
- **Complejidad:** peor, promedio y mejor caso `O(n²)` comparaciones; espacio `O(1)`. Hace `O(n)` intercambios.
- **Ventajas:** fácil y realiza pocas escrituras.
- **Desventajas / uso:** no se adapta a datos ya ordenados y, en su forma usual, no es estable; no conviene para listas grandes.
- **Código:** `selection_sort` en el script.

### Insertion sort (ordenamiento por inserción)

- **Necesidad:** ordenar manteniendo un prefijo ordenado mientras se procesa la entrada.
- **Qué hace:** toma el siguiente elemento y lo inserta en la posición correcta dentro de la parte ya ordenada.
- **Traza** con `[5, 1, 4]`: inserta `1` antes de `5` → `[1,5,4]`; inserta `4` entre ambos → `[1,4,5]`.
- **Complejidad:** peor y promedio `O(n²)`; mejor caso `O(n)` si ya está ordenada; espacio `O(1)`.
- **Ventajas:** estable, simple, eficiente en entradas pequeñas o casi ordenadas; puede ser útil dentro de algoritmos híbridos.
- **Desventajas / uso:** desplazar muchos elementos lo vuelve lento para listas grandes desordenadas.
- **Código:** `insertion_sort` en el script.

## 2. Ordenamiento eficiente

“Eficiente” describe una familia de estrategias, no un ganador universal. Los algoritmos siguientes aprovechan división y conquista o las propiedades de las claves.

### Merge sort (ordenamiento por mezcla)

- **Necesidad:** ordenar con rendimiento predecible y mantener estabilidad.
- **Qué hace:** divide la secuencia en mitades, ordena cada mitad y mezcla las dos mitades ya ordenadas.
- **Traza** con `[8, 3, 5, 1]`: divide en `[8,3]` y `[5,1]`; ordena a `[3,8]` y `[1,5]`; mezcla → `[1,3,5,8]`.
- **Complejidad:** mejor, promedio y peor caso `O(n log n)`; espacio auxiliar `O(n)` para arreglos.
- **Ventajas:** tiempo garantizado, estable y apropiado para datos grandes o cuando importa la estabilidad.
- **Desventajas / uso:** usa memoria adicional; normalmente no es la opción más económica para listas diminutas.
- **Código:** `merge_sort` en el script.

### Quick sort (ordenamiento rápido)

- **Necesidad:** ordenar con buen rendimiento práctico y poca memoria auxiliar en promedio.
- **Qué hace:** elige un pivote, separa elementos menores y mayores, y ordena recursivamente cada partición.
- **Traza** con `[8, 3, 5, 1]` y pivote `1`: particiona en `[]`, `1` y `[8,3,5]`; luego ordena esa partición → `[1,3,5,8]`.
- **Complejidad:** promedio y mejor caso `O(n log n)`; peor caso `O(n²)` si las particiones quedan muy desbalanceadas. Espacio promedio de pila `O(log n)`, peor `O(n)` en la versión recursiva.
- **Ventajas:** suele ser muy rápido en arreglos de tamaño mediano o grande y tiene buena localidad de memoria.
- **Desventajas / uso:** no es estable en esta implementación y un pivote desfavorable puede causar el peor caso. La versión educativa recursiva puede alcanzar el límite de recursión de Python con entradas grandes adversas.
- **Aclaración:** no se puede afirmar que sea “el mejor para datos pequeños” en general; insertion sort puede ser mejor con pocos elementos y una biblioteca optimizada puede superar implementaciones Python didácticas.
- **Código:** `quick_sort` en el script.

### Radix sort (ordenamiento por radix)

- **Necesidad:** ordenar claves enteras no negativas procesando sus dígitos, sin comparar pares de claves.
- **Qué hace:** ordena establemente por cada dígito, desde el menos significativo al más significativo.
- **Traza** con `[21, 13, 11]`: por unidades → `[21,11,13]`; por decenas → `[11,13,21]`.
- **Complejidad:** `O(d(n + b))`, donde `d` es la cantidad de dígitos y `b` la base (10 en el ejemplo); espacio `O(n+b)`. Con `d` acotado, se suele expresar como `O(n)`.
- **Ventajas:** puede ser lineal cuando la longitud de las claves está acotada y evita comparaciones entre valores.
- **Desventajas / uso:** esta implementación solo acepta enteros no negativos; claves largas o de longitud muy variable cambian el costo. No es “el mejor para volúmenes muy pequeños” por regla general: para esos casos, los costos de preparación pueden pesar más que el algoritmo.
- **Código:** `radix_sort` en el script.

### ¿Cuál ordenamiento conviene?

| Situación | Candidato razonable | Motivo y precaución |
|---|---|---|
| Pocos elementos o lista casi ordenada | Insertion sort | Bajo costo y mejor caso lineal. |
| Muchos elementos y memoria auxiliar aceptable | Merge sort | Garantiza `O(n log n)` y es estable. |
| Muchos elementos y buen rendimiento promedio | Quick sort | Suele ser rápido, pero el peor caso es cuadrático. |
| Enteros no negativos con cantidad de dígitos limitada | Radix sort | Puede evitar el `log n` de las comparaciones; depende de `d` y la base. |
| Código de producción en Python | `sorted()` / `list.sort()` | Implementación de biblioteca optimizada y estable; comparar contra código didáctico no es una comparación justa de algoritmos en abstracto. |

Para elegir por **tiempo medido**, ejecuta el benchmark del script con los mismos datos, en el mismo equipo y con varias repeticiones. Para decidir por **escala**, memoria y garantías, usa también el análisis teórico.

## 3. Acceso por clave

### Hash table (tabla hash)

- **Necesidad:** encontrar, insertar o eliminar un valor asociado a una clave sin recorrer normalmente todos los elementos.
- **Qué hace:** transforma la clave con una función hash y la usa para ubicar un bucket. El script maneja colisiones mediante encadenamiento (varias entradas pueden compartir bucket) y duplica la capacidad cuando la ocupación supera `0.75`.
- **Paso a paso:** insertar `"ana" → 42` calcula el bucket y guarda el par; insertar otra vez `"ana" → 43` actualiza el par; buscar `"ana"` calcula su bucket y devuelve `43`.
- **Complejidad:** búsqueda/inserción/eliminación promedio `O(1)` bajo una distribución razonable; peor caso `O(n)` si muchas claves colisionan. Espacio `O(n)`.
- **Ventajas:** acceso promedio rápido por clave.
- **Desventajas / uso:** no mantiene orden; requiere claves hashables y el peor caso no es constante. Usar cuando interesa consultar por clave; no cuando se necesita orden o búsqueda por rango.
- **Código:** `HashTable` (`put`, `get`, `delete`) en el script. En Python real, `dict` suele ser la opción habitual.

## 4. Estructuras lineales

Son estructuras cuyos elementos se organizan en una secuencia. La complejidad depende de la operación: insertar al principio no cuesta lo mismo que encontrar un elemento.

### Linked list (lista enlazada simple)

- **Necesidad:** representar una secuencia de nodos conectados, con inserciones/eliminaciones locales sin desplazar un arreglo.
- **Qué hace:** cada nodo guarda un valor y una referencia al siguiente.
- **Complejidad:** insertar al final `O(1)` si se conserva la cola; buscar/eliminar por valor `O(n)`; insertar al principio `O(1)`. Espacio `O(n)`.
- **Ventajas:** inserciones locales rápidas y tamaño dinámico.
- **Desventajas / uso:** no hay acceso aleatorio `O(1)`; cada nodo añade memoria. Útil si se modifica mucho mediante referencias a nodos; no es automáticamente mejor que `list`.
- **Paso a paso:** al añadir `1, 2, 3`, `head` apunta a `1`, y cada nodo enlaza al siguiente; buscar `3` revisa `1`, luego `2` y finalmente `3`.
- **Código:** `LinkedList` en el script.

### Doubly linked list (lista doblemente enlazada)

- **Necesidad:** recorrer en ambas direcciones y quitar un nodo conocido sin buscar su predecesor.
- **Qué hace:** cada nodo tiene referencias al anterior y al siguiente.
- **Complejidad:** añadir al final `O(1)` con referencia a cola; quitar un nodo conocido `O(1)`; buscar valor `O(n)`. Espacio `O(n)`.
- **Ventajas:** recorrido bidireccional y eliminación local directa.
- **Desventajas / uso:** mayor consumo de memoria y más referencias que mantener correctamente.
- **Paso a paso:** al añadir `1, 2, 3`, se conectan `1.next=2`, `2.previous=1`, `2.next=3` y `3.previous=2`; desde `3` se puede retroceder hasta `1`.
- **Código:** `DoublyLinkedList` en el script.

### Stack (pila)

- **Necesidad:** procesar elementos en orden LIFO: el último que entra es el primero que sale.
- **Qué hace:** `push` agrega arriba; `pop` y `peek` consultan o quitan el elemento superior.
- **Complejidad:** apilar, desapilar y consultar el tope `O(1)` amortizado con una lista dinámica. Espacio `O(n)`.
- **Usos:** llamadas, deshacer, análisis de expresiones y recorrido DFS iterativo.
- **Desventaja:** no está diseñada para buscar eficientemente en medio de sus elementos.
- **Paso a paso:** `push(A)`, `push(B)`, `pop()` devuelve `B`; queda `A` en el tope.
- **Código:** `Stack` en el script.

### Deque (cola de doble extremo)

- **Necesidad:** insertar y retirar eficientemente por ambos extremos.
- **Qué hace:** permite operaciones de cola al frente y al final; el script usa `collections.deque`.
- **Complejidad:** `append`, `appendleft`, `pop` y `popleft` son `O(1)` aproximadamente/amortizado según la operación. Buscar por índice o por valor es `O(n)`.
- **Usos:** colas FIFO, ventanas deslizantes y BFS.
- **Desventaja:** no es la estructura ideal para acceso aleatorio frecuente.
- **Paso a paso:** inicia `[2]`; agregar al frente `1` y al final `3` produce `[1,2,3]`; quitar por ambos extremos devuelve `1` y `3`.
- **Código:** `Deque` en el script.

## 5. Árboles y heaps

### BST (árbol binario de búsqueda)

- **Necesidad:** mantener claves ordenables para buscar y recorrerlas en orden.
- **Qué hace:** valores menores van al subárbol izquierdo y mayores al derecho; el recorrido in-order produce valores ordenados.
- **Complejidad:** búsqueda/inserción promedio `O(log n)` si el árbol está razonablemente balanceado; peor caso `O(n)` si se degrada a una cadena. Espacio `O(n)`.
- **Ventajas:** recorrido ordenado y búsqueda por rangos con estructura adecuada.
- **Desventajas / uso:** el BST simple no garantiza equilibrio. Si se insertan valores ya ordenados, puede degradarse.
- **Paso a paso:** insertar `3` lo vuelve raíz; `1` va a la izquierda y `4` a la derecha; insertar `2` compara con `3` y después `1`, así que queda a la derecha de `1`.
- **Código:** `BST` en el script.

### Balanced BST (BST balanceado AVL)

- **Necesidad:** evitar que la altura del BST se vuelva lineal.
- **Qué hace:** después de insertar, mide el balance de cada nodo y aplica rotaciones para mantener alturas similares.
- **Complejidad:** búsqueda e inserción `O(log n)` en el peor caso AVL; espacio `O(n)`.
- **Ventajas:** garantiza altura logarítmica y conserva recorrido ordenado.
- **Desventajas / uso:** rotaciones y mantenimiento hacen más compleja la implementación. Útil cuando se necesita orden y garantías logarítmicas.
- **Paso a paso:** insertar `3, 2, 1` produce desbalance a la izquierda en `3`; una rotación derecha deja `2` como raíz, con `1` y `3` como hijos.
- **Código:** `AVLTree` en el script. Implementa inserción y recorrido in-order.

### Heap sort (ordenamiento heapsort)

- **Necesidad:** ordenar con tiempo garantizado `O(n log n)` y espacio auxiliar constante.
- **Qué hace:** construye un max-heap y luego intercambia repetidamente la raíz (máximo) con el final, reduciendo el heap.
- **Traza:** en `[4, 1, 3]`, el max-heap coloca `4` en la raíz; al extraerlo al final queda `[3,1,4]`; extrae `3` → `[1,3,4]`.
- **Complejidad:** mejor, promedio y peor `O(n log n)`; espacio auxiliar `O(1)` en la implementación in-place.
- **Ventajas:** límite temporal garantizado y poco espacio.
- **Desventajas / uso:** no es estable y suele tener constantes/localidad menos favorables que los mejores ordenamientos prácticos.
- **Paso a paso:** para `[4,1,3]`, construye un max-heap con raíz `4`; intercambia `4` con el último elemento y repara el heap; continúa hasta que el prefijo restante está ordenado.
- **Código:** `heap_sort` en el script.

### Binary heap / max heap (montículo binario / máximo)

- **Necesidad:** obtener repetidamente el máximo con eficiencia.
- **Qué hace:** árbol binario casi completo almacenado en un arreglo; en un max-heap, cada padre es mayor o igual que sus hijos.
- **Complejidad:** consultar máximo `O(1)`; insertar y extraer máximo `O(log n)`; construir desde `n` elementos `O(n)`. Espacio `O(n)`.
- **Ventajas:** implementa colas de prioridad de manera compacta.
- **Desventajas / uso:** no mantiene todo el arreglo ordenado; buscar un valor arbitrario cuesta `O(n)`.
- **Paso a paso:** insertar `3,1,5` flota `5` hasta la raíz; extraerlo mueve el último elemento a la raíz y lo hunde hasta restaurar la propiedad de máximo.
- **Código:** `MaxHeap` en el script. Heapsort y max-heap están relacionados, pero no son sinónimos: heapsort usa la propiedad del heap para ordenar.

## 6. Grafos

Un grafo representa entidades (vértices) y sus relaciones (aristas). En el script se usa una lista de adyacencia.

### BFS (búsqueda en anchura)

- **Necesidad:** visitar un grafo por niveles y hallar caminos con menor cantidad de aristas en grafos no ponderados.
- **Qué hace:** comienza en un vértice, procesa primero sus vecinos y usa una cola para no perder el orden por niveles.
- **Traza** en `A:{B,C}, B:{D}, C:{}, D:{}`: desde `A`, visita `A`; encola `B,C`; procesa `B` y encola `D`; termina en el orden `A,B,C,D`.
- **Complejidad:** `O(V+E)` con listas de adyacencia; espacio `O(V)`.
- **Ventajas:** encuentra distancias mínimas en número de aristas si el grafo no tiene pesos.
- **Desventajas / uso:** no es la herramienta para caminos mínimos ponderados con pesos arbitrarios.
- **Código:** `BFS` en el script.

### DFS (búsqueda en profundidad)

- **Necesidad:** explorar componentes y estructura de grafos; sirve como base para ciclos, orden topológico y otras tareas.
- **Qué hace:** sigue un vecino no visitado tan lejos como puede, luego retrocede.
- **Traza** con el mismo grafo y vecinos en el orden indicado: visita `A`, baja a `B`, luego `D`, retrocede y visita `C`: `A,B,D,C`.
- **Complejidad:** `O(V+E)`; espacio `O(V)` entre visitados y pila/recursión.
- **Ventajas:** útil para explorar componentes y relaciones profundas.
- **Desventajas / uso:** el orden depende de los vecinos; DFS no garantiza el camino más corto. La versión del script es iterativa para evitar límites de recursión.
- **Código:** `DFS` en el script.

## Un extra

### Idempotencia

No es una estructura ni un algoritmo de ordenamiento: es una propiedad de una operación. Una operación es idempotente cuando repetirla con la misma solicitud deja el mismo estado que ejecutarla una sola vez. Por ejemplo, asignar `estado = "activo"` varias veces mantiene `"activo"`. En sistemas distribuidos, esta propiedad ayuda a reintentar solicitudes con seguridad. No debe confundirse “no hacer nada la segunda vez” con la definición: puede haber ejecución de nuevo, pero el estado final debe ser equivalente.

- **Costo del ejemplo:** asignar un estado cuesta `O(1)` por llamada.
- **Código:** `set_status` en el script.

### Búsqueda lineal

- **Necesidad:** encontrar un elemento sin asumir que los datos están ordenados.
- **Qué hace:** revisa elementos uno por uno hasta hallar el objetivo o terminar.
- **Complejidad:** peor y promedio `O(n)`; mejor `O(1)` si el primer elemento coincide; espacio `O(1)`.
- **Ventajas / uso:** sencilla y sirve en cualquier secuencia; conviene para colecciones pequeñas o desordenadas.
- **Desventajas:** crece linealmente con el tamaño.
- **Código:** `linear_search` en el script.

### Búsqueda binaria

- **Necesidad:** buscar en una secuencia ordenada reduciendo rápidamente el intervalo.
- **Qué hace:** compara con el elemento medio y descarta la mitad donde no puede estar el objetivo.
- **Traza** en `[1, 3, 5, 8, 9]` buscando `8`: medio `5` → busca a la derecha; medio `8` → encontrado.
- **Complejidad:** peor y promedio `O(log n)`; mejor `O(1)` si el primer medio coincide; espacio `O(1)` en la versión iterativa.
- **Ventajas / uso:** muy rápida en listas ordenadas con acceso por índice.
- **Desventajas:** exige datos ordenados; ordenar primero también cuesta tiempo y memoria.
- **Código:** `binary_search` en el script.
- **Paso a paso:** en `[1,3,5,8,9]`, buscar `8` compara el medio `5`, descarta la mitad izquierda y compara `8` en el intervalo restante.

## Cómo analizar casos

- **Mejor caso:** entrada más favorable para el algoritmo. Ejemplo: búsqueda lineal cuando el objetivo está primero (`O(1)`).
- **Caso promedio:** comportamiento esperado bajo una distribución de entradas definida. Hay que decir qué distribución se supone; “promedio” sin supuesto puede ser ambiguo.
- **Peor caso:** entrada que maximiza el trabajo para un tamaño `n`. Es importante cuando se necesitan garantías o se enfrentan entradas adversas.
- Al informar, define qué mide `n` y el modelo: por ejemplo, comparaciones, operaciones, memoria; para radix, usa también `d` (dígitos) y `b` (base), y para grafos `V` y `E`.
- `O(...)` describe crecimiento asintótico, no segundos exactos ni una predicción del tiempo para un equipo concreto.

## Medición del tiempo con `time`

El archivo usa `time.perf_counter()` para cronometrar los algoritmos de ordenamiento y búsqueda con los valores definidos en `VALUES_TO_TEST`, repite cada prueba y compara medianas. Cada algoritmo recibe datos equivalentes y se verifica que el resultado coincida. BFS y DFS se miden sobre un grafo lineal de tamaño igual a la cantidad de valores de esa lista.

Una medición casera puede variar por procesos activos, calentamiento del intérprete, tamaño de la muestra y costos de copia. Usa tamaños crecientes y varias repeticiones; no midas una sola ejecución diminuta y concluyas que ese algoritmo siempre es más rápido. Además, comparar una implementación educativa en Python con `sorted()` compara también calidad de implementación y optimización, no solo la idea algorítmica.

## Resumen de complejidad de peor caso

| Algoritmo / operación | Peor tiempo |
|---|---:|
| Bubble sort | `O(n²)` |
| Selection sort | `O(n²)` |
| Insertion sort | `O(n²)` |
| Merge sort | `O(n log n)` |
| Quick sort | `O(n²)` |
| Radix sort | `O(d(n+b))` |
| Hash table: buscar/insertar/eliminar | `O(n)` |
| Linked list: búsqueda por valor | `O(n)` |
| Doubly linked list: búsqueda por valor | `O(n)` |
| Stack: push/pop | `O(1)` amortizado |
| Deque: operaciones en extremos | `O(1)` |
| BST simple: buscar/insertar | `O(n)` |
| AVL: buscar/insertar | `O(log n)` |
| Heap sort | `O(n log n)` |
| Max-heap: insertar/extraer máximo | `O(log n)` |
| BFS / DFS | `O(V+E)` |
| Búsqueda lineal | `O(n)` |
| Búsqueda binaria | `O(log n)` |

### Nota para la entrega

Este documento y el script son material de estudio con implementaciones didácticas. Para el informe del parcial, añade los tiempos que obtengas al ejecutar el benchmark en tu entorno y explica por qué el tamaño y el tipo de datos afectan la elección. No declares un “ganador absoluto”: reporta el ganador observado para cada conjunto de condiciones.
