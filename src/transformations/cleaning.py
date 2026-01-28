# =============================================================================
# Transformaciones de limpieza de datos
# Big Data UAG 2026
# =============================================================================
"""
Funciones para limpiar y normalizar datos.
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StringType, TimestampType, DateType
from typing import List, Dict, Optional
import re


def clean_column_names(df: DataFrame) -> DataFrame:
    """
    Limpia los nombres de columnas (snake_case, sin espacios ni caracteres especiales).

    Parametros:
    -----------
    df : DataFrame
        DataFrame original

    Retorna:
    --------
    DataFrame
        DataFrame con nombres de columnas limpios

    Ejemplo:
    --------
    >>> df = clean_column_names(df)
    >>> # "Customer Name" -> "customer_name"
    >>> # "Order-ID" -> "order_id"
    """
    new_columns = []

    for col_name in df.columns:
        # Convertir a minusculas
        new_name = col_name.lower()
        # Reemplazar espacios y guiones por underscore
        new_name = re.sub(r'[\s\-\.]+', '_', new_name)
        # Eliminar caracteres especiales (excepto underscore)
        new_name = re.sub(r'[^a-z0-9_]', '', new_name)
        # Eliminar underscores multiples
        new_name = re.sub(r'_+', '_', new_name)
        # Eliminar underscores al inicio/final
        new_name = new_name.strip('_')

        new_columns.append(new_name)

    return df.toDF(*new_columns)


def remove_duplicates(
    df: DataFrame,
    subset: List[str] = None,
    keep: str = "first"
) -> DataFrame:
    """
    Elimina filas duplicadas.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    subset : List[str], opcional
        Columnas a considerar para duplicados (default: todas)
    keep : str
        Cual mantener: 'first', 'last' (nota: Spark solo soporta dropDuplicates)

    Retorna:
    --------
    DataFrame
        DataFrame sin duplicados

    Ejemplo:
    --------
    >>> df_clean = remove_duplicates(df, subset=["customer_id", "order_date"])
    """
    if subset:
        return df.dropDuplicates(subset)
    return df.dropDuplicates()


def fill_nulls(
    df: DataFrame,
    fill_values: Dict[str, any] = None,
    numeric_value: float = 0,
    string_value: str = "Unknown"
) -> DataFrame:
    """
    Rellena valores nulos.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    fill_values : Dict[str, any], opcional
        Diccionario {columna: valor} para valores especificos
    numeric_value : float
        Valor para columnas numericas (default: 0)
    string_value : str
        Valor para columnas string (default: "Unknown")

    Retorna:
    --------
    DataFrame
        DataFrame con nulos rellenados

    Ejemplo:
    --------
    >>> df = fill_nulls(df, fill_values={"price": 0, "category": "Other"})
    """
    if fill_values:
        return df.fillna(fill_values)

    # Rellenar por tipo de dato
    for field in df.schema.fields:
        if field.dataType in [StringType()]:
            df = df.fillna({field.name: string_value})
        elif "int" in str(field.dataType).lower() or "double" in str(field.dataType).lower():
            df = df.fillna({field.name: numeric_value})

    return df


def trim_strings(df: DataFrame, columns: List[str] = None) -> DataFrame:
    """
    Elimina espacios al inicio y final de strings.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    columns : List[str], opcional
        Columnas a limpiar (default: todas las columnas string)

    Retorna:
    --------
    DataFrame
        DataFrame con strings sin espacios extra

    Ejemplo:
    --------
    >>> df = trim_strings(df, ["name", "city"])
    """
    if columns is None:
        # Encontrar todas las columnas string
        columns = [
            field.name for field in df.schema.fields
            if isinstance(field.dataType, StringType)
        ]

    for col_name in columns:
        if col_name in df.columns:
            df = df.withColumn(col_name, F.trim(F.col(col_name)))

    return df


def standardize_dates(
    df: DataFrame,
    date_columns: List[str],
    input_formats: List[str] = None,
    output_format: str = "yyyy-MM-dd"
) -> DataFrame:
    """
    Estandariza columnas de fecha a un formato uniforme.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    date_columns : List[str]
        Columnas de fecha a estandarizar
    input_formats : List[str], opcional
        Formatos de entrada a probar (default: formatos comunes)
    output_format : str
        Formato de salida (default: "yyyy-MM-dd")

    Retorna:
    --------
    DataFrame
        DataFrame con fechas estandarizadas

    Ejemplo:
    --------
    >>> df = standardize_dates(df, ["order_date", "ship_date"])
    """
    if input_formats is None:
        input_formats = [
            "yyyy-MM-dd",
            "MM/dd/yyyy",
            "dd/MM/yyyy",
            "yyyy/MM/dd",
            "MM-dd-yyyy",
            "dd-MM-yyyy",
            "yyyyMMdd"
        ]

    for col_name in date_columns:
        if col_name in df.columns:
            # Intentar parsear con diferentes formatos
            parsed_col = None
            for fmt in input_formats:
                if parsed_col is None:
                    parsed_col = F.to_date(F.col(col_name), fmt)
                else:
                    parsed_col = F.coalesce(
                        parsed_col,
                        F.to_date(F.col(col_name), fmt)
                    )

            df = df.withColumn(col_name, parsed_col)

    return df


def cast_columns(df: DataFrame, type_mapping: Dict[str, str]) -> DataFrame:
    """
    Convierte tipos de datos de columnas.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    type_mapping : Dict[str, str]
        Diccionario {columna: tipo}
        Tipos: 'int', 'long', 'double', 'float', 'string', 'date', 'timestamp'

    Retorna:
    --------
    DataFrame
        DataFrame con tipos convertidos

    Ejemplo:
    --------
    >>> df = cast_columns(df, {"price": "double", "quantity": "int"})
    """
    for col_name, dtype in type_mapping.items():
        if col_name in df.columns:
            df = df.withColumn(col_name, F.col(col_name).cast(dtype))

    return df
