"""
Análisis para Tienda Aurelion.

El script realiza: limpieza, estadísticas descriptivas, distribuciones,
correlaciones, generación de gráficos.
"""

import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def _resolver_ruta(base_dir: Path, stem: str) -> Path:
    """Encuentra el archivo disponible para un dataset.

    Prioriza ``.xlsx`` (los archivos entregados) y acepta ``.csv`` como
    respaldo para mantener compatibilidad con ejecuciones previas.
    """

    for ext in (".xlsx", ".csv"):
        ruta = base_dir / f"{stem}{ext}"
        if ruta.exists():
            return ruta
    raise FileNotFoundError(f"No se encontró {stem}.xlsx ni {stem}.csv en {base_dir}")


def cargar_datos(base_dir: Path) -> tuple[dict[str, pd.DataFrame], dict[str, Path]]:
    """Carga los archivos de clientes, ventas, detalle y productos.

    Args:
        base_dir: Carpeta donde residen los archivos.

    Returns:
        Una tupla con el diccionario de dataframes y las rutas de origen.
    """
    
    stems = {
        "clientes": "Clientes",
        "ventas": "Ventas",
        "detalle": "Detalle_ventas",
        "productos": "Productos",
    }

    data: dict[str, pd.DataFrame] = {}
    rutas: dict[str, Path] = {}
    for nombre, stem in stems.items():
        ruta = _resolver_ruta(base_dir, stem)
        rutas[nombre] = ruta
        if ruta.suffix.lower() == ".xlsx":
            data[nombre] = pd.read_excel(ruta)
        else:
            data[nombre] = pd.read_csv(ruta)

    return data, rutas


def exportar_fuentes_csv(
    data: dict[str, pd.DataFrame], rutas: dict[str, Path], destino: Path
) -> None:
    """Convierte las fuentes Excel a CSV sin modificar los archivos originales."""

    destino.mkdir(parents=True, exist_ok=True)
    for nombre, df in data.items():
        if rutas.get(nombre, Path()).suffix.lower() == ".xlsx":
            df.to_csv(destino / f"{nombre}.csv", index=False)


