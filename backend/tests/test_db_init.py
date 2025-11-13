"""Pruebas para verificar la inicialización de la base de datos."""

from db import init_db, get_conn

def test_init_db_creates_table():
    """Verifica que init_db crea la tabla users si no existe."""
    init_db()
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT EXISTS (
            SELECT FROM information_schema.tables 
            WHERE table_name = 'users'
        );
    """)
    exists = cur.fetchone()[0]
    conn.close()
    assert exists is True
