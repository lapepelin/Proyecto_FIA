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
            print("1. Cargar datos: leer Clientes.xlsx, Ventas.xlsx, Detalle_ventas.xlsx, Productos.xlsx.\n"
                  "2. Validar: tipos (fechas/números), nulos, duplicados clave, cantidades/precios > 0, fechas dentro de enero y junio 2024.\n"
                  "3. Unir:\n"
                  "   Ventas ↔ Detalle_ventas (por id_venta)\n"
                  "   Ventas ↔ Clientes (por id_cliente)\n"
                  "   Ventas ↔ Productos (por id_producto)\n"
                  "4. Calcular métricas:\n"
                  "   - Importe línea = cantidad * precio_unitario\n"
                  "   - Ticket por venta = suma importes por id_venta\n"
                  "   - Ticket promedio por cliente y por categoría\n"
                  "5. Consultas interactivas:\n"
                  "   Generales, por cliente, por categoría, top productos.\n"
                  "6. Exportar resultados filtrados (CSV/XLSX).\n"
                  "7. Registrar errores/advertencias (log simple).")
        elif opcion == "2":
            print("\nPSEUDOCÓDIGO:")
            print("INICIO\n"
                  "      ESCRIBIR \"=== ANÁLISIS DE VENTAS - TIENDA AURELION ===\"\n"
                  "      ESCRIBIR \"Cargando datos...\"\n\n"
                  "      // 1. CARGA DE DATOS \n"
                  "      LEER archivo CLIENTES.xlsx\n"
                  "      LEER archivo VENTAS.xlsx\n"
                  "      LEER archivo DETALLE_VENTAS.xlsx\n"
                  "      LEER archivo PRODUCTOS.xlsx\n\n"
                  "     // 2. VALIDACIONES BÁSICAS"
                  "     VALIDAR que no existan campos nulos en claves principales\n"
                  "     VALIDAR que las fechas estén entre ENERO y JUNIO de 2024\n"
                  "     VALIDAR que precios y cantidades sean mayores a 0\n\n"
                  "     // 3. UNIÓN DE TABLAS\n"
                  "     UNIR VENTAS con DETALLE_VENTAS por id_venta\n"
                  "     UNIR resultado con PRODUCTOS por id_producto\n"
                  "     UNIR resultado con CLIENTES por id_cliente\n\n"
                  "     // 4. CÁLCULOS PRINCIPALES\n"
                  "     PARA cada registro EN tabla_unida HACER\n"
                  "       importe_linea ← cantidad * precio_unitario\n"
                  "     FIN PARA\n"
                  "     AGRUPAR por id_venta → calcular total_venta\n"
                  "     AGRUPAR por id_cliente → calcular ticket_promedio_cliente\n"
                  "     AGRUPAR por categoria → calcular ticket_promedio_categoria\n\n"
                  "     // 5. MENÚ INTERACTIVO\n"
                  "     REPETIR\n"
                  "         ESCRIBIR \"1. Ver métricas generales\"\n"
                  "         ESCRIBIR \"2. Consultar por cliente\"\n"
                  "         ESCRIBIR \"3. Consultar por categoría\"\n"
                  "         ESCRIBIR \"4. Ver top productos\"\n"
                  "         ESCRIBIR \"5. Exportar resultados\"\n"
                  "         ESCRIBIR \"0. Salir\"\n"
                  "         LEER opcion\n\n"
                  "         SEGÚN opcion HACER\n"
                  "             CASO 1:\n"
                  "                 MOSTRAR ticket_promedio_global, top_clientes, top_categorias\n"
                  "             CASO 2:\n"
                  "                 LEER id_cliente\n"
                  "                 MOSTRAR ventas y ticket del cliente\n"
                  "             CASO 3:\n"
                  "                 LEER categoria\n"
                  "                 MOSTRAR ticket promedio y productos más vendidos\n"
                  "             CASO 4:\n"
                  "                 MOSTRAR productos con mayor importe_total\n"
                  "             CASO 5:\n"
                  "                 EXPORTAR resultados a archivo Excel\n"
                  "             CASO 0:\n"
                  "                 ESCRIBIR \"Programa finalizado.\"\n"
                  "             DE OTRO MODO:\n"
                  "                 ESCRIBIR \"Opción no válida\"\n"
                  "         FINSEGÚN\n"
                  "     HASTA opcion = 0\n\n"
                  "FIN")
        elif opcion == "3":
            print("\nDIAGRAMA:")
            display(Image(filename='Diagrama.png'))
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
