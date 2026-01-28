# =============================================================================
# Dockerfile para Apache Spark
# Big Data UAG 2026 - AWS Academy Data Engineering
# =============================================================================

FROM bitnami/spark:3.5

# Metadata
LABEL maintainer="Big Data UAG 2026"
LABEL description="Apache Spark 3.5 con soporte para Delta Lake y conectores"

USER root

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Crear directorios de trabajo
RUN mkdir -p /data /labs /src && \
    chmod -R 777 /data /labs /src

# Descargar JARs necesarios para Delta Lake y conectores
WORKDIR /opt/bitnami/spark/jars

# Delta Lake
RUN wget -q https://repo1.maven.org/maven2/io/delta/delta-spark_2.12/3.1.0/delta-spark_2.12-3.1.0.jar && \
    wget -q https://repo1.maven.org/maven2/io/delta/delta-storage/3.1.0/delta-storage-3.1.0.jar

# Kafka connector
RUN wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-sql-kafka-0-10_2.12/3.5.0/spark-sql-kafka-0-10_2.12-3.5.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/kafka/kafka-clients/3.5.0/kafka-clients-3.5.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/spark/spark-token-provider-kafka-0-10_2.12/3.5.0/spark-token-provider-kafka-0-10_2.12-3.5.0.jar && \
    wget -q https://repo1.maven.org/maven2/org/apache/commons/commons-pool2/2.11.1/commons-pool2-2.11.1.jar

# PostgreSQL JDBC
RUN wget -q https://repo1.maven.org/maven2/org/postgresql/postgresql/42.6.0/postgresql-42.6.0.jar

# AWS S3 (para MinIO)
RUN wget -q https://repo1.maven.org/maven2/org/apache/hadoop/hadoop-aws/3.3.4/hadoop-aws-3.3.4.jar && \
    wget -q https://repo1.maven.org/maven2/com/amazonaws/aws-java-sdk-bundle/1.12.262/aws-java-sdk-bundle-1.12.262.jar

USER 1001

WORKDIR /opt/bitnami/spark

# Configuracion de Spark para Delta Lake
ENV SPARK_CONF_DIR=/opt/bitnami/spark/conf
