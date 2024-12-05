import psycopg2
from psycopg2 import pool
from contextlib import contextmanager
from settings import DB_CONFIG, POOL_MIN_CONN, POOL_MAX_CONN
import atexit

print("Initializing connection pool...")
connection_pool = psycopg2.pool.SimpleConnectionPool(
    POOL_MIN_CONN, POOL_MAX_CONN, **DB_CONFIG
)


@contextmanager
def get_connection():
    connection = connection_pool.getconn()
    try:
        yield connection
    finally:
        connection_pool.putconn(connection)


def close_connection_pool():
    if connection_pool:
        connection_pool.closeall()
        print("Connection pool closed.")


def on_exit():
    print("Приложение завершено! Закрываем ресурсы...")
    close_connection_pool()


atexit.register(on_exit)
