# Asistente_documentacion.py
# Asistente interactivo para consultar la documentación del proyecto Tienda Aurelion

# Librerías

from IPython.display import Image, display

# MENU PRINCIPAL

def menu_principal():
    while True:
        print("\n=== DOCUMENTACIÓN DEL PROYECTO - TIENDA AURELION ===")
        print("Bienvenidos/as al asistente interactivo de documentación\n")
        print("1. Planteamiento General")
        print("2. Base de Datos")
        print("3. Programa en Python")
        print("4. Sugerencias Copilot")
        print("5. Alcance de análisis estadístico")
        print("0. Salir")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            menu_planteamiento()
        elif opcion == "2":
            menu_base_datos()
        elif opcion == "3":
            menu_programa()
        elif opcion == "4":
            menu_copilot()
        elif opcion == "5":
            menu_estadisticas()
        elif opcion == "0":
            print("\nCerrando el asistente.")
            break
        else:
            print("Opción no válida. Intente nuevamente.")

# 1. PLANTEAMIENTO GENERAL

def menu_planteamiento():
    while True:
        print("\n1. PLANTEAMIENTO GENERAL")
        print("1. Tema")
        print("2. Problema")
        print("3. Solución")
        print("0. Volver al menú principal")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\nTEMA:")
            print("Análisis del comportamiento de compra de los clientes en Tienda Aurelion, con el objetivo de identificar patrones que optimicen la experiencia de compra y el valor promedio por cliente, a partir de las ventas registradas entre enero y junio de 2024, utilizando la base de datos de Clientes, Ventas, Detalle_ventas y Productos.")
        elif opcion == "2":
            print("\nPROBLEMA:")
            print("En Tienda Aurelion no se cuenta con un análisis que permita comprender los factores que determinan el valor promedio de compra. La falta de métricas consolidadas dificulta la toma de decisiones comerciales y estratégicas, como la planificación de promociones, la definición de productos complementarios y la fidelización de clientes con mayor potencial de gasto.")
        elif opcion == "3":
            print("\nSOLUCIÓN:")
            print("Se propone desarrollar una herramienta analítica interactiva en Python que integre y analice los datos de Clientes, Ventas, Detalle_ventas y Productos. El sistema permitirá identificar patrones de compra, calcular indicadores como el ticket promedio por cliente o producto, y ofrecer una visión integral del rendimiento comercial.Con esta información, la empresa podrá diseñar estrategias más efectivas, optimizar promociones y fortalecer la relación con sus clientes claves.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

# 2. BASE DE DATOS

def menu_base_datos():
    while True:
        print("\n2. BASE DE DATOS")
        print("1. Fuente")
        print("2. Definición")
        print("3. Estructura")
        print("4. Tipos")
        print("5. Escala")
        print("0. Volver al menú principal")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\nFUENTE:")
            print("Los datos utilizados provienen de los archivos Clientes.xlsx, Ventas.xlsx, Detalle_ventas.xlsx y Productos.xlsx, brindados por el programa Fundamentos en Inteligencia Artificial – IBM SkillsBuild & Guayerd (2025).")
        elif opcion == "2":
            print("\nDEFINICIÓN:")
            print("La base de datos representa la información comercial de Tienda Aurelion, integrando los registros de clientes, productos y ventas realizadas entre enero y junio de 2024. Su propósito es centralizar los datos necesarios para analizar el ticket promedio, la frecuencia de compra y los patrones de consumo.")
        elif opcion == "3":
            print("\nESTRUCTURA:")
            print("El modelo está compuesto por cuatro tablas principales: \n")
            print("- Clientes: información de identificación y ubicación de cada cliente.\n"
                  "- Ventas: registro de transacciones y métodos de pago.\n"
                  "- Detalle_ventas: detalle de los productos vendidos en cada operación.\n"
                  "- Productos: catálogo de artículos, categorías y precios.\n\n"
                  "Las tablas se relacionan mediante claves primarias y foráneas:\n"
                  "- id_cliente (Clientes → Ventas)\n"
                  "- id_venta (Ventas → Detalle_ventas)\n"
                  "- id_producto (Productos → Detalle_ventas)")
        elif opcion == "4":
            print("\nTIPOS:")
            print("Los datos son estructurados y almacenados en formato .xlsx. Incluyen variables numéricas, de texto y de fecha, adecuadas para su procesamiento en Python.")
        elif opcion == "5":
            print("\nESCALA:")
            print("- Nominal: nombres, categorías, medios de pago.\n"
                  "- Intervalo: fechas de ventas y registro de clientes.\n"
                  "- Razón: precios, cantidades e importes.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

# 3. PROGRAMA EN PYTHON

def menu_programa():
    while True:
        print("\n3. PROGRAMA EN PYTHON")
        print("1. Pasos")
        print("2. Pseudocódigo")
        print("3. Diagrama")
        print("0. Volver al menú principal")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\nPASOS:")
            print("1. Detectar y cargar archivos .xlsx, con alternativa .csv si no están disponibles.\n"
                  "2. Normalizar nombres/tipos, eliminar duplicados y registros con claves faltantes,\n"
                  "   asegurar valores positivos y recalcular importes faltantes.\n"
                  "3. Unificar Detalle_ventas con Productos y Clientes para construir ventas_detalle.\n"
                  "4. Exportar las fuentes a CSV y guardar versiones *_limpio.csv depuradas.\n"
                  "5. Calcular métricas descriptivas: resumen general, ticket por venta/cliente e importe por categoría.\n"
                  "6. Generar visualizaciones: distribución del ticket, ventas por medio de pago y matriz de correlación.\n"
                  "7. Guardar las métricas en CSV e imprimir el resumen general en consola.")
        elif opcion == "2":
            print("\nPSEUDOCÓDIGO:")
            print("INICIO\n"
                  "      ESCRIBIR \"=== ANÁLISIS DE VENTAS - TIENDA AURELION ===\"\n"
                  "      ESCRIBIR \"Cargando datos...\"\n\n"
                  "      // 1. CARGA DE DATOS \n"
                  "      LEER CLIENTES.xlsx/CSV, VENTAS.xlsx/CSV, DETALLE_VENTAS.xlsx/CSV, PRODUCTOS.xlsx/CSV\n\n"
                  "      // 2. LIMPIEZA Y TIPOS\n"
                  "      NORMALIZAR columnas, convertir fechas y montos\n"
                  "      ELIMINAR duplicados y registros sin claves\n"
                  "      RECALCULAR importes faltantes\n\n"
                  "      // 3. UNIFICACIÓN\n"
                  "      UNIR detalle + productos por id_producto\n"
                  "      UNIR con clientes por id_cliente → ventas_detalle\n\n"
                  "      // 4. EXPORTACIONES\n"
                  "      GUARDAR fuentes en CSV\n"
                  "      GUARDAR archivos *_limpio.csv\n\n"
                  "      // 5. MÉTRICAS\n"
                  "      CALCULAR resumen_general, ticket_por_venta, ticket_por_cliente, importe_por_categoria\n\n"
                  "      // 6. VISUALIZACIONES\n"
                  "      GENERAR histograma, gráfico por medio de pago y heatmap de correlaciones\n\n"
                  "      // 7. SALIDAS\n"
                  "      EXPORTAR CSV de métricas y correlaciones\n"
                  "      IMPRIMIR resumen_general\n\n"
                  "FIN")
        elif opcion == "3":
            print("\nDIAGRAMA:")
            display(Image(filename='Diagrama.png'))
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

# 5. ALCANCE DE ANÁLISIS ESTADÍSTICO

def menu_estadisticas():
    while True:
        print("\n5. ALCANCE DE ANÁLISIS ESTADÍSTICO")
        print("1. Estadísticas descriptivas")
        print("2. Distribución de variables principales")
        print("3. Correlaciones")
        print("0. Volver al menú principal")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\nESTADÍSTICAS DESCRIPTIVAS:")
            print("- Ventas registradas: 120\n"
                  "- Monto total vendido: S/ 2,651,417\n"
                  "- Ticket promedio por venta: S/ 22,095.14\n"
                  "- Productos distintos vendidos: 95\n"
                  "- Clientes distintos: 67\n\n"
                  "Interpretación: ventas de alto valor con pocas transacciones, lo que eleva el ticket promedio.")
        elif opcion == "2":
            print("\nDISTRIBUCIÓN DE VARIABLES PRINCIPALES:")
            print("- El histograma del ticket por venta está sesgado a la derecha, con la mayoría entre S/ 10,000 y S/ 25,000.\n"
                  "- Hay tickets altos (~S/ 60,000) que actúan como outliers positivos.\n"
                  "- Se incluye un gráfico de ventas por medio de pago para comparar preferencias.")
            display(Image(filename='distribucion_ticket.png'))
            display(Image(filename='ventas_por_medio_pago.png'))
        elif opcion == "3":
            print("\nCORRELACIONES:")
            print("Se analiza la relación entre cantidad, precio_final e importe, mostrando el heatmap generado.")
            display(Image(filename='correlaciones.png'))
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

# 4. SUGERENCIAS COPILOT

def menu_copilot():
    while True:
        print("\n4. SUGERENCIAS COPILOT")
        print("1. Sugerencias aceptadas")
        print("2. Sugerencias descartadas")
        print("0. Volver al menú principal")
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            print("\nACEPTADAS:")
            print("- Correción de ortografía y redacción.\n"
                  "- Detalle con precisión de la base de datos.\n"
                  "- División por secciones.")
        elif opcion == "2":
            print("\nDESCARTADAS:")
            print("- Uso de minúsculas en el pseudocódigo.\n"
                  "- Archivo de requisitos.txt.\n"
                  "- Reglas de validación de los datos.")
        elif opcion == "0":
            break
        else:
            print("Opción no válida.")

# EJECUCIÓN PRINCIPAL

if __name__ == "__main__":
    menu_principal()
