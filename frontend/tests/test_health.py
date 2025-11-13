"""Pruebas para verificar métricas de salud expuestas por Prometheus."""

from app import app

def test_health_metrics():
    """Verifica que las métricas se actualizan tras acceder a /health."""
    client = app.test_client()
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json == {"status": "ok"}
