# Módulo 00: Configuración del Entorno

## Descripción

Este módulo te guiará para configurar tu entorno de desarrollo de Big Data. Al finalizar, tendrás un cluster de Spark funcionando con Jupyter Lab.

## Prerequisitos

- Docker Desktop instalado
- 8GB RAM mínimo disponible
- Conexión a internet

## Contenido

| Notebook | Descripción | Tiempo |
|----------|-------------|--------|
| `01_environment_check.ipynb` | Verificar que todo funciona | 15 min |
| `02_spark_basics.ipynb` | Primeros pasos con Spark | 30 min |

## Instrucciones de Instalación

### 1. Instalar Docker

**macOS:**
```bash
brew install --cask docker
```

**Windows/Linux:**
Descargar de https://www.docker.com/products/docker-desktop

### 2. Verificar Docker

```bash
docker --version
docker compose version
```

### 3. Iniciar el Cluster

```bash
cd big-data-uag-2026
./infrastructure/scripts/start-cluster.sh spark
```

### 4. Acceder a Jupyter

Abrir http://localhost:8888 en el navegador.

### 5. Verificar Servicios

| Servicio | URL |
|----------|-----|
| Jupyter Lab | http://localhost:8888 |
| Spark Master | http://localhost:8080 |
| Spark Worker | http://localhost:8081 |

## Solución de Problemas

### "Puerto en uso"

```bash
# Detener servicios existentes
./infrastructure/scripts/stop-cluster.sh

# Verificar puertos
lsof -i :8888
lsof -i :8080
```

### "No hay memoria suficiente"

1. Abrir Docker Desktop
2. Settings → Resources
3. Aumentar memoria a 8GB mínimo

### "Contenedor no inicia"

```bash
# Ver logs
docker compose -f infrastructure/docker-compose.spark.yml logs

# Reiniciar
./infrastructure/scripts/stop-cluster.sh
./infrastructure/scripts/start-cluster.sh spark
```

## Siguiente Paso

Una vez verificado el entorno, continúa con `01_environment_check.ipynb`.
