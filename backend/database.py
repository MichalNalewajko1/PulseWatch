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