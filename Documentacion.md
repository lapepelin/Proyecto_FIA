# Documentación del Proyecto

## 1. Planteamiento General

### Tema:

Análisis del comportamiento de compra de los clientes en Tienda Aurelion con el objetivo de identificar patrones que optimicen la experiencia de compra y el valor promedio por cliente, a partir de las ventas registradas entre enero y junio de 2024, utilizando la base de datos de Clientes, Ventas, Detalle_ventas y Productos.

### Problema:

En Tienda Aurelion no se cuenta con un análisis que permita comprender los factores que determinan el valor promedio de compra. La falta de métricas consolidadas dificulta la toma de decisiones comerciales y estratégicas, como la planificación de promociones, la definición de productos complementarios y la fidelización de clientes con mayor potencial de gasto.

### Solución:

Se desarrolla una herramienta analítica interactiva en Python que integra y analiza los datos de Clientes, Ventas, Detalle_ventas y Productos. El sistema identifica patrones de compra, calcula indicadores como el ticket promedio por cliente o producto y ofrece una visión integral del rendimiento comercial. Con esta información, la empresa puede diseñar estrategias más efectivas, optimizar promociones y fortalecer la relación con sus clientes clave.

## 2. Base de Datos

### Fuente:

Los datos provienen de los archivos Clientes.xlsx, Ventas.xlsx, Detalle_ventas.xlsx y Productos.xlsx, brindados por el programa Fundamentos en Inteligencia Artificial – IBM SkillsBuild & Guayerd (2025).

### Definición:

La base de datos integra los registros de clientes, productos y ventas realizadas entre enero y junio de 2024. Su propósito es centralizar los datos necesarios para analizar el ticket promedio, la frecuencia de compra y los patrones de consumo.

### Estructura:

El modelo está compuesto por cuatro tablas principales:

- **Clientes:** información de identificación y ubicación de cada cliente.
- **Ventas:** registro de transacciones y métodos de pago.
- **Detalle_ventas:** detalle de los productos vendidos en cada operación.
- **Productos:** catálogo de artículos, categorías y precios.

Relaciones clave:

- `id_cliente` (Clientes → Ventas)
- `id_venta` (Ventas → Detalle_ventas)
- `id_producto` (Productos → Detalle_ventas)

### Tipos:

Los datos son estructurados y almacenados en formato .xlsx. Incluyen variables numéricas, de texto y de fecha, adecuadas para su procesamiento en Python.

### Escala:

- **Nominal:** nombres, categorías, medios de pago.
- **Intervalo:** fechas de ventas y registro de clientes.
- **Razón:** precios, cantidades e importes.

## 3. Programa en Python

### Pasos:

1. Detectar y cargar las fuentes de datos, priorizando los archivos `.xlsx` y aceptando `.csv` como respaldo.
2. Normalizar nombres y tipos de columnas, eliminar duplicados, descartar registros con claves faltantes y asegurar valores positivos en cantidades/precios. Se recalculan importes faltantes y se sincronizan precios con el catálogo de productos.
3. Unificar Detalle_ventas con Productos (por `id_producto`) y con Clientes (por `id_cliente`) para obtener la tabla consolidada `ventas_detalle`.
4. Exportar los archivos fuente a CSV y generar versiones limpias (`*_limpio.csv`).
5. Calcular métricas descriptivas: resumen general, ticket por venta, ticket por cliente e importe por categoría.
6. Generar visualizaciones: distribución del ticket por venta, ventas por medio de pago y matriz de correlación.
7. Guardar las salidas en CSV (`resumen_general.csv`, `ticket_por_venta.csv`, etc.) e imprimir el resumen general en consola.

### Pseudocódigo:

```pseint
INICIO

    ESCRIBIR "=== ANÁLISIS DE VENTAS - TIENDA AURELION ==="
    ESCRIBIR "Cargando datos..."

    // 1. CARGA DE DATOS
    LEER CLIENTES.xlsx (o CSV) → df_clientes
    LEER VENTAS.xlsx (o CSV) → df_ventas
    LEER DETALLE_VENTAS.xlsx (o CSV) → df_detalle
    LEER PRODUCTOS.xlsx (o CSV) → df_productos

    // 2. LIMPIEZA Y TIPOS
    NORMALIZAR nombres de columnas en minúsculas
    CONVERTIR fechas y montos numéricos
    ELIMINAR duplicados
    DESCARTAR registros con claves nulas y valores negativos
    RECALCULAR importes faltantes a partir de cantidad * precio

    // 3. UNIFICACIÓN
    UNIR df_detalle con df_productos (id_producto)
    UNIR con df_clientes (id_cliente)
    OBTENER tabla ventas_detalle

    // 4. EXPORTACIONES
    GUARDAR versiones CSV de las fuentes
    GUARDAR archivos *_limpio.csv con datos depurados

    // 5. MÉTRICAS
    CALCULAR ventas_registradas, monto_total, ticket_promedio
    CALCULAR ticket_por_venta, ticket_por_cliente, importe_por_categoria

    // 6. VISUALIZACIONES
    CREAR histograma del ticket por venta
    CREAR gráfico de ventas por medio de pago
    CREAR heatmap de correlaciones

    // 7. SALIDAS
    EXPORTAR CSV de métricas y matriz de correlación
    IMPRIMIR resumen_general en consola

FIN
```

