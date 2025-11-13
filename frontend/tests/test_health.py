"""Pruebas para verificar métricas de salud expuestas por Prometheus."""

from app import app

def test_health_metrics():
    """Verifica que las métricas se actualizan tras acceder a /health."""
    client = app.test_client()
    client.get("/health")

    res = client.get("/metrics")
    body = res.data.decode("utf-8")

    assert 'frontend_http_requests_total{method="GET",endpoint="/health",status="200"}' in body
    assert 'frontend_request_latency_seconds_bucket{endpoint="/health"' in body
