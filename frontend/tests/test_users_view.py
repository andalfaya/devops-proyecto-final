import pytest
from app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()


def test_home_page_loads(client, monkeypatch):
    """Carga de la página principal con usuarios mockeados."""
    def mock_get(url, timeout):
        class MockResponse:
            status_code = 200
            def json(self):
                return [{"id": 1, "name": "Alice", "email": "alice@test.com"}]
        return MockResponse()

    monkeypatch.setattr("requests.get", mock_get)
    res = client.get("/")
    assert res.status_code == 200
    assert b"Alice" in res.data
    assert b"Usuarios Registrados" in res.data


def test_add_user_redirect_success(client, monkeypatch):
    """Simula creación exitosa de usuario y redirección."""
    def mock_post(url, json, timeout):
        class MockResponse:
            status_code = 201
        return MockResponse()

    monkeypatch.setattr("requests.post", mock_post)
    res = client.post("/add", data={"name": "Bob", "email": "bob@test.com"})
    assert res.status_code == 302  # redirige a home


def test_add_user_missing_field(client):
    """Debe redirigir sin enviar datos cuando faltan campos."""
    res = client.post("/add", data={"name": ""})
    assert res.status_code == 302  # redirección a home
