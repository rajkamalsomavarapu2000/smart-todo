import sqlite3
from pathlib import Path

DB_PATH = Path(".todo.sqlite3")

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                notes TEXT DEFAULT '',
                tags TEXT DEFAULT '',
                created_at TEXT NOT NULL,
                due_at TEXT,
                done INTEGER NOT NULL DEFAULT 0,
                done_at TEXT
            )
            """
        )
        conn.commit()
