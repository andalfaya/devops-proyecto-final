from flask import Flask, jsonify, request
from db import get_conn, init_db
import os
from prometheus_client import Counter, Histogram, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
import debugpy

DEBUG = os.environ.get("DEBUG", "0") == "1"

if DEBUG:
    debugpy.listen(("0.0.0.0", 5678))
    print("Backend esperando debugger en puerto 5678...")
    # debugpy.wait_for_client()  # opcional: bloquea hasta conexión del IDE

app = Flask(__name__)

# Inicializa DB de manera segura
init_db()

# Métricas Prometheus
REQUEST_COUNT = Counter(
    "backend_http_requests_total",
    "Total de peticiones HTTP",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "backend_request_latency_seconds",
    "Latencia por endpoint",
    ["endpoint"]
)

@app.route("/api/health", methods=["GET"])
def health():
    REQUEST_COUNT.labels("GET", "/api/health", 200).inc()
    return jsonify({"status": "ok"}), 200


@app.route("/api/users", methods=["GET", "POST"])
def users():
    if request.method == "POST":
        data = request.json or {}
        name = data.get("name")
        email = data.get("email")

        if not name or not email:
            REQUEST_COUNT.labels("POST", "/api/users", 400).inc()
            return jsonify({"error": "Missing fields"}), 400

        conn = get_conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
            (name, email)
        )
        new_id = cur.fetchone()[0]
        conn.commit()
        conn.close()

        REQUEST_COUNT.labels("POST", "/api/users", 201).inc()
        return jsonify({"id": new_id, "name": name, "email": email}), 201

    # GET
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users;")
    rows = cur.fetchall()
    conn.close()

    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    REQUEST_COUNT.labels("GET", "/api/users", 200).inc()
    return jsonify(users), 200


# Exponer métricas en /metrics
metrics_app = make_wsgi_app()
app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {"/metrics": metrics_app})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)
