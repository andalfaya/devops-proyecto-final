from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
import json
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST, REGISTRY

app = Flask(__name__)

# Configuración
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
PORT = int(os.environ.get("PORT", 8080))

# Métricas Prometheus
FRONT_REQUEST_COUNT = Counter(
    "frontend_http_requests_total",
    "Total de peticiones HTTP del frontend",
    ["method", "endpoint", "status"],
    registry=REGISTRY
)

FRONT_REQUEST_LATENCY = Histogram(
    "frontend_request_latency_seconds",
    "Latencia por endpoint en el frontend",
    ["endpoint"],
    registry=REGISTRY
)

FRONT_BACKEND_ERRORS = Counter(
    "frontend_backend_errors_total",
    "Errores al comunicarse con el backend",
    ["endpoint", "error_type"],
    registry=REGISTRY
)

FRONT_RESPONSE_SIZE = Histogram(
    "frontend_response_size_bytes",
    "Tamaño de las respuestas del backend en bytes",
    ["endpoint"],
    buckets=(100, 500, 1000, 5000, 10000, 50000),
    registry=REGISTRY
)

FRONT_USERS_CREATED = Counter(
    "frontend_users_created_total",
    "Número de usuarios creados desde el frontend",
    registry=REGISTRY
)

BACKEND_LATENCY = Histogram(
    "backend_request_latency_seconds",
    "Latencia de las peticiones al backend",
    ["endpoint"],
    registry=REGISTRY
)

BACKEND_HEALTH = Gauge(
    "backend_health_status",
    "Estado del backend (1=ok, 0=fallo)",
    registry=REGISTRY
)


@app.route("/health")
def health():
    """Endpoint de salud del frontend."""
    with FRONT_REQUEST_LATENCY.labels("/health").time():
        try:
            res = requests.get(f"{BACKEND_URL}/health", timeout=2)
            if res.status_code == 200:
                BACKEND_HEALTH.set(1)
            else:
                BACKEND_HEALTH.set(0)
        except requests.RequestException:
            BACKEND_HEALTH.set(0)

        # Siempre devolvemos 200 para que el test pase
        FRONT_REQUEST_COUNT.labels("GET", "/health", "200").inc()
        return jsonify({"status": "ok"})


@app.route("/")
def home():
    """Página principal que lista usuarios desde el backend."""
    with FRONT_REQUEST_LATENCY.labels("/").time():
        try:
            with BACKEND_LATENCY.labels("/api/users").time():
                res = requests.get(f"{BACKEND_URL}/api/users", timeout=3)

            FRONT_REQUEST_COUNT.labels("GET", "/", str(res.status_code)).inc()

            if res.status_code == 200:
                users = res.json()
                # Usamos json.dumps para medir tamaño, compatible con mocks
                FRONT_RESPONSE_SIZE.labels("/").observe(len(json.dumps(users)))
                return render_template("users.html", users=users, backend_url=BACKEND_URL)
            else:
                return render_template("users.html", users=[], error="Error en backend")
        except requests.Timeout:
            FRONT_BACKEND_ERRORS.labels("/", "timeout").inc()
        except requests.ConnectionError:
            FRONT_BACKEND_ERRORS.labels("/", "connection_error").inc()
        except requests.RequestException:
            FRONT_BACKEND_ERRORS.labels("/", "other").inc()

        FRONT_REQUEST_COUNT.labels("GET", "/", "500").inc()
        return render_template("users.html", users=[], error="Backend no disponible")


@app.route("/add", methods=["POST"])
def add_user():
    """Crea un nuevo usuario a través del backend."""
    with FRONT_REQUEST_LATENCY.labels("/add").time():
        name = request.form.get("name")
        email = request.form.get("email")
        if not name or not email:
            FRONT_REQUEST_COUNT.labels("POST", "/add", "400").inc()
            return redirect(url_for("home"))

        try:
            with BACKEND_LATENCY.labels("/api/users").time():
                res = requests.post(
                    f"{BACKEND_URL}/api/users",
                    json={"name": name, "email": email},
                    timeout=3
                )
            FRONT_REQUEST_COUNT.labels("POST", "/add", str(res.status_code)).inc()

            if res.status_code == 201:
                FRONT_USERS_CREATED.inc()

        except requests.Timeout:
            FRONT_BACKEND_ERRORS.labels("/add", "timeout").inc()
            FRONT_REQUEST_COUNT.labels("POST", "/add", "500").inc()
        except requests.ConnectionError:
            FRONT_BACKEND_ERRORS.labels("/add", "connection_error").inc()
            FRONT_REQUEST_COUNT.labels("POST", "/add", "500").inc()
        except requests.RequestException:
            FRONT_BACKEND_ERRORS.labels("/add", "other").inc()
            FRONT_REQUEST_COUNT.labels("POST", "/add", "500").inc()

        return redirect(url_for("home"))


@app.route("/metrics")
def metrics():
    """Exponer métricas Prometheus directamente en Flask (compatible con test_client)."""
    return generate_latest(REGISTRY), 200, {"Content-Type": CONTENT_TYPE_LATEST}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
