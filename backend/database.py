import sqlite3
from pathlib import Path


DATABASE_PATH = (
    Path(__file__).resolve().parent
    / "pulsewatch.db"
)


def initialize_database() -> None:
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS snapshots (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                computer_name TEXT NOT NULL,
                cpu_usage_percent REAL NOT NULL,
                memory_total_bytes INTEGER NOT NULL,
                memory_available_bytes INTEGER NOT NULL,
                memory_used_bytes INTEGER NOT NULL,
                memory_usage_percent REAL NOT NULL,
                disk_total_bytes INTEGER NOT NULL,
                disk_free_bytes INTEGER NOT NULL,
                disk_used_bytes INTEGER NOT NULL,
                disk_usage_percent REAL NOT NULL
            )
            """
        )

        connection.commit()
    finally:
        connection.close()

def save_snapshot(snapshot: dict) -> int:
    connection = sqlite3.connect(DATABASE_PATH)

    try:
        cursor = connection.execute(
            """
            INSERT INTO snapshots (
                timestamp,
                computer_name,
                cpu_usage_percent,
                memory_total_bytes,
                memory_available_bytes,
                memory_used_bytes,
                memory_usage_percent,
                disk_total_bytes,
                disk_free_bytes,
                disk_used_bytes,
                disk_usage_percent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot["timestamp"],
                snapshot["computer_name"],
                snapshot["cpu_usage_percent"],
                snapshot["memory"]["total_bytes"],
                snapshot["memory"]["available_bytes"],
                snapshot["memory"]["used_bytes"],
                snapshot["memory"]["usage_percent"],
                snapshot["disk"]["total_bytes"],
                snapshot["disk"]["free_bytes"],
                snapshot["disk"]["used_bytes"],
                snapshot["disk"]["usage_percent"]
            )
        )

        connection.commit()

        snapshot_id = cursor.lastrowid

        if snapshot_id is None:
            raise RuntimeError(
                "Nie udalo sie pobrac ID zapisanego pomiaru."
            )

        return snapshot_id
    finally:
        connection.close()

def get_latest_snapshots(limit: int) -> list[dict]:
    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    try:
        cursor = connection.execute(
            """
            SELECT
                id,
                timestamp,
                computer_name,
                cpu_usage_percent,
                memory_total_bytes,
                memory_available_bytes,
                memory_used_bytes,
                memory_usage_percent,
                disk_total_bytes,
                disk_free_bytes,
                disk_used_bytes,
                disk_usage_percent
            FROM snapshots
            ORDER BY id DESC
            LIMIT ?
            """,
            (limit,)
        )

        rows = cursor.fetchall()

        return [
            dict(row)
            for row in rows
        ]
    finally:
        connection.close()