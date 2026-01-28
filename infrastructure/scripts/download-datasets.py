#!/usr/bin/env python3
"""
=============================================================================
Script para descargar datasets de Kaggle
Big Data UAG 2026 - AWS Academy Data Engineering
=============================================================================

Prerequisitos:
1. Instalar kaggle: pip install kaggle
2. Configurar credenciales:
   - Ir a kaggle.com/account
   - Crear nuevo API token
   - Guardar kaggle.json en ~/.kaggle/kaggle.json
   - chmod 600 ~/.kaggle/kaggle.json

Uso:
    python download-datasets.py           # Descargar todos
    python download-datasets.py --lab 01  # Descargar solo lab 01
    python download-datasets.py --list    # Listar datasets disponibles
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path

# Colores para terminal
class Colors:
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'

def print_status(msg):
    print(f"{Colors.BLUE}[INFO]{Colors.NC} {msg}")

def print_success(msg):
    print(f"{Colors.GREEN}[OK]{Colors.NC} {msg}")

def print_warning(msg):
    print(f"{Colors.YELLOW}[WARN]{Colors.NC} {msg}")

def print_error(msg):
    print(f"{Colors.RED}[ERROR]{Colors.NC} {msg}")

# Mapeo de labs a datasets de Kaggle
DATASETS = {
    "01": {
        "name": "NYC Taxi Trip Duration",
        "kaggle_id": "c/nyc-taxi-trip-duration",
        "folder": "01_data_fundamentals",
        "competition": True
    },
    "02": {
        "name": "Brazilian E-Commerce (Olist)",
        "kaggle_id": "olistbr/brazilian-ecommerce",
        "folder": "02_etl_pipeline",
        "competition": False
    },
    "03": {
        "name": "Chicago Crime",
        "kaggle_id": "chicago/chicago-crime",
        "folder": "03_batch_processing",
        "competition": False
    },
    "04": {
        "name": "E-Commerce Data",
        "kaggle_id": "carrie1/ecommerce-data",
        "folder": "04_streaming_simulation",
        "competition": False
    },
    "05": {
        "name": "Amazon Fine Food Reviews",
        "kaggle_id": "snap/amazon-fine-food-reviews",
        "folder": "05_data_storage",
        "competition": False
    },
    "06": {
        "name": "Flight Delays",
        "kaggle_id": "usdot/flight-delays",
        "folder": "06_spark_processing",
        "competition": False
    },
    "07": {
        "name": "Credit Card Fraud Detection",
        "kaggle_id": "mlg-ulb/creditcardfraud",
        "folder": "07_ml_data_preparation",
        "competition": False
    },
    "08": {
        "name": "COVID World Vaccination Progress",
        "kaggle_id": "gpreda/covid-world-vaccination-progress",
        "folder": "08_visualization_analysis",
        "competition": False
    },
    "09": {
        "name": "Environmental Sensor Data",
        "kaggle_id": "garystafford/environmental-sensor-data-132k",
        "folder": "09_project_iot_pipeline",
        "competition": False
    }
}

def get_project_root():
    """Obtener directorio raiz del proyecto"""
    script_dir = Path(__file__).parent
    return script_dir.parent.parent

def check_kaggle_installed():
    """Verificar que kaggle CLI esta instalado"""
    try:
        result = subprocess.run(
            ["kaggle", "--version"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_kaggle_credentials():
    """Verificar que las credenciales de Kaggle estan configuradas"""
    kaggle_json = Path.home() / ".kaggle" / "kaggle.json"
    return kaggle_json.exists()

def download_dataset(lab_id: str, data_dir: Path):
    """Descargar un dataset especifico"""
    if lab_id not in DATASETS:
        print_error(f"Lab {lab_id} no encontrado")
        return False

    dataset = DATASETS[lab_id]
    target_dir = data_dir / "raw" / dataset["folder"]

    print_status(f"Descargando: {dataset['name']}")
    print_status(f"  Kaggle ID: {dataset['kaggle_id']}")
    print_status(f"  Destino: {target_dir}")

    # Crear directorio destino
    target_dir.mkdir(parents=True, exist_ok=True)

    try:
        if dataset.get("competition", False):
            # Dataset de competencia
            cmd = [
                "kaggle", "competitions", "download",
                "-c", dataset["kaggle_id"].replace("c/", ""),
                "-p", str(target_dir)
            ]
        else:
            # Dataset normal
            cmd = [
                "kaggle", "datasets", "download",
                "-d", dataset["kaggle_id"],
                "-p", str(target_dir),
                "--unzip"
            ]

        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode == 0:
            print_success(f"Dataset {dataset['name']} descargado correctamente")

            # Si es un zip, descomprimir
            zip_files = list(target_dir.glob("*.zip"))
            for zip_file in zip_files:
                print_status(f"Descomprimiendo {zip_file.name}...")
                subprocess.run(
                    ["unzip", "-o", str(zip_file), "-d", str(target_dir)],
                    capture_output=True
                )
                zip_file.unlink()  # Eliminar zip

            return True
        else:
            print_error(f"Error descargando {dataset['name']}")
            print_error(result.stderr)
            return False

    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def list_datasets():
    """Listar todos los datasets disponibles"""
    print("\nDatasets disponibles:\n")
    print(f"{'Lab':<6} {'Nombre':<40} {'Kaggle ID':<45}")
    print("-" * 95)

    for lab_id, info in DATASETS.items():
        print(f"{lab_id:<6} {info['name']:<40} {info['kaggle_id']:<45}")

    print()

def create_sample_data(data_dir: Path):
    """Crear datos de ejemplo pequenos para testing"""
    print_status("Creando datos de ejemplo...")

    sample_dir = data_dir / "sample"
    sample_dir.mkdir(parents=True, exist_ok=True)

    # Crear CSV de ejemplo
    sample_csv = sample_dir / "sample_sales.csv"
    sample_data = """date,product,category,quantity,price,customer_id
