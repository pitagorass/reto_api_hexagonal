import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2 import pool
from typing import Optional
from ...models import PersonaOut
import time

class PostgresPersonRepository:
    def __init__(self, host, port, dbname, user, password, minconn=1, maxconn=5):
        self.dsn = dict(host=host, port=port, dbname=dbname, user=user, password=password)
        self._pool = None
        # Lazy init pool to avoid raising on import if env not set
        self._minconn = minconn
        self._maxconn = maxconn

    def _ensure_pool(self):
        if self._pool is None:
            if not all([self.dsn['host'], self.dsn['user'], self.dsn['password']]):
                raise RuntimeError('DB connection params not provided')
            # retry loop for transient connection errors (useful in cloud deployment)
            attempts = 0
            while True:
                try:
                    self._pool = pool.SimpleConnectionPool(self._minconn, self._maxconn, **self.dsn)
                    break
                except Exception as e:
                    attempts += 1
                    if attempts > 5:
                        raise
                    time.sleep(1)

    def create_person(self, identificacion: str, nombre: str, email: str) -> PersonaOut:
        self._ensure_pool()
        conn = self._pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('BEGIN;')
                # create schema if not exists (idempotent)
                cur.execute("""CREATE SCHEMA IF NOT EXISTS app;""")
                cur.execute("""CREATE TABLE IF NOT EXISTS app.personas (
                    id serial PRIMARY KEY,
                    identificacion varchar(64) UNIQUE NOT NULL,
                    nombre text NOT NULL,
                    email text NOT NULL,
                    created_at timestamptz DEFAULT now()
                );""")
                cur.execute(
                    'INSERT INTO app.personas(identificacion,nombre,email) VALUES(%s,%s,%s) RETURNING id,identificacion,nombre,email,created_at;',
                    (identificacion, nombre, email)
                )
                row = cur.fetchone()
                conn.commit()
                return PersonaOut(**row)
        except Exception:
            conn.rollback()
            raise
        finally:
            self._pool.putconn(conn)

    def get_person_by_id(self, id: int) -> Optional[PersonaOut]:
        self._ensure_pool()
        conn = self._pool.getconn()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute('SELECT id,identificacion,nombre,email,created_at FROM app.personas WHERE id=%s;', (id,))
                row = cur.fetchone()
                if not row:
                    return None
                return PersonaOut(**row)
        finally:
            self._pool.putconn(conn)
