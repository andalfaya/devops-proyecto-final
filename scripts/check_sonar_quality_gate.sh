#!/usr/bin/env bash
set -euo pipefail

SONAR_HOST_URL="${SONAR_HOST_URL:-http://localhost:9000}"
SONAR_TOKEN="${SONAR_TOKEN:?SONAR_TOKEN must be set}"
PROJECT_KEY="${1:-devops-lab}"
TIMEOUT=${2:-120}   # seconds
INTERVAL=5
ELAPSED=0

echo "⏳ Waiting for SonarQube analysis of project '${PROJECT_KEY}' (timeout: ${TIMEOUT}s, interval: ${INTERVAL}s)"

# poll SonarQube for analysis status
while [ "$ELAPSED" -lt "$TIMEOUT" ]; do
  resp=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/ce/component?component=${PROJECT_KEY}")
  taskId=$(echo "$resp" | jq -r '.queue[0].id // .current?.id // empty')

  if [ -z "$taskId" ]; then
    status=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${PROJECT_KEY}" | jq -r '.projectStatus.status')
    if [ "$status" = "OK" ]; then
      jq -n --arg project "$PROJECT_KEY" --arg status "$status" --arg elapsed "$ELAPSED" \
        '{project:$project, status:$status, elapsed_seconds:($elapsed|tonumber)}'
      exit 0
    else
      jq -n --arg project "$PROJECT_KEY" --arg status "$status" --arg elapsed "$ELAPSED" \
        '{project:$project, status:$status, elapsed_seconds:($elapsed|tonumber)}'
      exit 1
    fi
  fi

  task=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/ce/task?id=${taskId}")
  taskStatus=$(echo "$task" | jq -r '.task.status')
  echo "Sonar analysis task ${taskId} status: ${taskStatus} (elapsed: ${ELAPSED}s)"

  if [ "$taskStatus" = "SUCCESS" ]; then
    status=$(curl -s -u "${SONAR_TOKEN}:" "${SONAR_HOST_URL}/api/qualitygates/project_status?projectKey=${PROJECT_KEY}" | jq -r '.projectStatus.status')
    jq -n --arg project "$PROJECT_KEY" --arg status "$status" --arg elapsed "$ELAPSED" \
      '{project:$project, status:$status, elapsed_seconds:($elapsed|tonumber)}'
    if [ "$status" = "OK" ]; then
      exit 0
    else
      exit 1
    fi
  elif [ "$taskStatus" = "FAILED" ] || [ "$taskStatus" = "CANCELED" ]; then
    jq -n --arg project "$PROJECT_KEY" --arg status "$taskStatus" --arg elapsed "$ELAPSED" \
      '{project:$project, status:$status, elapsed_seconds:($elapsed|tonumber)}'
    exit 1
  fi

  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

jq -n --arg project "$PROJECT_KEY" --arg status "TIMEOUT" --arg elapsed "$ELAPSED" \
  '{project:$project, status:$status, elapsed_seconds:($elapsed|tonumber)}'
exit 1
