# Módulo 09: Proyecto Final - Pipeline IoT

## Descripción

Proyecto integrador que combina todos los conceptos del curso en un pipeline IoT end-to-end.

## Módulo AWS Academy Relacionado

📚 **Caso de uso IoT**
- AWS IoT Core
- Kinesis for IoT
- Analytics pipeline

## Dataset

**Environmental Sensor Data**
- Fuente: Kaggle `garystafford/environmental-sensor-data-132k`
- Datos de sensores ambientales (temperatura, humedad, etc.)

## Objetivo del Proyecto

Construir un pipeline completo que:
1. Ingeste datos de sensores (simulados)
2. Procese en tiempo semi-real
3. Detecte anomalías
4. Almacene en data lake
5. Visualice en dashboard

## Arquitectura del Proyecto

```
[Sensores]     [Ingesta]      [Procesamiento]    [Storage]      [Consumo]
    ↓              ↓               ↓                 ↓              ↓
 Simulador  →   Kafka    →    Spark       →     Delta     →   Dashboard
                           Structured          Lake
                           Streaming
```

## Contenido

| Notebook | Descripción |
|----------|-------------|
| `01_project_setup.ipynb` | Configuración del proyecto |
| `02_data_ingestion.ipynb` | Ingesta de sensores |
| `03_stream_processing.ipynb` | Procesamiento streaming |
| `04_anomaly_detection.ipynb` | Detección de anomalías |
| `05_data_lake_storage.ipynb` | Almacenamiento Delta |
| `06_visualization.ipynb` | Dashboard final |
| `07_project_presentation.ipynb` | Presentación |

## Entregables

1. Pipeline funcional end-to-end
2. Documentación del diseño
3. Dashboard interactivo
4. Presentación de resultados

## Criterios de Evaluación

- [ ] Pipeline ejecuta sin errores
- [ ] Datos procesados correctamente
- [ ] Anomalías detectadas
- [ ] Dashboard funcional
- [ ] Código documentado
