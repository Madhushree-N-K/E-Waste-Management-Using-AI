# backend/app/db.py

import sqlite3
import os

# Database absolute path: backend/recyclers.db
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "recyclers.db")
DB_PATH = os.path.abspath(DB_PATH)

def _get_conn():
    """Create SQLite connection with Row factory."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """Creates recyclers table if not exists."""
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS recyclers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            accepted_items TEXT,        -- Comma-separated categories
            base_multiplier REAL,
            lat REAL,
            lon REAL,
            rating REAL,
            capacity_score REAL,
            pickup_available INTEGER,
            eco_certified INTEGER,
            contact TEXT
        )
    """)

    conn.commit()
    conn.close()
    print("Database initialized → recyclers.db")


def add_recycler(data: dict):
    """Insert a new recycler into DB."""
    conn = _get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO recyclers 
        (name, accepted_items, base_multiplier, lat, lon, rating, capacity_score, pickup_available, eco_certified, contact)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        data.get("accepted_items", ""),
        data["base_multiplier"],
        data.get("lat"),
        data.get("lon"),
        data.get("rating", 3.0),
        data.get("capacity_score", 0.7),
        int(bool(data.get("pickup_available", 0))),
        int(bool(data.get("eco_certified", 0))),
        data.get("contact", "")
    ))

    conn.commit()
    conn.close()


def get_all_recyclers():
    """Returns all recyclers."""
    conn = _get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM recyclers")
    rows = cur.fetchall()
    conn.close()

    return [dict(r) for r in rows]
