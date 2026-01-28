# Módulo 03: Procesamiento Batch

## Descripción

Aprende procesamiento batch de datos históricos, el enfoque tradicional para procesar grandes volúmenes de datos.

## Módulo AWS Academy Relacionado

📚 **Módulo 7: Data Processing**
- Batch vs Streaming
- MapReduce concepts
- Scheduling y orquestación

## Dataset

**Chicago Crime**
- Fuente: Kaggle `chicago/chicago-crime`
- Datos históricos de crimen en Chicago

## Contenido Planificado

| Notebook | Descripción |
|----------|-------------|
| `01_batch_vs_streaming.ipynb` | Comparación de enfoques |
| `02_mapreduce_concepts.ipynb` | Fundamentos MapReduce |
| `03_batch_pipeline.ipynb` | Pipeline batch completo |
| `04_scheduling.ipynb` | Programación de jobs |

## Conceptos Clave

### Batch vs Streaming

| Característica | Batch | Streaming |
|----------------|-------|-----------|
| Latencia | Minutos-horas | Segundos-ms |
| Datos | Históricos | Tiempo real |
| Complejidad | Menor | Mayor |
| Casos de uso | Reportes, ETL | Alertas, dashboards |

### Arquitectura Batch

```
[Fuentes] → [Ingesta] → [Procesamiento] → [Almacén] → [Consumo]
              ↓              ↓                ↓
           Scheduler    Spark/EMR        Data Lake
```
