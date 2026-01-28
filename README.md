# Big Data UAG 2026

Repositorio de prácticas para el curso AWS Academy Data Engineering.

## Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/agusvillarreal/big-data-uag-2026.git
cd big-data-uag-2026

# 2. Iniciar cluster Spark + Jupyter
./infrastructure/scripts/start-cluster.sh spark

# 3. Abrir Jupyter Lab
open http://localhost:8888

# 4. Navegar a labs/ y comenzar con 00_setup/
```

## Acceso a Servicios

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Jupyter Lab | http://localhost:8888 | Entorno de notebooks |
| Spark Master UI | http://localhost:8080 | Monitoreo del cluster |
| Spark Worker UI | http://localhost:8081 | Estado del worker |
| Spark App UI | http://localhost:4040 | UI de aplicación activa |
| Kafka UI | http://localhost:9000 | Administración de Kafka |
| MinIO Console | http://localhost:9001 | Storage S3-compatible |

## Estructura del Proyecto

```
big-data-uag-2026/
├── labs/                           # Notebooks de práctica
│   ├── 00_setup/                   # Configuración inicial
│   ├── 01_data_fundamentals/       # Fundamentos de datos
│   ├── 02_etl_pipeline/            # Pipelines ETL
│   ├── 03_batch_processing/        # Procesamiento batch
│   ├── 04_streaming_simulation/    # Streaming simulado
│   ├── 05_data_storage/            # Almacenamiento de datos
│   ├── 06_spark_processing/        # Apache Spark
│   ├── 07_ml_data_preparation/     # Preparación para ML
│   ├── 08_visualization_analysis/  # Visualización
│   └── 09_project_iot_pipeline/    # Proyecto final IoT
├── infrastructure/                 # Docker y scripts
│   ├── docker-compose.spark.yml    # Cluster Spark
│   ├── docker-compose.kafka.yml    # Cluster Kafka
│   ├── docker-compose.full-stack.yml # Stack completo
│   └── scripts/                    # Scripts de utilidad
├── data/                           # Datasets
│   ├── raw/                        # Datos sin procesar
│   ├── processed/                  # Datos procesados
│   └── sample/                     # Datos de ejemplo
├── src/                            # Código reutilizable
│   ├── utils/                      # Utilidades Spark
│   ├── connectors/                 # Conectores DB/Kafka
│   └── transformations/            # Transformaciones
└── docs/                           # Documentación
```

## Comandos Comunes

```bash
# Iniciar solo Spark + Jupyter
./infrastructure/scripts/start-cluster.sh spark

# Iniciar Kafka (para labs de streaming)
./infrastructure/scripts/start-cluster.sh kafka

# Iniciar todo (Spark + Kafka + PostgreSQL + Redis + MinIO)
./infrastructure/scripts/start-cluster.sh full

# Detener servicios
./infrastructure/scripts/stop-cluster.sh

# Descargar datasets de Kaggle
python infrastructure/scripts/download-datasets.py

# Crear solo datos de ejemplo (sin Kaggle)
python infrastructure/scripts/download-datasets.py --sample
```

## Requisitos

- Docker Desktop
- 8GB RAM mínimo (16GB recomendado)
- 20GB espacio en disco
- Cuenta de Kaggle (para datasets completos)

## Stack Tecnológico

- **PySpark 3.5** - Procesamiento distribuido
- **Delta Lake** - Storage transaccional
- **Jupyter Lab** - Entorno interactivo
- **Kafka** - Streaming de datos
- **PostgreSQL** - Base de datos relacional
- **MinIO** - Storage compatible con S3

## Documentación Adicional

- [Guía de Docker](docs/docker-guide.md) - Tutorial completo de Docker
- [AWS Academy Data Engineering](https://awsacademy.instructure.com/) - Curso oficial

## Mapeo con AWS Academy

| Lab Local | Módulo AWS | Tema Principal |
|-----------|------------|----------------|
| 00_setup | - | Configuración |
| 01_data_fundamentals | M03 | 5 Vs, tipos de datos |
| 02_etl_pipeline | M06 | ETL/ELT, data wrangling |
| 03_batch_processing | M07 | Batch vs streaming |
| 04_streaming_simulation | M07 | Kinesis, streaming |
| 05_data_storage | M08 | S3, data lake, formatos |
| 06_spark_processing | M09 | EMR, Hadoop, Spark |
| 07_ml_data_preparation | M10 | SageMaker, feature eng |
| 08_visualization_analysis | M11 | Athena, QuickSight |
| 09_project_iot_pipeline | IoT | Pipeline completo |