def limpiar_datos(data: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    """Aplica reglas básicas de limpieza y prepara las tablas unificadas."""
    clientes = data["clientes"].copy()
    ventas = data["ventas"].copy()
    detalle = data["detalle"].copy()
    productos = data["productos"].copy()

    # Normalizar nombres de columnas en minúsculas
    for df in (clientes, ventas, detalle, productos):
        df.columns = [c.strip().lower() for c in df.columns]

    # Tipos
    for col in ("fecha_alta", "fecha"):
        if col in clientes:
            clientes[col] = pd.to_datetime(clientes[col], errors="coerce")
        if col in ventas:
            ventas[col] = pd.to_datetime(ventas[col], errors="coerce")

    for df, cols in ((detalle, ["cantidad", "precio_unitario", "importe"]), (productos, ["precio_unitario"])):
        for col in cols:
            if col in df:
                df[col] = pd.to_numeric(df[col], errors="coerce")

    # Eliminar duplicados exactos
    clientes = clientes.drop_duplicates()
    ventas = ventas.drop_duplicates()
    detalle = detalle.drop_duplicates()
    productos = productos.drop_duplicates()

    # Quitar registros con claves faltantes
    ventas = ventas.dropna(subset=["id_venta", "id_cliente"])
    detalle = detalle.dropna(subset=["id_venta", "id_producto"])
    productos = productos.dropna(subset=["id_producto"])

    # Consistencias básicas
    detalle = detalle[detalle["cantidad"] > 0]
    for col in ("precio_unitario", "importe"):
        if col in detalle:
            detalle = detalle[detalle[col] >= 0]
    if "precio_unitario" in productos:
        productos = productos[productos["precio_unitario"] >= 0]

    # Recalcular importe cuando falte o sea 0
    if {"cantidad", "precio_unitario"}.issubset(detalle.columns):
        detalle["importe_recalculado"] = detalle["cantidad"] * detalle["precio_unitario"]
        if "importe" not in detalle:
            detalle["importe"] = detalle["importe_recalculado"]
        else:
            detalle["importe"] = detalle["importe"].fillna(detalle["importe_recalculado"])
        detalle = detalle.drop(columns=["importe_recalculado"], errors="ignore")

    # Unificación
    detalle = detalle.merge(
        productos[["id_producto", "categoria", "precio_unitario"]].rename(columns={"precio_unitario": "precio_catalogo"}),
        on="id_producto",
        how="left",
    )
    detalle["precio_final"] = detalle["precio_unitario"].fillna(detalle["precio_catalogo"])
    detalle["importe"] = detalle["importe"].fillna(detalle["cantidad"] * detalle["precio_final"])

    ventas_detalle = ventas.merge(detalle, on="id_venta", how="left", suffixes=("_venta", "_detalle"))
    ventas_detalle = ventas_detalle.merge(clientes, on="id_cliente", how="left", suffixes=("", "_cliente"))

    return {
        "clientes": clientes,
        "ventas": ventas,
        "detalle": detalle,
        "ventas_detalle": ventas_detalle,
    }


def estadisticas_descriptivas(ventas_detalle: pd.DataFrame) -> dict[str, pd.Series]:
    """Calcula métricas descriptivas clave."""
    ventas_totales = ventas_detalle.groupby("id_venta")["importe"].sum()
    ticket_por_cliente = ventas_detalle.groupby("id_cliente")["importe"].sum()
    ticket_por_categoria = ventas_detalle.groupby("categoria")["importe"].sum()

    resumen_general = pd.Series({
        "ventas_registradas": ventas_totales.shape[0],
        "monto_total": ventas_totales.sum(),
        "ticket_promedio": ventas_totales.mean(),
        "productos_distintos": ventas_detalle["id_producto"].nunique(),
        "clientes_distintos": ventas_detalle["id_cliente"].nunique(),
    })

    return {
        "resumen_general": resumen_general,
        "ticket_por_venta": ventas_totales.describe(),
        "ticket_por_cliente": ticket_por_cliente.describe(),
        "importe_por_categoria": ticket_por_categoria.sort_values(ascending=False),
    }


def crear_distribuciones(ventas_detalle: pd.DataFrame, salida: Path) -> None:
    """Genera histogramas y distribuciones básicas."""
    salida.mkdir(parents=True, exist_ok=True)
    ventas_totales = ventas_detalle.groupby("id_venta")["importe"].sum()

    plt.figure(figsize=(8, 5))
    sns.histplot(ventas_totales, bins=20, kde=True, color="#4c72b0")
    plt.title("Distribución del ticket por venta")
    plt.xlabel("Monto de venta")
    plt.ylabel("Frecuencia")
    plt.tight_layout()
    plt.savefig(salida / "distribucion_ticket.png")
    plt.close()

    plt.figure(figsize=(8, 5))
    sns.countplot(
        data=ventas_detalle.drop_duplicates("id_venta"),
        x="medio_pago",
        hue="medio_pago",
        palette="viridis",
        legend=False,
    )
    plt.title("Ventas por medio de pago")
    plt.xlabel("Medio de pago")
    plt.ylabel("Número de ventas")
    plt.tight_layout()
    plt.savefig(salida / "ventas_por_medio_pago.png")
    plt.close()


def crear_correlaciones(ventas_detalle: pd.DataFrame, salida: Path) -> pd.DataFrame:
    """Calcula matriz de correlación y genera un heatmap."""
    salida.mkdir(parents=True, exist_ok=True)
    num_cols = [c for c in ["cantidad", "precio_final", "importe"] if c in ventas_detalle.columns]
    corr = ventas_detalle[num_cols].corr()

    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlación entre variables numéricas")
    plt.tight_layout()
    plt.savefig(salida / "correlaciones.png")
    plt.close()
    return corr


def crear_graficos(ventas_detalle: pd.DataFrame, salida: Path) -> None:
    """Crea gráficos adicionales de comportamiento temporal y por categoría."""
    salida.mkdir(parents=True, exist_ok=True)
    ventas_detalle["fecha"] = pd.to_datetime(ventas_detalle["fecha"], errors="coerce")
    ventas_detalle["mes"] = ventas_detalle["fecha"].dt.to_period("M")

    # Ventas por mes
    ventas_mensuales = ventas_detalle.groupby("mes")["importe"].sum().sort_index()
    plt.figure(figsize=(8, 5))
    ventas_mensuales.plot(kind="bar", color="#55a868")
    plt.title("Monto total vendido por mes")
    plt.xlabel("Mes")
    plt.ylabel("Importe")
    plt.tight_layout()
    plt.savefig(salida / "ventas_mensuales.png")
    plt.close()

    # Top categorías
    top_categorias = ventas_detalle.groupby("categoria")["importe"].sum().sort_values(ascending=False).head(10)
    plt.figure(figsize=(8, 5))
    top_categorias.plot(kind="bar", color="#c44e52")
    plt.title("Top categorías por importe vendido")
    plt.xlabel("Categoría")
    plt.ylabel("Importe acumulado")
    plt.tight_layout()
    plt.savefig(salida / "top_categorias.png")
    plt.close()

    # Precio vs cantidad
    plt.figure(figsize=(7, 5))
    sns.scatterplot(data=ventas_detalle, x="precio_final", y="cantidad", alpha=0.7)
    plt.title("Relación entre precio y cantidad")
    plt.xlabel("Precio")
    plt.ylabel("Cantidad")
    plt.tight_layout()
    plt.savefig(salida / "precio_vs_cantidad.png")
    plt.close()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    salida = base_dir / "resultados"
    salida.mkdir(exist_ok=True)

    data, rutas = cargar_datos(base_dir)
    data_limpia = limpiar_datos(data)
    ventas_detalle = data_limpia["ventas_detalle"]

    exportar_fuentes_csv(data, rutas, salida / "fuentes_csv")

    # Exportar versiones limpias
    for nombre, df in data_limpia.items():
        df.to_csv(salida / f"{nombre}_limpio.csv", index=False)

    stats = estadisticas_descriptivas(ventas_detalle)
    distribuciones_dir = salida / "distribuciones"
    correlaciones_dir = salida / "correlaciones"
    graficos_dir = salida / "graficos"

    crear_distribuciones(ventas_detalle, distribuciones_dir)
    corr = crear_correlaciones(ventas_detalle, correlaciones_dir)
    crear_graficos(ventas_detalle, graficos_dir)

    # Guardar estadísticas
    stats["resumen_general"].to_csv(salida / "resumen_general.csv")
    stats["ticket_por_venta"].to_csv(salida / "ticket_por_venta.csv")
    stats["ticket_por_cliente"].to_csv(salida / "ticket_por_cliente.csv")
    stats["importe_por_categoria"].to_csv(salida / "importe_por_categoria.csv")
    corr.to_csv(salida / "matriz_correlacion.csv")

    print("=== Estadísticas descriptivas ===")
    print(stats["resumen_general"].to_string())

if __name__ == "__main__":
    main()
