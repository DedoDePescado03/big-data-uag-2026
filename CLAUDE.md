# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Educational repository for a Big Data course at UAG (2026). Contains Docker learning materials, Flask/Jupyter templates, and example configurations for teaching containerization concepts.

## Repository Structure

- `docs/docker-guide.md` - Comprehensive Docker tutorial with hands-on exercises
- `examples/docker/` - Template files (*.example) for Flask apps, Jupyter notebooks, and Docker Compose setups
- `flask-demo/` - Working Flask application example (port 5051)

## Common Commands

### Flask Demo

```bash
# Build and run the flask-demo
cd flask-demo
docker build -t flask-demo .
docker run -d -p 5051:5051 --name flask-demo flask-demo

# Test the endpoints
curl http://localhost:5051
curl http://localhost:5051/health

# Stop and remove
docker stop flask-demo && docker rm flask-demo
```

### Using Example Templates

```bash
# Copy examples to create a new project
cp examples/docker/Dockerfile.example ./Dockerfile
cp examples/docker/app.py.example ./app.py
cp examples/docker/requirements.txt.example ./requirements.txt
cp examples/docker/docker-compose.example.yml ./docker-compose.yml

# Build and run with Docker Compose
docker compose up -d
```

### Multi-Service Stack (from docker-compose.example.yml)

```bash
docker compose up -d          # Start all services (Flask, Jupyter, PostgreSQL, Redis)
docker compose ps             # Check status
docker compose logs -f        # Follow logs
docker compose down -v        # Stop and remove volumes
```

## Technology Stack

- Python 3.11-slim (base Docker image)
- Flask 3.0.0 (web framework)
- Jupyter Lab (data science notebooks)
- PostgreSQL 15, Redis 7 (in compose examples)
- Data science: pandas, numpy, matplotlib, seaborn, scikit-learn

## Port Conventions

- Flask apps: 5000 (examples) or 5051 (flask-demo)
- Jupyter Lab: 8888
- PostgreSQL: 5432
- Redis: 6379

# Big Data UAG 2026 - Instrucciones del Proyecto

## Descripción

Repositorio de prácticas para el curso AWS Academy Data Engineering. Estudiantes **sin experiencia previa en Big Data**. Las prácticas son **independientes** de los labs de AWS Academy.

## Stack Tecnológico

- **PySpark 3.5** en Docker (cluster local)
- **Jupyter Lab** para notebooks
- **Delta Lake** para storage
- **Kafka** para streaming (opcional)
- Datasets de **Kaggle**

## Estructura del Proyecto

```
big-data-uag-2026/
├── labs/                    # Notebooks de práctica
│   ├── 00_setup/
│   ├── 01_data_fundamentals/
│   ├── 02_etl_pipeline/
│   ├── 03_batch_processing/
│   ├── 04_streaming_simulation/
│   ├── 05_data_storage/
│   ├── 06_spark_processing/
│   ├── 07_ml_data_preparation/
│   ├── 08_visualization_analysis/
│   └── 09_project_iot_pipeline/
├── infrastructure/          # Docker, scripts
├── data/                    # Datasets (raw, processed, sample)
├── src/                     # Código reutilizable
└── docs/                    # Documentación
```

## Formato Obligatorio de Notebooks

```python
"""
# Título del Notebook

## Objetivos de Aprendizaje
- Objetivo 1
- Objetivo 2

## Prerequisitos
- Notebooks anteriores requeridos
- Conocimientos previos

## Tiempo Estimado
⏱️ XX minutos

## Módulo AWS Academy Relacionado
📚 Módulo X: Nombre
"""

# === SECCIÓN X ===
"""
## X. Título

### Explicación Conceptual
[Explicación simple con analogías del mundo real]

### Código
"""
# Código CON COMENTARIOS EN CADA LÍNEA explicando qué y por qué

"""
### 🎯 Ejercicio Práctico X.1
[Instrucciones claras]

**Pistas:**
- Pista 1
- Pista 2
"""
# TODO: Código del estudiante

"""
### ✅ Solución
"""
# Solución comentada

# === RESUMEN FINAL ===
"""
## Resumen

### Conceptos Clave
- Concepto: explicación

### Conexión con AWS
- Servicio AWS: cómo se relaciona

### Siguiente Paso
Continúa con: `XX_siguiente.ipynb`
"""
```

