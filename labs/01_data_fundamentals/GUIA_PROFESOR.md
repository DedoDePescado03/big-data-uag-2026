# 👨‍🏫 Guía del Profesor - Lab 01: Fundamentos de Big Data

## Resumen Ejecutivo

**Duración**: 90-120 minutos
**Nivel**: Principiante (sin experiencia previa en Big Data)
**Módulo AWS Academy**: Módulo 3 - Data Characteristics

---

## 🚀 Comandos Rápidos para Levantar el Ambiente

### Antes de la Clase (Preparación)

```bash
# 1. Navegar al directorio del proyecto
cd ~/Documents/big-data-uag-2026

# 2. Construir las imágenes Docker (solo primera vez, ~5-10 min)
docker compose -f infrastructure/docker-compose.spark.yml build

# 3. Verificar que no hay conflictos de puertos
lsof -i :8888  # Jupyter
lsof -i :8080  # Spark Master
lsof -i :8081  # Spark Worker
```

### Durante la Clase

```bash
# Levantar el cluster completo
docker compose -f infrastructure/docker-compose.spark.yml up -d

# Verificar que todo está corriendo
docker compose -f infrastructure/docker-compose.spark.yml ps

# Ver los logs si hay problemas
docker compose -f infrastructure/docker-compose.spark.yml logs -f
```

### Después de la Clase

```bash
# Detener el cluster (preserva volúmenes)
docker compose -f infrastructure/docker-compose.spark.yml stop

# O detener y limpiar completamente
docker compose -f infrastructure/docker-compose.spark.yml down
```

---

## 🌐 URLs para Compartir con Alumnos

| Servicio | URL | Descripción |
|----------|-----|-------------|
| Jupyter Lab | http://localhost:8888 | Notebooks (sin password) |
| Spark Master UI | http://localhost:8080 | Dashboard del cluster |
| Spark Worker UI | http://localhost:8081 | Estado del worker |
| Spark App UI | http://localhost:4040 | Jobs activos |

---

## 📋 Checklist Pre-Clase

- [ ] Docker Desktop instalado y corriendo
- [ ] Al menos 4GB de RAM disponible
- [ ] Puertos 8888, 8080, 8081, 4040 libres
- [ ] Imágenes Docker construidas (`docker compose build`)
- [ ] Cluster probado localmente
- [ ] Proyector/pantalla configurado

---

## 🎯 Objetivos de Aprendizaje

Al finalizar, los alumnos serán capaces de:

1. **Explicar** qué es Big Data y por qué es importante
2. **Describir** las 5 Vs con ejemplos del mundo real
3. **Diferenciar** entre datos estructurados, semi-estructurados y no estructurados
4. **Crear** una SparkSession y cargar datos
5. **Realizar** operaciones básicas de exploración (select, filter, groupBy)

---

## 📖 Plan de Clase Sugerido

### Parte 1: Introducción Teórica (30 min)

1. **¿Qué es Big Data?** (10 min)
   - Mostrar estadísticas impactantes (datos generados por día)
   - Analogía de la biblioteca
   - Preguntar: "¿Qué apps usan Big Data?"

2. **Las 5 Vs** (15 min)
   - Explicar cada V con ejemplos
   - Conectar con el dataset de taxis de NYC
   - Ejercicio oral: identificar las Vs en Netflix/Uber

3. **Tipos de Datos** (5 min)
   - Estructurados vs Semi-estructurados vs No estructurados
   - Porcentajes del mundo real (80% no estructurados)

### Parte 2: Práctica Guiada (45 min)

1. **Setup del Ambiente** (10 min)
   - Abrir Jupyter Lab
   - Navegar al notebook
   - Ejecutar celda de configuración

2. **Crear SparkSession** (10 min)
   - Explicar qué es SparkSession
   - Ejecutar la celda
   - Mostrar Spark UI (localhost:8080)

3. **Exploración de Datos** (25 min)
   - Generar datos de muestra
   - show(), describe()
   - select(), filter(), groupBy()
   - Visualización básica

