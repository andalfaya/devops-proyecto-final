from app import app

def test_health_metrics():
    client = app.test_client()
    client.get("/health")

    # Ahora pedimos las métricas
    res = client.get("/metrics")
    body = res.data.decode("utf-8")

    # Verificamos que el counter se incrementó
    assert 'frontend_http_requests_total{method="GET",endpoint="/health",status="200"}' in body

    # Verificamos que el histograma de latencia existe
    assert 'frontend_request_latency_seconds_bucket{endpoint="/health"' in body
