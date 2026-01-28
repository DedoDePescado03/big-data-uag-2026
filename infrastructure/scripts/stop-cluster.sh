#!/bin/bash
# =============================================================================
# Script para detener el cluster de Big Data
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

# Mostrar uso
usage() {
    echo "Uso: $0 [opcion]"
    echo ""
    echo "Opciones:"
    echo "  spark     - Detener solo Spark + Jupyter"
    echo "  kafka     - Detener solo Kafka"
    echo "  full      - Detener todo"
    echo "  all       - Detener todos los stacks"
    echo "  clean     - Detener todo y eliminar volumenes"
    echo "  help      - Mostrar esta ayuda"
    echo ""
    echo "Ejemplo: $0 spark"
}

# Detener Spark
stop_spark() {
    print_status "Deteniendo cluster Spark..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.spark.yml down 2>/dev/null || true
    print_success "Cluster Spark detenido"
}

# Detener Kafka
stop_kafka() {
    print_status "Deteniendo Kafka..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.kafka.yml down 2>/dev/null || true
    print_success "Kafka detenido"
}

# Detener Full Stack
stop_full() {
    print_status "Deteniendo Full Stack..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.full-stack.yml down 2>/dev/null || true
    print_success "Full Stack detenido"
}

# Detener todo
stop_all() {
    print_status "Deteniendo todos los servicios..."
    cd "$INFRA_DIR"
    docker compose -f docker-compose.spark.yml down 2>/dev/null || true
    docker compose -f docker-compose.kafka.yml down 2>/dev/null || true
    docker compose -f docker-compose.full-stack.yml down 2>/dev/null || true
    print_success "Todos los servicios detenidos"
}

# Limpieza completa
clean_all() {
    print_warning "Esto eliminara todos los contenedores y volumenes..."
    read -p "Continuar? (y/N): " confirm

    if [[ "$confirm" =~ ^[Yy]$ ]]; then
        print_status "Deteniendo y limpiando..."
        cd "$INFRA_DIR"
        docker compose -f docker-compose.spark.yml down -v 2>/dev/null || true
        docker compose -f docker-compose.kafka.yml down -v 2>/dev/null || true
        docker compose -f docker-compose.full-stack.yml down -v 2>/dev/null || true

        # Eliminar volumenes huerfanos
        docker volume prune -f 2>/dev/null || true

        print_success "Limpieza completa realizada"
    else
        print_status "Operacion cancelada"
    fi
}

# Main
main() {
    echo ""
    echo "=========================================="
    echo "  Big Data UAG 2026 - Stop Cluster"
    echo "=========================================="
    echo ""

    case "${1:-all}" in
        spark)
            stop_spark
            ;;
        kafka)
            stop_kafka
            ;;
        full)
            stop_full
            ;;
        all)
            stop_all
            ;;
        clean)
            clean_all
            ;;
        help|--help|-h)
            usage
            ;;
        *)
            print_warning "Opcion no reconocida: $1"
            usage
            exit 1
            ;;
    esac

    echo ""
}

main "$@"
