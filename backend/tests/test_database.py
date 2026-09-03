import sqlite3
import database

def build_valid_snapshot() -> dict:
    return {
        "timestamp": "2026-09-03 12:00:00",
        "computer_name": "TEST-PC",
        "cpu_usage_percent": 25.0,
        "memory": {
            "total_bytes": 1000,
            "available_bytes": 400,
            "used_bytes": 600,
            "usage_percent": 60.0
        },
        "disk": {
            "total_bytes": 2000,
            "free_bytes": 500,
            "used_bytes": 1500,
            "usage_percent": 75.0
        }
    }


def test_initialize_database_creates_snapshots_table(monkeypatch, tmp_path):
    test_database_path = (tmp_path / "test_pulsewatch.db")


    monkeypatch.setattr(database, "DATABASE_PATH", test_database_path)

    database.initialize_database()

    assert test_database_path.exists()


    connection = sqlite3.connect(test_database_path)

    try:
        row = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
              AND name = 'snapshots'
            """
        ).fetchone()
    finally:
        connection.close()

    assert row is not None

def test_save_snapshot_stores_data_and_returns_id(monkeypatch, tmp_path):
    test_database_path = (tmp_path / "test_pulsewatch.db")

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database_path
    )

    database.initialize_database()

    snapshot = build_valid_snapshot()

    snapshot_id = database.save_snapshot(
        snapshot
    )

    assert snapshot_id == 1

    connection = sqlite3.connect(
        test_database_path
    )

    try:
        row = connection.execute(
            """
            SELECT
                timestamp,
                computer_name,
                cpu_usage_percent,
                memory_used_bytes,
                disk_used_bytes
            FROM snapshots
            WHERE id = ?
            """,
            (snapshot_id,)
        ).fetchone()
    finally:
        connection.close()

    assert row == (
        "2026-09-03 12:00:00",
        "TEST-PC",
        25.0,
        600,
        1500
    )