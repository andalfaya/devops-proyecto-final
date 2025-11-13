"""Pruebas de vistas de usuario en la interfaz web."""

import pytest
from app import app


@pytest.fixture
def client_fixture():
    """Crea cliente de pruebas con configuración TESTING."""
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_loads(client_fixture, monkeypatch):
    """Carga de la página principal con usuarios mockeados."""
    class MockResponse:
        """Respuesta simulada para requests.get."""
        status_code = 200
        def json(self):
            return [{"id": 1, "name": "Alice", "email": "alice@test.com"}]

    monkeypatch.setattr("requests.get", lambda *_: MockResponse())
    res = client_fixture.get("/")
    assert res.status_code == 200
    assert b"Alice" in res.data
    assert b"Usuarios Registrados" in res.data


def test_add_user_redirect_success(client_fixture, monkeypatch):
    """Simula creación exitosa de usuario y redirección."""
    class MockResponse:
        """Respuesta simulada para requests.post."""
        status_code = 201

    monkeypatch.setattr("requests.post", lambda *_: MockResponse())
    res = client_fixture.post("/add", data={"name": "Bob", "email": "bob@test.com"})
    assert res.status_code == 302


def test_add_user_missing_field(client_fixture):
    """Debe redirigir sin enviar datos cuando faltan campos."""
    res = client_fixture.post("/add", data={"name": ""})
    assert res.status_code == 302
