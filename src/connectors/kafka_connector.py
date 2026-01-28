# =============================================================================
# Conector para Apache Kafka
# Big Data UAG 2026
# =============================================================================
"""
Conectores para Apache Kafka usando Spark Structured Streaming.
"""

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql import functions as F
from pyspark.sql.types import StructType
from typing import Optional, Callable
import os
import json


def create_kafka_producer(bootstrap_servers: str = None):
    """
    Crea un productor de Kafka simple usando kafka-python.

    Parametros:
    -----------
    bootstrap_servers : str
        Servidores de Kafka (default: KAFKA_BOOTSTRAP_SERVERS o 'localhost:9092')

    Retorna:
    --------
    KafkaProducer
        Instancia del productor

    Ejemplo:
    --------
    >>> producer = create_kafka_producer()
    >>> producer.send('mi-topic', value=b'mensaje')
    >>> producer.flush()
    """
    from kafka import KafkaProducer

    servers = bootstrap_servers or os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    return KafkaProducer(
        bootstrap_servers=servers,
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )


def create_kafka_consumer(topic: str, bootstrap_servers: str = None, group_id: str = "bigdata-consumer"):
    """
    Crea un consumidor de Kafka simple usando kafka-python.

    Parametros:
    -----------
    topic : str
        Nombre del topic a consumir
    bootstrap_servers : str
        Servidores de Kafka
    group_id : str
        ID del grupo de consumidores

    Retorna:
    --------
    KafkaConsumer
        Instancia del consumidor

    Ejemplo:
    --------
    >>> consumer = create_kafka_consumer('mi-topic')
    >>> for msg in consumer:
    ...     print(msg.value)
    """
    from kafka import KafkaConsumer

    servers = bootstrap_servers or os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")

    return KafkaConsumer(
        topic,
        bootstrap_servers=servers,
        group_id=group_id,
        auto_offset_reset='earliest',
        value_deserializer=lambda v: json.loads(v.decode('utf-8'))
    )


class KafkaConnector:
    """
    Conector para Apache Kafka usando Spark Structured Streaming.

    Ejemplo:
    --------
    >>> kafka = KafkaConnector(spark)
    >>> df_stream = kafka.read_stream("sensor-data", schema)
    >>> kafka.write_stream(df_processed, "processed-data")
    """

    def __init__(
        self,
        spark: SparkSession,
        bootstrap_servers: str = None
    ):
        """
        Inicializa el conector a Kafka.

        Parametros:
        -----------
        spark : SparkSession
            Sesion de Spark activa
        bootstrap_servers : str, opcional
            Servidores de Kafka (default: KAFKA_BOOTSTRAP_SERVERS o 'kafka:29092')
        """
        self.spark = spark
        self.bootstrap_servers = bootstrap_servers or \
            os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "kafka:29092")

    def read_stream(
        self,
        topic: str,
        schema: StructType = None,
        starting_offsets: str = "earliest"
    ) -> DataFrame:
        """
        Lee un stream de Kafka.

        Parametros:
        -----------
        topic : str
            Nombre del topic
        schema : StructType, opcional
            Esquema para parsear el JSON del mensaje
        starting_offsets : str
            Desde donde empezar: 'earliest', 'latest'

        Retorna:
        --------
        DataFrame
            DataFrame de streaming
        """
        df = self.spark.readStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_servers) \
            .option("subscribe", topic) \
            .option("startingOffsets", starting_offsets) \
            .load()

        # Decodificar el valor como string
        df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")

        # Si hay esquema, parsear el JSON
        if schema:
            df = df.select(
                F.col("key"),
                F.from_json(F.col("value"), schema).alias("data"),
                F.col("timestamp")
            ).select("key", "data.*", "timestamp")

        return df

    def read_batch(
        self,
        topic: str,
        schema: StructType = None,
        starting_offsets: str = "earliest",
        ending_offsets: str = "latest"
    ) -> DataFrame:
        """
        Lee datos de Kafka en modo batch (no streaming).

        Parametros:
        -----------
        topic : str
            Nombre del topic
        schema : StructType, opcional
            Esquema para parsear JSON
        starting_offsets : str
            Offset inicial
        ending_offsets : str
            Offset final

        Retorna:
        --------
        DataFrame
            DataFrame con los datos
        """
        df = self.spark.read \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_servers) \
            .option("subscribe", topic) \
            .option("startingOffsets", starting_offsets) \
            .option("endingOffsets", ending_offsets) \
            .load()

        # Decodificar
        df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)", "timestamp")

        if schema:
            df = df.select(
                F.col("key"),
                F.from_json(F.col("value"), schema).alias("data"),
                F.col("timestamp")
            ).select("key", "data.*", "timestamp")

        return df

    def write_stream(
        self,
        df: DataFrame,
        topic: str,
        checkpoint_location: str,
        output_mode: str = "append",
        trigger_interval: str = "10 seconds"
    ):
        """
        Escribe un DataFrame de streaming a Kafka.

        Parametros:
        -----------
        df : DataFrame
            DataFrame de streaming
        topic : str
            Topic destino
        checkpoint_location : str
            Ruta para checkpoints
        output_mode : str
            Modo: 'append', 'complete', 'update'
        trigger_interval : str
            Intervalo de procesamiento

        Retorna:
        --------
        StreamingQuery
            Query de streaming
        """
        # Convertir a formato Kafka (key, value)
        df_kafka = df.select(
            F.to_json(F.struct("*")).alias("value")
        )

        return df_kafka.writeStream \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_servers) \
            .option("topic", topic) \
            .option("checkpointLocation", checkpoint_location) \
            .outputMode(output_mode) \
            .trigger(processingTime=trigger_interval) \
            .start()

    def write_batch(self, df: DataFrame, topic: str):
        """
        Escribe un DataFrame a Kafka en modo batch.

        Parametros:
        -----------
        df : DataFrame
            DataFrame a escribir
        topic : str
            Topic destino
        """
        df.select(
            F.to_json(F.struct("*")).alias("value")
        ).write \
            .format("kafka") \
            .option("kafka.bootstrap.servers", self.bootstrap_servers) \
            .option("topic", topic) \
            .save()

        print(f"✅ Datos escritos al topic '{topic}'")
