# Módulo 06: Procesamiento con Apache Spark

## Descripción

Este módulo cubre el procesamiento de datos a gran escala usando Apache Spark. Aprenderás desde los fundamentos de RDDs hasta técnicas avanzadas de optimización.

## Objetivos de Aprendizaje

Al completar este módulo podrás:
- Entender la arquitectura y modelo de ejecución de Spark
- Trabajar con RDDs y DataFrames
- Escribir consultas SQL eficientes en Spark
- Realizar joins y agregaciones complejas
- Usar funciones de ventana para análisis avanzado
- Optimizar jobs de Spark para mejor rendimiento

## Módulo AWS Academy Relacionado

📚 **Módulo 9: Big Data Processing**
- Amazon EMR (Elastic MapReduce)
- Apache Hadoop y Spark en AWS
- Procesamiento distribuido

## Contenido

| Notebook | Descripción | Tiempo | Nivel |
|----------|-------------|--------|-------|
| `01_rdd_fundamentals.ipynb` | Fundamentos de RDDs | 45 min | Básico |
| `02_dataframes_api.ipynb` | API de DataFrames en profundidad | 60 min | Básico |
| `03_spark_sql.ipynb` | SQL en Spark | 45 min | Intermedio |
| `04_joins_aggregations.ipynb` | Joins y agregaciones complejas | 60 min | Intermedio |
| `05_window_functions.ipynb` | Funciones de ventana | 45 min | Avanzado |
| `06_optimization_techniques.ipynb` | Técnicas de optimización | 60 min | Avanzado |

## Dataset

**Flight Delays (US DOT)**
- Fuente: Kaggle `usdot/flight-delays`
- ~5.8 millones de vuelos domésticos en USA
- Columnas: fecha, aerolínea, origen, destino, retrasos, etc.

## Prerequisitos

- Completar `00_setup/`
- Conocimientos básicos de Python
- Familiaridad con SQL (recomendado)

## Arquitectura de Spark

```
┌─────────────────────────────────────────────────┐
│                   Driver Program                 │
│  ┌───────────────────────────────────────────┐  │
│  │            SparkContext                    │  │
│  │  - Coordina la ejecución                   │  │
│  │  - Divide trabajo en tareas               │  │
│  │  - Monitorea el cluster                   │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│                 Cluster Manager                  │
│         (Standalone / YARN / Kubernetes)        │
└─────────────────────────────────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│   Worker    │ │   Worker    │ │   Worker    │
│  ┌───────┐  │ │  ┌───────┐  │ │  ┌───────┐  │
│  │Executor│ │ │  │Executor│ │ │  │Executor│ │
│  │ Tasks  │ │ │  │ Tasks  │ │ │  │ Tasks  │ │
│  └───────┘  │ │  └───────┘  │ │  └───────┘  │
└─────────────┘ └─────────────┘ └─────────────┘
```

## Conceptos Clave

### RDD vs DataFrame vs Dataset

| Característica | RDD | DataFrame | Dataset |
|----------------|-----|-----------|---------|
| Abstracción | Bajo nivel | Alto nivel | Alto nivel |
| Esquema | No | Sí | Sí |
| Optimización | Manual | Catalyst | Catalyst |
| Type Safety | No | No | Sí (Scala) |
| Uso recomendado | Legacy, control total | Python, SQL | Scala, Java |

### Transformaciones vs Acciones

**Transformaciones (Lazy)**
- `map()`, `filter()`, `flatMap()`
- `select()`, `withColumn()`, `groupBy()`
- `join()`, `union()`, `distinct()`

**Acciones (Eager)**
- `collect()`, `count()`, `first()`
- `show()`, `take()`, `foreach()`
- `write()`, `save()`

## Comandos Útiles

```bash
# Iniciar cluster
./infrastructure/scripts/start-cluster.sh spark

# Ver Spark UI
open http://localhost:8080

# Ver logs de un job
docker logs spark-master

# Monitorear recursos
docker stats
```

## Conexión con AWS

| Concepto Local | Equivalente AWS | Descripción |
|----------------|-----------------|-------------|
| Spark Master | EMR Master Node | Coordina el cluster |
| Spark Worker | EMR Core Nodes | Procesan datos |
| HDFS | Amazon S3 | Almacenamiento |
| Spark UI | EMR Console | Monitoreo |
| spark-submit | EMR Step | Ejecutar jobs |

## Siguiente Módulo

Después de completar este módulo, continúa con:
- `07_ml_data_preparation/` - Preparación de datos para ML