## Reglas de Estilo

### OBLIGATORIO

- Explicaciones en **español**
- Código puede usar nombres en **inglés**
- **Comentario en CADA línea** de código explicando qué y por qué
- Usar analogías del mundo real para conceptos nuevos
- Emojis para destacar: 💡 tips, ⚠️ advertencias, 🎯 ejercicios, ✅ soluciones
- Mínimo **3 ejercicios** por notebook con soluciones
- Mostrar **output esperado** como comentario después de cada bloque

### PROHIBIDO

- Asumir conocimiento previo de Big Data
- Usar jerga sin explicarla primero
- Dejar código sin comentarios
- Saltar pasos "obvios"
- Explicaciones en inglés

## Datasets por Módulo

| Lab | Dataset Kaggle |
|-----|----------------|
| 01_data_fundamentals | `new-york-city/nyc-taxi-trip-duration` |
| 02_etl_pipeline | `olistbr/brazilian-ecommerce` |
| 03_batch_processing | `chicago/chicago-crime` |
| 04_streaming | `carrie1/ecommerce-data` |
| 05_data_storage | `snap/amazon-fine-food-reviews` |
| 06_spark_processing | `usdot/flight-delays` |
| 07_ml_preparation | `mlg-ulb/creditcardfraud` |
| 08_visualization | `gpreda/covid-world-vaccination-progress` |
| 09_project_iot | `garystafford/environmental-sensor-data-132k` |

## Mapeo con Módulos AWS Academy

| Lab Local | Módulo AWS | Tema |
|-----------|------------|------|
| 00_setup | - | Configuración |
| 01_data_fundamentals | M03 | 5 Vs, tipos de datos |
| 02_etl_pipeline | M06 | ETL/ELT, data wrangling |
| 03_batch_processing | M07 | Batch vs streaming |
| 04_streaming | M07 | Kinesis, streaming |
| 05_data_storage | M08 | S3, data lake, formatos |
| 06_spark_processing | M09 | EMR, Hadoop, Spark |
| 07_ml_preparation | M10 | SageMaker, feature eng |
| 08_visualization | M11 | Athena, QuickSight |
| 09_project_iot | IoT Use Case | Pipeline completo |

## Infraestructura Docker

### docker-compose.spark.yml

- `spark-master`: Puerto 8080 (UI), 7077 (master)
- `spark-worker`: 2GB RAM, 2 cores
- `jupyter`: Puerto 8888, conectado al cluster

### Volúmenes

- `./data:/data` - Datasets
- `./labs:/labs` - Notebooks
- `./src:/src` - Código compartido

## Prioridad de Desarrollo

1. **Alta**: 00_setup, 06_spark_processing, 02_etl_pipeline, 05_data_storage
2. **Media**: 03_batch_processing, 04_streaming, 07_ml_preparation
3. **Normal**: 01_data_fundamentals, 08_visualization, 09_project_iot

## Verificación de Calidad

Cada notebook DEBE:

- [ ] Ejecutarse sin errores de principio a fin
- [ ] Tener todas las celdas documentadas
- [ ] Incluir mínimo 3 ejercicios con soluciones
- [ ] Conectar con módulo AWS correspondiente
- [ ] Mostrar outputs esperados

## Comandos Útiles

```bash
# Iniciar cluster
docker compose -f infrastructure/docker-compose.spark.yml up -d

# Ver logs
docker compose -f infrastructure/docker-compose.spark.yml logs -f jupyter

# Detener
docker compose -f infrastructure/docker-compose.spark.yml down

# Descargar datasets
python infrastructure/scripts/download-datasets.py
```
