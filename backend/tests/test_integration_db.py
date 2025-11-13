import psycopg2
import os
from db import init_db, get_conn

def test_db_insert_select():
    os.environ["DATABASE_URL"] = "postgresql://postgres:postgres@localhost:5433/postgres"
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id;", ("test", "test@example.com"))
    uid = cur.fetchone()[0]
    conn.commit()

    cur.execute("SELECT name, email FROM users WHERE id = %s;", (uid,))
    row = cur.fetchone()
    conn.close()

    assert row[0] == "test"
    assert row[1] == "test@example.com"
