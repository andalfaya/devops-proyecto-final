"""Pruebas de integración para inserción y selección en la base de datos."""

import os
from db import init_db, get_conn

def test_db_insert_select():
    """Verifica que se puede insertar y recuperar un usuario en la base de datos."""
    os.environ["DATABASE_URL"] = (
        "postgresql://postgres:postgres@localhost:5433/postgres"
    )
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;",
        ("test", "test@example.com")
    )
    uid = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT name, email FROM users WHERE id = %s;", (uid,))
    row = cur.fetchone()
    conn.close()

    assert row[0] == "test"
    assert row[1] == "test@example.com"