### Parte 3: Ejercicios Individuales (30 min)

1. **Ejercicio 1**: Análisis de pasajeros (10 min)
2. **Ejercicio 2**: Viajes cortos/largos (10 min)
3. **Ejercicio 3**: Distancia calculada (10 min)

### Cierre (10 min)

- Resumen de conceptos clave
- Conexión con AWS (EMR, Glue)
- Preguntas y respuestas
- Asignar lectura para próxima clase

---

## 💡 Tips Pedagógicos

### Para Mantener la Atención

- Usar analogías del mundo real constantemente
- Hacer preguntas interactivas: "¿Cuántos datos genera Spotify?"
- Mostrar la Spark UI para visualizar el procesamiento
- Comparar tiempos: Pandas vs Spark (cuando hay más datos)

### Errores Comunes de Alumnos

| Error | Solución |
|-------|----------|
| "Connection refused" | Verificar que Docker está corriendo |
| "SparkSession already exists" | Reiniciar el kernel del notebook |
| Celda no ejecuta | Verificar que ejecutaron celdas anteriores |
| OutOfMemoryError | Reducir tamaño de datos o aumentar memoria |

### Preguntas Frecuentes

**Q: ¿Por qué no usamos pandas directamente?**
A: Pandas carga todo en memoria de una máquina. Spark distribuye los datos entre múltiples máquinas, permitiendo procesar terabytes.

**Q: ¿Cuándo debo usar Big Data?**
A: Cuando tus datos no caben en memoria de una sola máquina, o cuando necesitas procesar en tiempo real.

**Q: ¿Qué diferencia hay entre esto y AWS?**
A: Usamos las mismas tecnologías (Spark), pero en local. AWS provee la infraestructura para escalar a producción.

---

## 📊 Evaluación Sugerida

### Criterios de Evaluación por Ejercicio

| Ejercicio | Puntos | Criterios |
|-----------|--------|-----------|
| Ejercicio 1 | 30 | groupBy correcto, ordenamiento, porcentaje calculado |
| Ejercicio 2 | 30 | Filtros correctos, conteo, ejemplos mostrados |
| Ejercicio 3 | 40 | Nueva columna creada, fórmula correcta, agregación |

### Preguntas de Reflexión (Tarea)

1. ¿Cuál de las 5 Vs consideras más importante y por qué?
2. Describe 3 ejemplos de datos no estructurados en tu vida diaria
3. ¿Qué servicio de AWS usarías para procesar 10TB de logs?

---

## 🔗 Recursos Adicionales

### Para Profundizar

- [Apache Spark Documentation](https://spark.apache.org/docs/latest/)
- [AWS Big Data Blog](https://aws.amazon.com/blogs/big-data/)
- [Módulo 3 AWS Academy](https://awsacademy.instructure.com/)

### Videos Recomendados

- "What is Big Data?" - Simplilearn (10 min)
- "Apache Spark in 5 minutes" - Databricks (5 min)

---

## ⚠️ Solución de Problemas en Clase

### Si Docker no inicia

```bash
# Reiniciar Docker Desktop
# O desde terminal:
killall Docker && open -a Docker
```

### Si Jupyter no responde

```bash
# Reiniciar solo el contenedor de Jupyter
docker restart jupyter-spark
```

### Si Spark no conecta

```bash
# Verificar que spark-master está corriendo
docker logs spark-master

# Reiniciar el cluster completo
docker compose -f infrastructure/docker-compose.spark.yml restart
```

### Si un alumno no puede acceder

1. Verificar que está en la misma red (si es remoto)
2. Verificar firewall/antivirus
3. Usar `docker-compose logs` para diagnosticar

---

## 📝 Notas del Laboratorio

**Cambios realizados**:
- Fecha: 2026-01-28
- Versión: 1.0

**Próxima actualización**:
- Agregar más visualizaciones
- Conectar con dataset real de Kaggle
- Agregar ejercicio de streaming preview
