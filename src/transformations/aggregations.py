# =============================================================================
# Transformaciones de agregacion
# Big Data UAG 2026
# =============================================================================
"""
Funciones para agregaciones y calculos estadisticos.
"""

from pyspark.sql import DataFrame, Window
from pyspark.sql import functions as F
from typing import List, Dict, Optional


def calculate_statistics(
    df: DataFrame,
    numeric_columns: List[str] = None
) -> DataFrame:
    """
    Calcula estadisticas descriptivas para columnas numericas.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    numeric_columns : List[str], opcional
        Columnas a analizar (default: todas las numericas)

    Retorna:
    --------
    DataFrame
        DataFrame con estadisticas (count, mean, std, min, max, etc.)

    Ejemplo:
    --------
    >>> stats = calculate_statistics(df, ["price", "quantity"])
    >>> stats.show()
    """
    if numeric_columns is None:
        # Encontrar columnas numericas
        numeric_columns = [
            field.name for field in df.schema.fields
            if "int" in str(field.dataType).lower()
            or "double" in str(field.dataType).lower()
            or "float" in str(field.dataType).lower()
        ]

    return df.select(numeric_columns).describe()


def group_and_aggregate(
    df: DataFrame,
    group_by: List[str],
    aggregations: Dict[str, List[str]]
) -> DataFrame:
    """
    Agrupa y aplica multiples agregaciones.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    group_by : List[str]
        Columnas para agrupar
    aggregations : Dict[str, List[str]]
        Diccionario {columna: [funciones]}
        Funciones: 'sum', 'avg', 'min', 'max', 'count', 'first', 'last'

    Retorna:
    --------
    DataFrame
        DataFrame agregado

    Ejemplo:
    --------
    >>> df_agg = group_and_aggregate(
    ...     df,
    ...     group_by=["category", "year"],
    ...     aggregations={
    ...         "price": ["sum", "avg"],
    ...         "quantity": ["sum", "count"]
    ...     }
    ... )
    """
    # Construir lista de agregaciones
    agg_exprs = []

    func_map = {
        'sum': F.sum,
        'avg': F.avg,
        'mean': F.avg,
        'min': F.min,
        'max': F.max,
        'count': F.count,
        'first': F.first,
        'last': F.last,
        'stddev': F.stddev,
        'variance': F.variance
    }

    for col_name, funcs in aggregations.items():
        for func_name in funcs:
            if func_name in func_map:
                alias = f"{col_name}_{func_name}"
                agg_exprs.append(
                    func_map[func_name](F.col(col_name)).alias(alias)
                )

    return df.groupBy(group_by).agg(*agg_exprs)


def rolling_window(
    df: DataFrame,
    partition_by: List[str],
    order_by: str,
    column: str,
    window_size: int,
    func: str = "avg"
) -> DataFrame:
    """
    Calcula una funcion de ventana deslizante.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    partition_by : List[str]
        Columnas para particionar
    order_by : str
        Columna para ordenar
    column : str
        Columna a calcular
    window_size : int
        Tamano de la ventana (filas)
    func : str
        Funcion: 'avg', 'sum', 'min', 'max', 'count'

    Retorna:
    --------
    DataFrame
        DataFrame con columna de ventana agregada

    Ejemplo:
    --------
    >>> df = rolling_window(
    ...     df,
    ...     partition_by=["product_id"],
    ...     order_by="date",
    ...     column="sales",
    ...     window_size=7,
    ...     func="avg"
    ... )
    """
    # Definir la ventana
    window_spec = Window \
        .partitionBy(partition_by) \
        .orderBy(order_by) \
        .rowsBetween(-(window_size - 1), 0)

    # Mapeo de funciones
    func_map = {
        'avg': F.avg,
        'sum': F.sum,
        'min': F.min,
        'max': F.max,
        'count': F.count
    }

    if func not in func_map:
        raise ValueError(f"Funcion '{func}' no soportada. Use: {list(func_map.keys())}")

    # Aplicar la funcion de ventana
    new_col_name = f"{column}_{func}_{window_size}"
    return df.withColumn(
        new_col_name,
        func_map[func](F.col(column)).over(window_spec)
    )


def cumulative_sum(
    df: DataFrame,
    partition_by: List[str],
    order_by: str,
    column: str
) -> DataFrame:
    """
    Calcula la suma acumulada.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    partition_by : List[str]
        Columnas para particionar
    order_by : str
        Columna para ordenar
    column : str
        Columna a sumar

    Retorna:
    --------
    DataFrame
        DataFrame con suma acumulada

    Ejemplo:
    --------
    >>> df = cumulative_sum(df, ["customer_id"], "date", "amount")
    """
    window_spec = Window \
        .partitionBy(partition_by) \
        .orderBy(order_by) \
        .rowsBetween(Window.unboundedPreceding, Window.currentRow)

    new_col_name = f"{column}_cumsum"
    return df.withColumn(
        new_col_name,
        F.sum(F.col(column)).over(window_spec)
    )


def rank_within_group(
    df: DataFrame,
    partition_by: List[str],
    order_by: str,
    ascending: bool = False,
    rank_type: str = "rank"
) -> DataFrame:
    """
    Calcula ranking dentro de grupos.

    Parametros:
    -----------
    df : DataFrame
        DataFrame original
    partition_by : List[str]
        Columnas para particionar
    order_by : str
        Columna para ordenar
    ascending : bool
        Si True, menor valor = mejor rank
    rank_type : str
        Tipo: 'rank', 'dense_rank', 'row_number', 'percent_rank'

    Retorna:
    --------
    DataFrame
        DataFrame con columna de ranking

    Ejemplo:
    --------
    >>> df = rank_within_group(
    ...     df,
    ...     partition_by=["category"],
    ...     order_by="sales",
    ...     ascending=False
    ... )
    """
    # Definir orden
    if ascending:
        order_col = F.col(order_by).asc()
    else:
        order_col = F.col(order_by).desc()

    window_spec = Window \
        .partitionBy(partition_by) \
        .orderBy(order_col)

    # Mapeo de tipos de ranking
    rank_funcs = {
        'rank': F.rank,
        'dense_rank': F.dense_rank,
        'row_number': F.row_number,
        'percent_rank': F.percent_rank
    }

    if rank_type not in rank_funcs:
        raise ValueError(f"Tipo '{rank_type}' no soportado. Use: {list(rank_funcs.keys())}")

    return df.withColumn(
        f"{rank_type}_by_{order_by}",
        rank_funcs[rank_type]().over(window_spec)
    )
