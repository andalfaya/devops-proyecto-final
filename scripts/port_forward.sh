#!/usr/bin/env bash
# scripts/port_forward.sh
set -e

ENV=$1
BACKEND_PORT=$2
FRONTEND_PORT=$3

echo "Esperando que los servicios estén disponibles..."
sleep 5

pkill -f "kubectl port-forward svc/backend" || true
pkill -f "kubectl port-forward svc/frontend" || true

nohup kubectl port-forward svc/backend ${BACKEND_PORT}:8000 -n ${ENV} >/tmp/backend_${ENV}.log 2>&1 &
nohup kubectl port-forward svc/frontend ${FRONTEND_PORT}:80 -n ${ENV} >/tmp/frontend_${ENV}.log 2>&1 &

echo "Servicios accesibles en:"
echo "  Backend:  http://localhost:${BACKEND_PORT}"
echo "  Frontend: http://localhost:${FRONTEND_PORT}"