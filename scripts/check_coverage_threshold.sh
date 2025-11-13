#!/usr/bin/env bash
set -euo pipefail

# Uso: ./check_coverage_threshold.sh <coverage-xml> [min_coverage]
# Ejemplo: ./check_coverage_threshold.sh coverage-frontend.xml 70

TARGET=${1:? "Debes indicar el fichero XML de cobertura"}
MIN_COVERAGE=${2:-60}   # umbral mínimo, por defecto 60%

echo "🔍 Checking coverage threshold on '${TARGET}' (minimum: ${MIN_COVERAGE}%)"

if [ ! -f "$TARGET" ]; then
    echo "Coverage file not found: $TARGET"
    exit 1
fi

# Fuerza locale con punto decimal
export LC_NUMERIC=C

# Extraer SOLO la primera coincidencia de line-rate (nivel raíz)
LINE_RATE=$(grep -m1 -o 'line-rate="[0-9.,]*"' "$TARGET" \
  | sed 's/.*="//;s/"//' \
  | tr ',' '.')

if [[ -z "$LINE_RATE" ]]; then
    echo "No se pudo extraer el porcentaje de cobertura del XML"
    exit 1
fi

# Asegura 0 delante si empieza por punto (".9286" -> "0.9286")
LINE_RATE=$(echo "$LINE_RATE" | sed 's/^\./0./')

# Calcula porcentaje con bc
COVERAGE_PERCENT=$(echo "$LINE_RATE * 100" | bc -l)

# Formatea con dos decimales
COVERAGE_PERCENT=$(printf "%.2f" "$COVERAGE_PERCENT")

echo "📊 Coverage encontrado: ${COVERAGE_PERCENT}%"

# Compara con el umbral
if echo "$COVERAGE_PERCENT >= $MIN_COVERAGE" | bc -l | grep -q 1; then
    echo "Coverage OK: ${COVERAGE_PERCENT}% (mínimo ${MIN_COVERAGE}%)"
else
    echo "Coverage demasiado bajo: ${COVERAGE_PERCENT}% (< ${MIN_COVERAGE}%)"
    exit 1
fi
