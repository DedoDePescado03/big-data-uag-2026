# =============================================================================
# Utilidades para Apache Spark
# Big Data UAG 2026
# =============================================================================
"""
Funciones de utilidad para crear y gestionar sesiones de Spark.
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from typing import Optional
import os


def create_spark_session(
    app_name: str = "BigDataUAG",
    master: str = None,
    enable_delta: bool = True,
    enable_hive: bool = False,
    memory: str = "2g",
    cores: str = "2"
) -> SparkSession:
    """
    Crea una sesion de Spark configurada para el entorno del curso.

    Parametros:
    -----------
    app_name : str
        Nombre de la aplicacion Spark (aparece en la UI)
    master : str, opcional
        URL del master. Si es None, usa la variable de entorno SPARK_MASTER
        o 'local[*]' por defecto
    enable_delta : bool
        Si True, configura soporte para Delta Lake
    enable_hive : bool
        Si True, habilita soporte para Hive metastore
    memory : str
        Memoria del driver (ej: '2g', '4g')
    cores : str
        Numero de cores para modo local (ej: '2', '*')

    Retorna:
    --------
    SparkSession
        Sesion de Spark configurada

    Ejemplo:
    --------
    >>> spark = create_spark_session("MiApp", enable_delta=True)
    >>> df = spark.read.csv("/data/sample.csv", header=True)
    """
    # Determinar el master URL
    if master is None:
        master = os.environ.get("SPARK_MASTER", f"local[{cores}]")

    # Construir la sesion
    builder = SparkSession.builder \
        .appName(app_name) \
        .master(master) \
        .config("spark.driver.memory", memory) \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")

    # Configuracion para Delta Lake
    if enable_delta:
        builder = builder \
            .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")

    # Habilitar Hive si se requiere
    if enable_hive:
        builder = builder.enableHiveSupport()

    # Crear y retornar la sesion
    spark = builder.getOrCreate()

    # Configurar nivel de log (reducir verbosidad)
    spark.sparkContext.setLogLevel("WARN")

    return spark


def get_spark_session() -> Optional[SparkSession]:
    """
    Obtiene la sesion de Spark activa.

    Retorna:
    --------
    SparkSession o None
        La sesion activa o None si no hay ninguna

    Ejemplo:
    --------
    >>> spark = get_spark_session()
    >>> if spark:
    ...     print("Spark esta activo")
    """
    return SparkSession.getActiveSession()


def stop_spark_session():
    """
    Detiene la sesion de Spark activa.

    Ejemplo:
    --------
    >>> stop_spark_session()
    >>> print("Spark detenido")
    """
    spark = get_spark_session()
    if spark:
        spark.stop()


def show_dataframe_info(df: DataFrame, name: str = "DataFrame"):
    """
    Muestra informacion detallada de un DataFrame.

    Parametros:
    -----------
    df : DataFrame
        DataFrame de Spark a analizar
    name : str
        Nombre descriptivo del DataFrame

    Ejemplo:
    --------
    >>> show_dataframe_info(df_ventas, "Ventas 2024")
    === Ventas 2024 ===
    Filas: 1,000,000
    Columnas: 15
    Particiones: 8
    ...
    """
    print(f"\n{'='*50}")
    print(f"  {name}")
    print(f"{'='*50}")

    # Contar filas (cacheado si es posible)
    row_count = df.count()

    print(f"\n📊 Estadisticas basicas:")
    print(f"   Filas: {row_count:,}")
    print(f"   Columnas: {len(df.columns)}")
    print(f"   Particiones: {df.rdd.getNumPartitions()}")

    print(f"\n📋 Esquema:")
    df.printSchema()

    print(f"\n🔍 Muestra de datos (5 filas):")
    df.show(5, truncate=50)

    # Estadisticas de nulos
    print(f"\n❓ Valores nulos por columna:")
    null_counts = df.select([
        F.sum(F.when(F.col(c).isNull(), 1).otherwise(0)).alias(c)
        for c in df.columns
    ]).collect()[0]

    for col_name in df.columns:
        null_count = null_counts[col_name]
        if null_count > 0:
            pct = (null_count / row_count) * 100
            print(f"   {col_name}: {null_count:,} ({pct:.1f}%)")

    print(f"\n{'='*50}\n")
