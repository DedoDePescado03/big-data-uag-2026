# 📊 Lab 01: Fundamentos de Big Data

## 🎯 Descripción

Este laboratorio introduce los conceptos fundamentales de Big Data utilizando el dataset de viajes en taxi de Nueva York. Aprenderás las **5 Vs del Big Data**, tipos de datos, y darás tus primeros pasos con PySpark.

## 📚 Módulo AWS Academy Relacionado

**Módulo 3: Data Characteristics** - Características de los datos, las 5 Vs, tipos de datos estructurados y no estructurados.

## ⏱️ Tiempo Estimado

**90-120 minutos** (incluyendo ejercicios prácticos)

## 📋 Prerequisitos

- ✅ Haber completado el Lab 00 (Setup del entorno)
- ✅ Docker Desktop instalado y funcionando
- ✅ Conocimientos básicos de Python

---

## 🚀 Instrucciones de Inicio

### Paso 1: Navegar al Directorio del Proyecto

```bash
# Abrir terminal y navegar al proyecto
cd ~/Documents/big-data-uag-2026
```

### Paso 2: Levantar el Cluster de Spark

```bash
# Construir y levantar los contenedores (primera vez tomará unos minutos)
docker compose -f infrastructure/docker-compose.spark.yml up -d --build
```

**💡 Tip:** La primera vez que ejecutes este comando, Docker descargará las imágenes base (~2-3 GB). Esto solo ocurre una vez.

### Paso 3: Verificar que los Servicios Están Corriendo

```bash
# Ver el estado de los contenedores
docker compose -f infrastructure/docker-compose.spark.yml ps
```

Deberías ver algo como:

```
NAME            STATUS      PORTS
spark-master    running     0.0.0.0:7077->7077/tcp, 0.0.0.0:8080->8080/tcp
spark-worker    running     0.0.0.0:8081->8081/tcp
jupyter-spark   running     0.0.0.0:4040->4040/tcp, 0.0.0.0:8888->8888/tcp
```

### Paso 4: Acceder a Jupyter Lab

1. Abre tu navegador web
2. Ve a: **http://localhost:8888**
3. No se requiere contraseña (el token está deshabilitado para desarrollo local)

### Paso 5: Abrir el Notebook del Laboratorio

1. En Jupyter Lab, navega a: `labs/01_data_fundamentals/`
2. Abre el archivo: `01_introduccion_big_data.ipynb`

---

## 🌐 URLs Importantes

| Servicio | URL | Descripción |
|----------|-----|-------------|
| **Jupyter Lab** | http://localhost:8888 | Entorno de notebooks |
| **Spark Master UI** | http://localhost:8080 | Dashboard del cluster |
| **Spark Worker UI** | http://localhost:8081 | Estado del worker |
| **Spark App UI** | http://localhost:4040 | Jobs en ejecución (solo cuando hay una app corriendo) |

---

## 📁 Estructura del Laboratorio

```
01_data_fundamentals/
├── README.md                          # Este archivo (instrucciones)
├── 01_introduccion_big_data.ipynb     # Notebook principal
└── data/                              # Datos de muestra
    └── sample_taxi_trips.csv
```

---

## 📊 Dataset

### Opción A: Datos de Muestra (Recomendado para empezar)

El notebook incluye código para generar datos de muestra que simulan viajes en taxi. Esto permite practicar sin necesidad de descargar el dataset completo.

### Opción B: Dataset Completo de Kaggle

Para trabajar con el dataset real de NYC Taxi (1.5M+ registros):

```bash
# Instalar Kaggle CLI (si no lo tienes)
pip install kaggle

# Configurar credenciales de Kaggle
# 1. Ve a kaggle.com/account
# 2. Click en "Create New API Token"
# 3. Mueve el archivo descargado:
mkdir -p ~/.kaggle
mv ~/Downloads/kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Descargar el dataset del Lab 01
python infrastructure/scripts/download-datasets.py --lab 01
```

---

## 🛑 Detener el Cluster

Cuando termines de trabajar:

```bash
# Detener los contenedores (preserva los datos)
docker compose -f infrastructure/docker-compose.spark.yml stop

# O para detener y eliminar los contenedores
docker compose -f infrastructure/docker-compose.spark.yml down
```

**⚠️ Advertencia:** Si usas `down -v`, también se eliminarán los volúmenes con tus datos.

---

## 🔧 Solución de Problemas

### El puerto 8888 ya está en uso

```bash
# Verificar qué proceso usa el puerto
lsof -i :8888

# Detener el proceso o cambiar el puerto en docker-compose.spark.yml
```

### Los contenedores no inician

```bash
# Ver los logs para identificar el problema
docker compose -f infrastructure/docker-compose.spark.yml logs

# Reiniciar Docker Desktop y volver a intentar
```

### Jupyter no conecta con Spark

```bash
# Verificar que spark-master está corriendo
docker compose -f infrastructure/docker-compose.spark.yml logs spark-master

# Reiniciar el cluster
docker compose -f infrastructure/docker-compose.spark.yml restart
```

### Error de memoria en Spark

El worker está configurado con 2GB de RAM. Si procesas datasets muy grandes:

1. Aumenta la memoria en `docker-compose.spark.yml`:
   ```yaml
   SPARK_WORKER_MEMORY=4g
   ```
2. Reinicia el cluster

---

## 📝 Contenido del Laboratorio

### Sección 1: Introducción a Big Data
- ¿Qué es Big Data?
- Las 5 Vs explicadas con ejemplos del mundo real

### Sección 2: Tipos de Datos
- Estructurados vs Semi-estructurados vs No estructurados
- Ejemplos prácticos

### Sección 3: Primeros Pasos con PySpark
- Crear una SparkSession
- Cargar datos en DataFrames
- Operaciones básicas

### Sección 4: Exploración del Dataset de Taxis
- Estadísticas descriptivas
- Detección de valores nulos
- Visualizaciones básicas

### Sección 5: Ejercicios Prácticos
- 3 ejercicios con soluciones completas
- Conexión con conceptos de AWS

---

## ✅ Checklist de Finalización

- [ ] Puedo explicar las 5 Vs del Big Data con ejemplos
- [ ] Entiendo la diferencia entre datos estructurados y no estructurados
- [ ] Puedo crear una SparkSession y cargar datos
- [ ] Puedo realizar operaciones básicas con DataFrames
- [ ] Completé los 3 ejercicios prácticos

---

## ➡️ Siguiente Paso

Una vez completado este laboratorio, continúa con:
**Lab 02: ETL Pipeline** (`labs/02_etl_pipeline/`)
