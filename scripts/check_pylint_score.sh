#!/usr/bin/env bash
set -euo pipefail

# Uso: ./lint_score.sh <fichero> [min_score]
# Ejemplo: ./lint_score.sh backend/app.py 7.5

FILE=${1:? "Debes indicar el fichero a analizar"}
MIN_SCORE=${2:-6.0}   # umbral mínimo, por defecto 6.0

PYLINT_OUTPUT=$(mktemp)

# Ejecutar pylint con exit-zero para que no rompa el script
pylint --exit-zero "$FILE" > "$PYLINT_OUTPUT"

# Mostrar salida completa
cat "$PYLINT_OUTPUT"

# Extraer puntuación
SCORE_LINE=$(grep "Your code has been rated at" "$PYLINT_OUTPUT" || true)
if [[ -z "$SCORE_LINE" ]]; then
  echo "No se encontró la puntuación de pylint en la salida."
  rm -f "$PYLINT_OUTPUT"
  exit 1
fi

SCORE=$(echo "$SCORE_LINE" | awk -F' ' '{print $7}' | cut -d'/' -f1)

# Comparar con umbral
if awk "BEGIN{exit !($SCORE >= $MIN_SCORE)}"; then
  echo "Pylint score OK: $SCORE/10 (mínimo $MIN_SCORE)"
else
  echo "Pylint score demasiado bajo: $SCORE/10 (< $MIN_SCORE)"
  rm -f "$PYLINT_OUTPUT"
  exit 1
fi

rm -f "$PYLINT_OUTPUT"
