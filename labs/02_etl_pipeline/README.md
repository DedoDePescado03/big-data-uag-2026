# Módulo 02: Pipeline ETL

## Descripción

Este módulo enseña cómo construir pipelines ETL (Extract, Transform, Load) usando PySpark. Aprenderás a extraer datos de múltiples fuentes, transformarlos y cargarlos en diferentes destinos.

## Objetivos de Aprendizaje

Al completar este módulo podrás:
- Entender las diferencias entre ETL y ELT
- Extraer datos de CSV, JSON, Parquet y bases de datos
- Aplicar transformaciones de limpieza y enriquecimiento
- Cargar datos en diferentes formatos y destinos
- Manejar errores y datos problemáticos

## Módulo AWS Academy Relacionado

📚 **Módulo 6: Data Processing and Analysis**
- ETL/ELT concepts
- AWS Glue para ETL serverless
- Data wrangling

## Dataset

**Brazilian E-Commerce (Olist)**
- Fuente: Kaggle `olistbr/brazilian-ecommerce`
- Datos reales de e-commerce de Brasil
- Múltiples tablas relacionadas (pedidos, productos, clientes, pagos)

## Contenido

| Notebook | Descripción | Tiempo |
|----------|-------------|--------|
| `01_etl_concepts.ipynb` | Conceptos ETL vs ELT | 30 min |
| `02_data_extraction.ipynb` | Extracción de múltiples fuentes | 45 min |
| `03_data_transformation.ipynb` | Transformaciones comunes | 60 min |
| `04_data_loading.ipynb` | Carga a diferentes destinos | 45 min |
| `05_pipeline_completo.ipynb` | Pipeline ETL end-to-end | 60 min |

## Conceptos Clave

### ETL vs ELT

```
ETL (Extract-Transform-Load):
┌─────────┐    ┌─────────────┐    ┌─────────┐
│ Extract │ -> │  Transform  │ -> │  Load   │
│ (Source)│    │ (Spark/ETL) │    │ (Target)│
└─────────┘    └─────────────┘    └─────────┘
- Transformaciones ANTES de cargar
- Usado cuando el destino tiene capacidad limitada

ELT (Extract-Load-Transform):
┌─────────┐    ┌─────────┐    ┌─────────────┐
│ Extract │ -> │  Load   │ -> │  Transform  │
│ (Source)│    │ (Lake)  │    │ (Lake/DW)   │
└─────────┘    └─────────┘    └─────────────┘
- Carga datos crudos primero
- Transformaciones en el data lake/warehouse
- Aprovecha poder de cómputo del destino
```

### Fases del Pipeline

1. **Extract (Extracción)**
   - Conectar a fuentes de datos
   - Validar conexiones
   - Manejar errores de lectura

2. **Transform (Transformación)**
   - Limpieza (nulos, duplicados)
   - Normalización (formatos, tipos)
   - Enriquecimiento (joins, cálculos)
   - Agregación (resúmenes)

3. **Load (Carga)**
   - Elegir formato destino
   - Particionar datos
   - Validar carga exitosa

## Comandos Útiles

```bash
# Descargar dataset de Kaggle
python infrastructure/scripts/download-datasets.py --lab 02

# Verificar archivos descargados
ls -la data/raw/02_etl_pipeline/

# Iniciar cluster
./infrastructure/scripts/start-cluster.sh spark
```

## Estructura de Datos Olist

```
olist_customers_dataset.csv       - Clientes
olist_orders_dataset.csv          - Pedidos
olist_order_items_dataset.csv     - Items de pedidos
olist_order_payments_dataset.csv  - Pagos
olist_products_dataset.csv        - Productos
olist_sellers_dataset.csv         - Vendedores
product_category_name_translation.csv - Traducciones
```

## Conexión con AWS

| Concepto Local | Servicio AWS | Uso |
|----------------|--------------|-----|
| PySpark ETL | AWS Glue | ETL serverless |
| Script Python | Glue Job | Código ETL |
| Schema inference | Glue Crawler | Descubrir esquemas |
| CSV/Parquet | S3 | Almacenamiento |
| Transformaciones | Glue Studio | ETL visual |

## Siguiente Módulo

Después de completar ETL, continúa con:
- `03_batch_processing/` - Procesamiento batch
