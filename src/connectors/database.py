# =============================================================================
# Conector para bases de datos
# Big Data UAG 2026
# =============================================================================
"""
Conectores para PostgreSQL y otras bases de datos.
"""

from pyspark.sql import SparkSession, DataFrame
from typing import Optional, Dict, Any
import os


def get_jdbc_url(
    host: str = "localhost",
    port: int = 5432,
    database: str = "datawarehouse",
    driver: str = "postgresql"
) -> str:
    """
    Genera una URL JDBC para conexion a base de datos.

    Parametros:
    -----------
    host : str
        Hostname del servidor
    port : int
        Puerto de la base de datos
    database : str
        Nombre de la base de datos
    driver : str
        Tipo de base de datos: 'postgresql', 'mysql'

    Retorna:
    --------
    str
        URL JDBC formateada

    Ejemplo:
    --------
    >>> url = get_jdbc_url("postgres", 5432, "mydb")
    >>> print(url)
    jdbc:postgresql://postgres:5432/mydb
    """
    return f"jdbc:{driver}://{host}:{port}/{database}"


class PostgresConnector:
    """
    Conector para PostgreSQL usando Spark JDBC.

    Ejemplo:
    --------
    >>> pg = PostgresConnector(spark)
    >>> df = pg.read_table("ventas")
    >>> pg.write_table(df_nuevo, "ventas_procesadas")
    """

    def __init__(
        self,
        spark: SparkSession,
        host: str = None,
        port: int = 5432,
        database: str = "datawarehouse",
        user: str = None,
        password: str = None
    ):
        """
        Inicializa el conector a PostgreSQL.

        Parametros:
        -----------
        spark : SparkSession
            Sesion de Spark activa
        host : str, opcional
            Hostname (default: variable POSTGRES_HOST o 'postgres')
        port : int
            Puerto (default: 5432)
        database : str
            Nombre de la base de datos
        user : str, opcional
            Usuario (default: variable POSTGRES_USER o 'bigdata')
        password : str, opcional
            Contrasena (default: variable POSTGRES_PASSWORD o 'bigdata123')
        """
        self.spark = spark
        self.host = host or os.environ.get("POSTGRES_HOST", "postgres")
        self.port = port
        self.database = database
        self.user = user or os.environ.get("POSTGRES_USER", "bigdata")
        self.password = password or os.environ.get("POSTGRES_PASSWORD", "bigdata123")

        self.jdbc_url = get_jdbc_url(self.host, self.port, self.database)
        self.driver = "org.postgresql.Driver"

    def read_table(self, table: str, **kwargs) -> DataFrame:
        """
        Lee una tabla de PostgreSQL.

        Parametros:
        -----------
        table : str
            Nombre de la tabla
        **kwargs
            Argumentos adicionales (fetchsize, partitionColumn, etc.)

        Retorna:
        --------
        DataFrame
            Datos de la tabla
        """
        return self.spark.read \
            .format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("dbtable", table) \
            .option("user", self.user) \
            .option("password", self.password) \
            .option("driver", self.driver) \
            .options(**kwargs) \
            .load()

    def read_query(self, query: str) -> DataFrame:
        """
        Ejecuta una consulta SQL y retorna los resultados.

        Parametros:
        -----------
        query : str
            Consulta SQL

        Retorna:
        --------
        DataFrame
            Resultados de la consulta
        """
        return self.spark.read \
            .format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("query", query) \
            .option("user", self.user) \
            .option("password", self.password) \
            .option("driver", self.driver) \
            .load()

    def write_table(
        self,
        df: DataFrame,
        table: str,
        mode: str = "overwrite",
        **kwargs
    ):
        """
        Escribe un DataFrame a PostgreSQL.

        Parametros:
        -----------
        df : DataFrame
            DataFrame a escribir
        table : str
            Nombre de la tabla destino
        mode : str
            Modo de escritura: 'overwrite', 'append', 'ignore', 'error'
        """
        df.write \
            .format("jdbc") \
            .option("url", self.jdbc_url) \
            .option("dbtable", table) \
            .option("user", self.user) \
            .option("password", self.password) \
            .option("driver", self.driver) \
            .options(**kwargs) \
            .mode(mode) \
            .save()

        print(f"✅ Tabla '{table}' guardada en PostgreSQL")

    def get_tables(self) -> DataFrame:
        """
        Lista todas las tablas en la base de datos.

        Retorna:
        --------
        DataFrame
            Lista de tablas
        """
        query = """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
        """
        return self.read_query(query)
