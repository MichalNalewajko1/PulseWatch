from fastapi.testclient import TestClient

import main


def test_post_snapshot_returns_created(monkeypatch):
    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None
    )

    monkeypatch.setattr(
        main,
        "save_snapshot",
        lambda snapshot_data: 9001
    )

    payload = {
        "timestamp": "2026-09-01 12:00:00",
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

    with TestClient(main.app) as client:
        response = client.post(
            "/api/v1/snapshots",
            json=payload
        )

    assert response.status_code == 201

    assert response.json() == {
        "status": "accepted",
        "id": 9001,
        "computer_name": "TEST-PC",
        "timestamp": "2026-09-01 12:00:00"
    }

def test_post_invalid_snapshot_returns_422(
    monkeypatch
):
    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None
    )

    def fail_if_save_is_called(
        _snapshot_data
    ):
        raise AssertionError(
            "save_snapshot nie powinno zostać wywołane"
        )

    monkeypatch.setattr(
        main,
        "save_snapshot",
        fail_if_save_is_called
    )

    payload = {
        "timestamp": "2026-09-01 12:00:00",
        "computer_name": "TEST-PC",
        "cpu_usage_percent": 150.0,
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

    with TestClient(main.app) as client:
        response = client.post(
            "/api/v1/snapshots",
            json=payload
        )

    assert response.status_code == 422