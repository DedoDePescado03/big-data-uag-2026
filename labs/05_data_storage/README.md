# Módulo 05: Almacenamiento de Datos

## Descripción

Este módulo cubre los diferentes formatos y estrategias de almacenamiento para Big Data, incluyendo data lakes, formatos columnares y Delta Lake.

## Objetivos de Aprendizaje

Al completar este módulo podrás:
- Comparar formatos de archivo (CSV, JSON, Parquet, ORC, Avro)
- Diseñar estrategias de particionamiento
- Implementar Delta Lake para almacenamiento transaccional
- Optimizar lecturas y escrituras de datos

## Módulo AWS Academy Relacionado

📚 **Módulo 8: Data Storage and Management**
- Amazon S3 para data lakes
- Formatos de archivo optimizados
- Particionamiento y organización

## Dataset

**Amazon Fine Food Reviews**
- Fuente: Kaggle `snap/amazon-fine-food-reviews`
- ~500K reviews de productos de Amazon
- Datos de texto para análisis

## Contenido

| Notebook | Descripción | Tiempo |
|----------|-------------|--------|
| `01_file_formats.ipynb` | Comparación de formatos | 45 min |
| `02_partitioning.ipynb` | Estrategias de particionamiento | 45 min |
| `03_delta_lake.ipynb` | Introducción a Delta Lake | 60 min |
| `04_data_lake_design.ipynb` | Diseño de data lakes | 45 min |

## Formatos de Archivo

| Formato | Tipo | Compresión | Esquema | Uso Principal |
|---------|------|------------|---------|---------------|
| CSV | Texto | No/Gzip | No | Intercambio simple |
| JSON | Texto | No/Gzip | Embebido | APIs, logs |
| Parquet | Columnar | Snappy/Gzip | Sí | Analytics |
| ORC | Columnar | Zlib/Snappy | Sí | Hive/Hadoop |
| Avro | Row-based | Snappy | Sí | Streaming |
| Delta | Columnar+ | Snappy | Sí | Transaccional |

## Arquitectura Data Lake

```
data/
├── raw/                    # Datos crudos (inmutables)
│   ├── year=2024/
│   │   ├── month=01/
│   │   └── month=02/
│   └── year=2023/
├── processed/              # Datos limpios
│   └── partitioned by date
├── curated/                # Datos listos para análisis
│   └── aggregated tables
└── delta/                  # Tablas Delta Lake
    └── transactional tables
```

## Comandos Útiles

```bash
# Descargar dataset
python infrastructure/scripts/download-datasets.py --lab 05

# Ver tamaño de archivos
du -sh data/raw/05_data_storage/*

# Comparar tamaños de formatos
ls -lh data/processed/
```

## Delta Lake Features

- **ACID Transactions**: Operaciones atómicas
- **Schema Evolution**: Cambios de esquema seguros
- **Time Travel**: Acceso a versiones anteriores
- **Unified Batch/Streaming**: Mismo formato para ambos
- **Data Versioning**: Historial completo

## Conexión con AWS

| Concepto Local | Servicio AWS | Descripción |
|----------------|--------------|-------------|
| Parquet files | S3 + Athena | Queries SQL sobre S3 |
| Delta Lake | S3 + EMR | Tablas transaccionales |
| Partitioning | S3 prefixes | Organización de datos |
| Data Lake | Lake Formation | Gobernanza de data lake |

## Siguiente Módulo

Continúa con:
- `06_spark_processing/` - Procesamiento con Spark
