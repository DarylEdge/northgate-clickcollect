"""Thin data access layer.

Backed by SQLite by default. Set DATABASE_URL to a postgresql:// URL to use
PostgreSQL instead; the psycopg package is imported only if you do.
"""

import os
import sqlite3

DEFAULT_URL = "sqlite:///clickcollect.db"


def _url():
    return os.environ.get("DATABASE_URL", DEFAULT_URL)


def _sqlite_path(url):
    return url.replace("sqlite:///", "", 1)


def connect():
    """Open a connection to whichever database DATABASE_URL points at."""
    url = _url()
    if url.startswith("postgresql://"):
        import psycopg  # imported lazily so SQLite users need not install it

        conn = psycopg.connect(url)
        return conn
    conn = sqlite3.connect(_sqlite_path(url))
    conn.row_factory = sqlite3.Row
    return conn


def query(sql, params=()):
    """Run a SELECT and return a list of dict-like rows."""
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        columns = [d[0] for d in cur.description]
        return [dict(zip(columns, row)) for row in cur.fetchall()]
    finally:
        conn.close()


def query_one(sql, params=()):
    rows = query(sql, params)
    return rows[0] if rows else None


def execute(sql, params=()):
    """Run an INSERT or UPDATE and commit."""
    conn = connect()
    try:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()


SCHEMA = """
CREATE TABLE IF NOT EXISTS stores (
    id          INTEGER PRIMARY KEY,
    name        TEXT NOT NULL,
    town        TEXT NOT NULL,
    opens_at    TEXT NOT NULL,
    closes_at   TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
    sku         TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    price_pence INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS stock (
    store_id         INTEGER NOT NULL,
    sku              TEXT NOT NULL,
    quantity_on_hand INTEGER NOT NULL,
    PRIMARY KEY (store_id, sku)
);
CREATE TABLE IF NOT EXISTS reservations (
    reference      TEXT PRIMARY KEY,
    store_id       INTEGER NOT NULL,
    sku            TEXT NOT NULL,
    quantity       INTEGER NOT NULL,
    customer_email TEXT NOT NULL,
    status         TEXT NOT NULL,
    created_at     TEXT NOT NULL
);
"""


def create_schema():
    conn = connect()
    try:
        cur = conn.cursor()
        for statement in SCHEMA.strip().split(";"):
            if statement.strip():
                cur.execute(statement)
        conn.commit()
    finally:
        conn.close()


def reset():
    """Drop all rows. Used by the seed script and the test fixtures."""
    conn = connect()
    try:
        cur = conn.cursor()
        for table in ("reservations", "stock", "products", "stores"):
            cur.execute(f"DELETE FROM {table}")
        conn.commit()
    finally:
        conn.close()
