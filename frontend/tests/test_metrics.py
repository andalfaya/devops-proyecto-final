"""Prueba de disponibilidad del endpoint /metrics."""

from app import app

def test_metrics_endpoint_available():
    """Verifica que /metrics expone las métricas Prometheus."""
    client = app.test_client()
    res = client.get("/metrics")
    assert res.status_code == 200
    data = res.data.decode()
    assert "frontend_http_requests_total" in data
    assert "frontend_request_latency_seconds" in data
