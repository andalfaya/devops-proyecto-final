"""Pruebas para el endpoint /api/users."""

import pytest
from main import app
from db import get_conn, init_db

@pytest.fixture(scope="module", autouse=True)
def setup_db():
    """Inicializa la base de datos de pruebas."""
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users;")  # limpia usuarios previos
    conn.commit()
    conn.close()
    yield
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM users;")
    conn.commit()
    conn.close()


def test_post_user_success():
    """Debe crear un usuario correctamente."""
    client = app.test_client()
    res = client.post("/api/users", json={"name": "Alice", "email": "alice@test.com"})
    assert res.status_code == 201
    data = res.json
    assert "id" in data
    assert data["name"] == "Alice"
    assert data["email"] == "alice@test.com"


def test_post_user_missing_field():
    """Debe devolver error si falta un campo."""
    client = app.test_client()
    res = client.post("/api/users", json={"name": "Bob"})
    assert res.status_code == 400
    assert res.json["error"] == "Missing fields"


def test_get_users_returns_list():
    """Debe devolver lista de usuarios existente."""
    client = app.test_client()
    res = client.get("/api/users")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert all("name" in u and "email" in u for u in res.json)


def test_get_users_after_insert():
    """Verifica que el usuario insertado aparece en GET /api/users."""
    client = app.test_client()
    client.post("/api/users", json={"name": "Charlie", "email": "charlie@test.com"})
    res = client.get("/api/users")
    emails = [u["email"] for u in res.json]
    assert "charlie@test.com" in emails
