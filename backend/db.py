import os
import time
import psycopg2
from psycopg2 import OperationalError, sql

DB_URL = os.environ.get(
    "DATABASE_URL",
    "postgresql://postgres:postgres@postgres:5432/postgres"
)

def get_conn(retries=10, delay=3):
    """Crea conexión a PostgreSQL con reintentos."""
    attempt = 0
    while attempt < retries:
        try:
            return psycopg2.connect(DB_URL)
        except OperationalError:
            attempt += 1
            print(f"[DB] No disponible, reintentando {attempt}/{retries}...")
            time.sleep(delay)
    raise OperationalError(f"No se pudo conectar a PostgreSQL después de {retries} intentos")


def init_db():
    conn = get_conn()
    cur = conn.cursor()

    # DROP TABLE asegura que la tabla se crea limpia
    cur.execute("DROP TABLE IF EXISTS users CASCADE;")
    cur.execute("""
        CREATE TABLE users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255),
            email VARCHAR(255)
        );
    """)
    conn.commit()

    cur.close()
    conn.close()
    print("[DB] Inicialización completa")