2024-01-01,Laptop,Electronics,2,999.99,C001
2024-01-01,Mouse,Electronics,5,29.99,C002
2024-01-02,Desk,Furniture,1,299.99,C003
2024-01-02,Chair,Furniture,4,149.99,C001
2024-01-03,Monitor,Electronics,3,399.99,C004
2024-01-03,Keyboard,Electronics,10,79.99,C002
2024-01-04,Bookshelf,Furniture,2,199.99,C005
2024-01-04,Lamp,Furniture,6,49.99,C003
2024-01-05,Tablet,Electronics,4,599.99,C001
2024-01-05,Headphones,Electronics,8,149.99,C004
"""

    with open(sample_csv, 'w') as f:
        f.write(sample_data)

    print_success(f"Datos de ejemplo creados en {sample_dir}")

def main():
    parser = argparse.ArgumentParser(
        description="Descargar datasets de Kaggle para Big Data UAG 2026"
    )
    parser.add_argument(
        "--lab",
        type=str,
        help="ID del lab (01-09) para descargar solo ese dataset"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="Listar datasets disponibles"
    )
    parser.add_argument(
        "--sample",
        action="store_true",
        help="Crear solo datos de ejemplo (sin Kaggle)"
    )

    args = parser.parse_args()

    print("\n" + "=" * 50)
    print("  Big Data UAG 2026 - Dataset Downloader")
    print("=" * 50 + "\n")

    # Solo listar
    if args.list:
        list_datasets()
        return

    # Obtener directorio de datos
    project_root = get_project_root()
    data_dir = project_root / "data"

    # Solo crear sample data
    if args.sample:
        create_sample_data(data_dir)
        return

    # Verificar Kaggle
    if not check_kaggle_installed():
        print_error("Kaggle CLI no esta instalado")
        print_status("Instalar con: pip install kaggle")
        sys.exit(1)

    if not check_kaggle_credentials():
        print_error("Credenciales de Kaggle no configuradas")
        print_status("1. Ir a kaggle.com/account")
        print_status("2. Click en 'Create New API Token'")
        print_status("3. Guardar kaggle.json en ~/.kaggle/")
        print_status("4. chmod 600 ~/.kaggle/kaggle.json")
        sys.exit(1)

    print_success("Kaggle configurado correctamente")

    # Crear sample data siempre
    create_sample_data(data_dir)

    # Descargar datasets
    if args.lab:
        # Descargar solo un lab
        download_dataset(args.lab, data_dir)
    else:
        # Descargar todos
        print_status("Descargando todos los datasets...")
        print_warning("Esto puede tomar varios minutos\n")

        success = 0
        failed = 0

        for lab_id in DATASETS:
            if download_dataset(lab_id, data_dir):
                success += 1
            else:
                failed += 1
            print()

        print("\n" + "=" * 50)
        print(f"  Completado: {success} exitosos, {failed} fallidos")
        print("=" * 50 + "\n")

if __name__ == "__main__":
    main()
