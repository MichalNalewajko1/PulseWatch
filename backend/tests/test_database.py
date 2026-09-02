import sqlite3

import database


def test_initialize_database_creates_snapshots_table(
    monkeypatch,
    tmp_path
):
    test_database_path = (
        tmp_path
        / "test_pulsewatch.db"
    )

    monkeypatch.setattr(
        database,
        "DATABASE_PATH",
        test_database_path
    )

    database.initialize_database()

    assert test_database_path.exists()

    connection = sqlite3.connect(
        test_database_path
    )

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