# Módulo 04: Simulación de Streaming

## Descripción

Simula procesamiento de datos en streaming usando datos batch, preparación para Kafka y sistemas de streaming real.

## Módulo AWS Academy Relacionado

📚 **Módulo 7: Data Processing - Streaming**
- Amazon Kinesis
- Real-time processing
- Event-driven architecture

## Dataset

**E-Commerce Data**
- Fuente: Kaggle `carrie1/ecommerce-data`
- Transacciones de e-commerce para simular stream

## Contenido Planificado

| Notebook | Descripción |
|----------|-------------|
| `01_streaming_concepts.ipynb` | Conceptos de streaming |
| `02_structured_streaming.ipynb` | Spark Structured Streaming |
| `03_window_operations.ipynb` | Ventanas de tiempo |
| `04_kafka_simulation.ipynb` | Simulación con Kafka |

## Conceptos Clave

### Streaming Patterns

- **Event Time vs Processing Time**
- **Watermarks**: Manejo de datos tardíos
- **Windows**: Tumbling, Sliding, Session
- **Triggers**: Frecuencia de procesamiento

### Arquitectura Streaming

```
[Producers] → [Message Queue] → [Processors] → [Consumers]
    ↓              ↓                ↓              ↓
  Sensors       Kafka           Spark          Dashboard
  Apps          Kinesis         Flink          Alerts
```
