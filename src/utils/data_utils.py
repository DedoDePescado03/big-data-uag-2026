# =============================================================================
# Utilidades para manejo de datos
# Big Data UAG 2026
# =============================================================================
"""
Funciones de utilidad para cargar y guardar datos en diferentes formatos.
"""

from pyspark.sql import SparkSession, DataFrame
from pathlib import Path
from typing import Optional, List, Dict, Any
import os


def get_data_path(
    folder: str = "",
    filename: str = "",
    data_type: str = "raw"
) -> str:
    """
    Obtiene la ruta al directorio de datos.

    Parametros:
    -----------
    folder : str
        Subcarpeta dentro del directorio de datos
    filename : str
        Nombre del archivo (opcional)
    data_type : str
        Tipo de datos: 'raw', 'processed', 'sample'

    Retorna:
    --------
    str
        Ruta completa al archivo o directorio

    Ejemplo:
    --------
    >>> path = get_data_path("01_data_fundamentals", "train.csv", "raw")
    >>> print(path)
    /home/jovyan/data/raw/01_data_fundamentals/train.csv
    """
    # Directorio base de datos (funciona tanto en Docker como local)
    base_paths = [
        "/home/jovyan/data",    # Docker Jupyter
        "/data",                # Docker Spark
        str(Path.home() / "Documents/big-data-uag-2026/data"),  # Local
        "./data"                # Relativo
    ]

    # Encontrar el directorio base que existe
    base_path = None
    for path in base_paths:
        if os.path.exists(path):
            base_path = path
            break

    if base_path is None:
        base_path = "./data"  # Default

    # Construir ruta completa
    full_path = Path(base_path) / data_type

    if folder:
        full_path = full_path / folder

    if filename:
        full_path = full_path / filename

    return str(full_path)


def load_csv_to_spark(
    spark: SparkSession,
    path: str,
    header: bool = True,
    infer_schema: bool = True,
    delimiter: str = ",",
    encoding: str = "utf-8",
    null_value: str = "",
    **kwargs
) -> DataFrame:
    """
    Carga un archivo CSV en un DataFrame de Spark.

    Parametros:
    -----------
    spark : SparkSession
        Sesion de Spark activa
    path : str
        Ruta al archivo CSV (puede usar wildcards como *.csv)
    header : bool
        Si el archivo tiene encabezados
    infer_schema : bool
        Si debe inferir tipos de datos automaticamente
    delimiter : str
        Separador de campos (default: coma)
    encoding : str
        Codificacion del archivo
    null_value : str
        Valor que representa nulo
    **kwargs
        Argumentos adicionales para spark.read.csv()

    Retorna:
    --------
    DataFrame
        DataFrame de Spark con los datos

    Ejemplo:
    --------
    >>> df = load_csv_to_spark(spark, "/data/raw/ventas.csv")
    >>> df.show(5)
    """
    return spark.read.csv(
        path,
        header=header,
        inferSchema=infer_schema,
        sep=delimiter,
        encoding=encoding,
        nullValue=null_value,
        **kwargs
    )


def save_to_parquet(
    df: DataFrame,
    path: str,
    mode: str = "overwrite",
    partition_by: Optional[List[str]] = None,
    compression: str = "snappy"
):
    """
    Guarda un DataFrame en formato Parquet.

    Parametros:
    -----------
    df : DataFrame
        DataFrame a guardar
    path : str
        Ruta destino
    mode : str
        Modo de escritura: 'overwrite', 'append', 'ignore', 'error'
    partition_by : List[str], opcional
        Columnas para particionar
    compression : str
        Algoritmo de compresion: 'snappy', 'gzip', 'lz4', 'none'

    Ejemplo:
    --------
    >>> save_to_parquet(df, "/data/processed/ventas.parquet", partition_by=["year", "month"])
    """
    writer = df.write.mode(mode).option("compression", compression)

    if partition_by:
        writer = writer.partitionBy(*partition_by)

    writer.parquet(path)
    print(f"✅ Datos guardados en: {path}")


def save_to_delta(
    df: DataFrame,
    path: str,
    mode: str = "overwrite",
    partition_by: Optional[List[str]] = None,
    merge_schema: bool = True
):
    """
    Guarda un DataFrame en formato Delta Lake.

    Parametros:
    -----------
    df : DataFrame
        DataFrame a guardar
    path : str
        Ruta destino
    mode : str
        Modo de escritura: 'overwrite', 'append', 'ignore', 'error'
    partition_by : List[str], opcional
        Columnas para particionar
    merge_schema : bool
        Si debe hacer merge de esquema en caso de cambios

    Ejemplo:
    --------
    >>> save_to_delta(df, "/data/processed/ventas_delta", partition_by=["date"])
    """
    writer = df.write.format("delta").mode(mode)

    if merge_schema:
        writer = writer.option("mergeSchema", "true")

    if partition_by:
        writer = writer.partitionBy(*partition_by)

    writer.save(path)
    print(f"✅ Datos guardados en Delta: {path}")


def load_sample_data(spark: SparkSession) -> Dict[str, DataFrame]:
    """
    Carga todos los datasets de ejemplo disponibles.

    Parametros:
    -----------
    spark : SparkSession
        Sesion de Spark activa

    Retorna:
    --------
    Dict[str, DataFrame]
        Diccionario con los DataFrames cargados

    Ejemplo:
    --------
    >>> data = load_sample_data(spark)
    >>> data["sales"].show()
    """
    sample_path = get_data_path(data_type="sample")
    datasets = {}

    if os.path.exists(sample_path):
        for file in Path(sample_path).glob("*.csv"):
            name = file.stem
            datasets[name] = load_csv_to_spark(spark, str(file))
            print(f"📁 Cargado: {name} ({datasets[name].count()} filas)")

    return datasets
