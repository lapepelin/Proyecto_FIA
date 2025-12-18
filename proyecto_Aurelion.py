"""
Análisis para Tienda Aurelion.

El script realiza: limpieza, estadísticas descriptivas, distribuciones,
correlaciones, generación de gráficos.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split


def _resolver_ruta(base_dir: Path, stem: str) -> Path:
    """Encuentra el archivo Excel disponible para un dataset."""

    ruta = base_dir / f"{stem}.xlsx"
    if ruta.exists():
        return ruta
    raise FileNotFoundError(f"No se encontró {stem}.xlsx en {base_dir}")

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
        data[nombre] = pd.read_excel(ruta)

    return data, rutas


def exportar_fuentes_csv(
    data: dict[str, pd.DataFrame], rutas: dict[str, Path], destino: Path
) -> None:
    """Convierte los Excel a CSV y los deja en un directorio plano.
    Los archivos mantienen el nombre original y no se crean subcarpetas.
    """

    for nombre, df in data.items():
        ruta_origen = rutas.get(nombre, Path())
        if ruta_origen.suffix.lower() == ".xlsx":
            df.to_csv(destino / f"{ruta_origen.stem}.csv", index=False)


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

    # Enriquecer el detalle con información del catálogo de productos
    if "id_producto" in detalle.columns and "id_producto" in productos.columns:
        columnas_productos = [
            col
            for col in ("id_producto", "categoria", "precio_unitario")
            if col in productos.columns
        ]
        productos_unicos = productos[columnas_productos].drop_duplicates(
            subset=["id_producto"]
        )
        detalle = detalle.merge(
            productos_unicos, on="id_producto", how="left", suffixes=("", "_prod")
        )

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
    if "categoria" in ventas_detalle.columns:
        ticket_por_categoria = ventas_detalle.groupby("categoria")["importe"].sum()
    else:
        ticket_por_categoria = pd.Series(dtype=float)

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
    num_cols = [c for c in ["cantidad", "importe"] if c in ventas_detalle.columns]
    corr = ventas_detalle[num_cols].corr()

    plt.figure(figsize=(6, 4))
    sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlación entre variables numéricas")
    plt.tight_layout()
    plt.savefig(salida / "correlaciones.png")
    plt.close()
    return corr

def main() -> None:
    base_dir = Path(__file__).resolve().parent
    salida = base_dir

    data, rutas = cargar_datos(base_dir)
    data_limpia = limpiar_datos(data)
    ventas_detalle = data_limpia["ventas_detalle"]

    exportar_fuentes_csv(data, rutas, salida)

    # Exportar versiones limpias
    for nombre, df in data_limpia.items():
        base_nombre = rutas.get(nombre, Path()).stem if nombre in rutas else nombre
        df.to_csv(salida / f"{base_nombre}_limpio.csv", index=False)

    stats = estadisticas_descriptivas(ventas_detalle)
    crear_distribuciones(ventas_detalle, salida)
    corr = crear_correlaciones(ventas_detalle, salida)

    # Guardar estadísticas
    stats["resumen_general"].to_csv(salida / "resumen_general.csv")
    stats["ticket_por_venta"].to_csv(salida / "ticket_por_venta.csv")
    stats["ticket_por_cliente"].to_csv(salida / "ticket_por_cliente.csv")
    stats["importe_por_categoria"].to_csv(salida / "importe_por_categoria.csv")
    corr.to_csv(salida / "matriz_correlacion.csv")

    print("=== Estadísticas descriptivas ===")
    print(stats["resumen_general"].to_string())

    # Modelo de regresión lineal para estimar el importe
    df_ml = data_limpia["detalle"].copy()
    if "categoria" in df_ml:
        df_ml = pd.get_dummies(df_ml, columns=["categoria"], drop_first=True)

    variables_basicas = [col for col in ("cantidad", "precio_unitario") if col in df_ml]
    variables_categorias = [col for col in df_ml.columns if col.startswith("categoria_")]
    columnas_modelo = variables_basicas + variables_categorias

    if not columnas_modelo:
        raise ValueError("No hay columnas disponibles para entrenar el modelo")

    X = df_ml[columnas_modelo]
    y = df_ml["importe"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    modelo_aurelion = LinearRegression()
    modelo_aurelion.fit(X_train, y_train)

    y_pred = modelo_aurelion.predict(X_test)
    print(f"R2 Score: {r2_score(y_test, y_pred):.2f}")
    print(f"MAE: {mean_absolute_error(y_test, y_pred):.2f}")

if __name__ == "__main__":
    main()
