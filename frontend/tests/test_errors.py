"""Pruebas de errores y ramas no cubiertas en app.py."""

import pytest
import requests
from app import app


@pytest.fixture
def client_fixture():
    app.config["TESTING"] = True
    return app.test_client()


def test_metrics_endpoint(client_fixture):
    """Debe devolver métricas Prometheus."""
    res = client_fixture.get("/metrics")
    assert res.status_code == 200
    assert b"frontend_http_requests_total" in res.data


def test_home_page_backend_error(client_fixture, monkeypatch):
    """Simula backend devolviendo 500."""
    class MockResponse:
        status_code = 500
        def json(self): return {}
    monkeypatch.setattr("requests.get", lambda *a, **k: MockResponse())
    res = client_fixture.get("/")
    assert res.status_code == 200
    assert b"Error en backend" in res.data


def test_home_page_backend_unavailable(client_fixture, monkeypatch):
    """Simula fallo de conexión al backend."""
    def mock_get(*a, **k): raise requests.ConnectionError()
    monkeypatch.setattr("requests.get", mock_get)
    res = client_fixture.get("/")
    assert res.status_code == 200
    assert b"Backend no disponible" in res.data


def test_add_user_backend_timeout(client_fixture, monkeypatch):
    """Simula timeout al crear usuario."""
    def mock_post(*a, **k): raise requests.Timeout()
    monkeypatch.setattr("requests.post", mock_post)
    res = client_fixture.post("/add", data={"name": "Eve", "email": "eve@test.com"})
    assert res.status_code == 302


def test_add_user_backend_connection_error(client_fixture, monkeypatch):
    """Simula error de conexión al crear usuario."""
    def mock_post(*a, **k): raise requests.ConnectionError()
    monkeypatch.setattr("requests.post", mock_post)
    res = client_fixture.post("/add", data={"name": "Zoe", "email": "zoe@test.com"})
    assert res.status_code == 302


def test_add_user_created_counter(client_fixture, monkeypatch):
    """Simula creación exitosa de usuario (201)."""
    class MockResponse:
        status_code = 201
    monkeypatch.setattr("requests.post", lambda *a, **k: MockResponse())
    res = client_fixture.post("/add", data={"name": "Tom", "email": "tom@test.com"})
    assert res.status_code == 302


def test_health_backend_unavailable(client_fixture, monkeypatch):
    """Simula backend caído en /health."""
    def mock_get(*a, **k): raise requests.ConnectionError()
    monkeypatch.setattr("requests.get", mock_get)
    res = client_fixture.get("/health")
    assert res.status_code == 200
    assert b"ok" in res.data
