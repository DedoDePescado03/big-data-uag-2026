#!/bin/bash
# =============================================================================
# Script para iniciar el cluster de Big Data
# Big Data UAG 2026 - AWS Academy Data Engineering
# =============================================================================

set -e

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Directorio base
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INFRA_DIR="$(dirname "$SCRIPT_DIR")"

# Funcion para imprimir mensajes
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Mostrar uso
usage() {
    echo "Uso: $0 [opcion]"
    echo ""
    echo "Opciones:"
    echo "  spark     - Iniciar solo Spark + Jupyter"
    echo "  kafka     - Iniciar solo Kafka"
    echo "  full      - Iniciar todo (Spark + Kafka + DBs)"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplo: $0 spark"
}

# Verificar Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker no esta instalado"
        exit 1
    fi

    if ! docker info &> /dev/null; then
        print_error "Docker daemon no esta corriendo"
        exit 1
    fi

    print_success "Docker esta disponible"
}

# Iniciar cluster Spark
start_spark() {
    print_status "Iniciando cluster Spark..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.spark.yml up -d --build

    print_status "Esperando a que los servicios esten listos..."
    sleep 10

    echo ""
    print_success "Cluster Spark iniciado!"
    echo ""
    echo "  Spark Master UI:  http://localhost:8080"
    echo "  Spark Worker UI:  http://localhost:8081"
    echo "  Jupyter Lab:      http://localhost:8888"
    echo "  Spark App UI:     http://localhost:4040 (cuando hay una app corriendo)"
    echo ""
}

# Iniciar Kafka
start_kafka() {
    print_status "Iniciando Kafka..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.kafka.yml up -d

    print_status "Esperando a que los servicios esten listos..."
    sleep 15

    echo ""
    print_success "Kafka iniciado!"
    echo ""
    echo "  Kafka Broker:     localhost:9092"
    echo "  Kafka UI:         http://localhost:9000"
    echo "  Schema Registry:  http://localhost:8081"
    echo "  Zookeeper:        localhost:2181"
    echo ""
}

# Iniciar full stack
start_full() {
    print_status "Iniciando Full Stack (Spark + Kafka + DBs)..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.full-stack.yml up -d --build

    print_status "Esperando a que los servicios esten listos..."
    sleep 20

    echo ""
    print_success "Full Stack iniciado!"
    echo ""
    echo "  === SPARK ==="
    echo "  Spark Master UI:  http://localhost:8080"
    echo "  Spark Worker UI:  http://localhost:8081"
    echo "  Jupyter Lab:      http://localhost:8888"
    echo ""
    echo "  === KAFKA ==="
    echo "  Kafka Broker:     localhost:9092"
    echo "  Kafka UI:         http://localhost:9000"
    echo ""
    echo "  === DATABASES ==="
    echo "  PostgreSQL:       localhost:5432 (user: bigdata, pass: bigdata123)"
    echo "  Redis:            localhost:6379"
    echo "  MinIO Console:    http://localhost:9001 (user: minioadmin, pass: minioadmin123)"
    echo ""
}

# Main
main() {
    echo ""
    echo "=========================================="
    echo "  Big Data UAG 2026 - Cluster Manager"
    echo "=========================================="
    echo ""

    check_docker

    case "${1:-spark}" in
        spark)
            start_spark
            ;;
        kafka)
            start_kafka
            ;;
        full)
            start_full
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_error "Opcion no reconocida: $1"
            usage
            exit 1
            ;;
    esac
}

main "$@"