### Diagrama:

Gráfico: `Diagrama.png`

## 4. Sugerencias Copilot

### Aceptadas:

- Corrección de ortografía y redacción.
- Detalle con precisión de la base de datos.
- División por secciones.

### Descartadas:

- Uso de minúsculas en el pseudocódigo.
- Archivo de requisitos.txt.
- Reglas de validación de los datos.

## 5. Alcance de análisis estadístico

### 5.1 Estadísticas descriptivas

Se calcularon métricas de tendencia central y dispersión para entender el volumen y comportamiento general de las ventas:

- **Ventas registradas:** 120
- **Monto total vendido:** S/ 2,651,417
- **Ticket promedio por venta:** S/ 22,095.14
- **Productos distintos vendidos:** 95
- **Clientes distintos:** 67

Estas métricas muestran un modelo de ventas con **pocas transacciones pero de alto valor**, lo cual incrementa de manera importante el ticket promedio.

### 5.2 Distribución de variables principales

El histograma del **ticket por venta** evidencia una **distribución sesgada hacia la derecha**, típica en negocios donde existen tickets elevados pero poco frecuentes.

Hallazgos clave:

- La mayor parte de las ventas se concentra entre **S/ 10,000 y S/ 25,000**.
- Existen tickets altos (hasta ~S/ 60,000) que funcionan como **outliers positivos**.
- La curva KDE refuerza la presencia de una cola hacia la derecha, indicando ventas atípicas de alto valor.

**Gráfico:** `distribucion_ticket.png`

El gráfico de barras de **ventas por medio de pago** muestra la preferencia relativa de cada opción registrada en las ventas únicas.

**Gráfico:** `ventas_por_medio_pago.png`

### 5.3 Correlaciones

Se evaluaron las relaciones entre las variables numéricas disponibles en el detalle de ventas (por defecto, *cantidad* e *importe*):

- **Cantidad vs. Importe:** correlación positiva que refleja que compras con más unidades tienden a generar montos más altos.
- **Otras variables numéricas:** si el dataset incluye precios finales, se incorporan al cálculo y al heatmap para observar su interacción con el importe.

**Gráfico:** `correlaciones.png`

### 5.4 Outliers

El análisis visual reveló la presencia de valores extremos, principalmente:

- **Tickets de venta superiores a S/ 40,000**, poco frecuentes.
- **Variaciones excepcionales en la cantidad adquirida**, asociadas a compras puntuales.
- **Categorías con importes acumulados atípicamente altos** (observado en el análisis de categorías).

Estos outliers pueden deberse a **ventas especiales, compras mayoristas o pedidos corporativos**.

### 5.5 Gráficos representativos

Los gráficos que resumen los hallazgos del análisis son:

1. **Distribución del ticket por venta** (`distribucion_ticket.png`).
2. **Ventas por medio de pago** (`ventas_por_medio_pago.png`).
3. **Heatmap de correlaciones** (`correlaciones.png`).

Cada visualización aporta un enfoque distinto: distribución de ventas, comportamiento de medios de pago y relación entre variables numéricas.

### 5.6 Interpretación orientada al negocio

El análisis evidencia que Tienda Aurelion opera con un **modelo de ventas de alto valor**, donde un número reducido de transacciones representa una elevada facturación total.

La combinación de productos premium, compras en volúmenes moderados y la presencia de tickets extraordinariamente altos sugiere oportunidades en:

- **Optimización de precios**.
- **Segmentación de clientes de alto valor**.
- **Promociones dirigidas según medio de pago**.
- **Enfoque en categorías con mayor aporte a la facturación**.

Los resultados permiten comprender mejor el comportamiento de compra y las variables que impulsan los ingresos.