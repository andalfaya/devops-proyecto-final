from flask import Flask, render_template, request, redirect, url_for, jsonify
import requests
import os
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

app = Flask(__name__)

# Configuración
BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")
PORT = int(os.environ.get("PORT", 8080))

# Métricas Prometheus
FRONT_REQUEST_COUNT = Counter(
    "frontend_http_requests_total",
    "Total de peticiones HTTP del frontend",
    ["method", "endpoint", "status"]
)

FRONT_REQUEST_LATENCY = Histogram(
    "frontend_request_latency_seconds",
    "Latencia por endpoint en el frontend",
    ["endpoint"]
)


@app.route("/health")
def health():
    FRONT_REQUEST_COUNT.labels("GET", "/health", 200).inc()
    return jsonify({"status": "ok"}), 200


@app.route("/")
def home():
    """Página principal que lista usuarios desde el backend."""
    try:
        res = requests.get(f"{BACKEND_URL}/api/users", timeout=3)
        users = res.json() if res.status_code == 200 else []
        FRONT_REQUEST_COUNT.labels("GET", "/", res.status_code).inc()
        return render_template("users.html", users=users, backend_url=BACKEND_URL)
    except requests.RequestException:
        FRONT_REQUEST_COUNT.labels("GET", "/", 500).inc()
        return render_template("users.html", users=[], error="Backend no disponible")


@app.route("/add", methods=["POST"])
def add_user():
    """Crea un nuevo usuario a través del backend."""
    name = request.form.get("name")
    email = request.form.get("email")
    if not name or not email:
        FRONT_REQUEST_COUNT.labels("POST", "/add", 400).inc()
        return redirect(url_for("home"))

    try:
        res = requests.post(
            f"{BACKEND_URL}/api/users",
            json={"name": name, "email": email},
            timeout=3
        )
        FRONT_REQUEST_COUNT.labels("POST", "/add", res.status_code).inc()
    except requests.RequestException:
        FRONT_REQUEST_COUNT.labels("POST", "/add", 500).inc()

    return redirect(url_for("home"))


# Exponer métricas Prometheus
metrics_app = make_wsgi_app()
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": metrics_app})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)
