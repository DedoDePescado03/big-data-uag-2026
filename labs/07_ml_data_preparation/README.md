# Módulo 07: Preparación de Datos para ML

## Descripción

Técnicas de preparación y feature engineering para Machine Learning usando PySpark MLlib.

## Módulo AWS Academy Relacionado

📚 **Módulo 10: Machine Learning Concepts**
- SageMaker basics
- Feature engineering
- Data preparation pipelines

## Dataset

**Credit Card Fraud Detection**
- Fuente: Kaggle `mlg-ulb/creditcardfraud`
- Datos de transacciones con fraude etiquetado

## Contenido Planificado

| Notebook | Descripción |
|----------|-------------|
| `01_feature_engineering.ipynb` | Creación de features |
| `02_data_preprocessing.ipynb` | Preprocesamiento |
| `03_handling_imbalance.ipynb` | Datos desbalanceados |
| `04_feature_selection.ipynb` | Selección de features |
| `05_ml_pipeline.ipynb` | Pipeline completo |

## Conceptos Clave

### Feature Engineering

- **Encoding**: One-hot, Label, Target
- **Scaling**: StandardScaler, MinMax, Robust
- **Binning**: Discretización de continuos
- **Interaction**: Features combinadas

### MLlib Transformers

```python
from pyspark.ml.feature import (
    VectorAssembler,    # Combinar features
    StandardScaler,     # Normalizar
    StringIndexer,      # Categorías a números
    OneHotEncoder       # One-hot encoding
)
```
