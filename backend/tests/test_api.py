import pytest
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

def test_get_snapshots_returns_data(
    monkeypatch
):
    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None
    )

    expected_snapshots = [
        {
            "id": 9001,
            "timestamp": "2026-09-01 12:00:00",
            "computer_name": "TEST-PC",
            "cpu_usage_percent": 25.0,
            "memory_total_bytes": 1000,
            "memory_available_bytes": 400,
            "memory_used_bytes": 600,
            "memory_usage_percent": 60.0,
            "disk_total_bytes": 2000,
            "disk_free_bytes": 500,
            "disk_used_bytes": 1500,
            "disk_usage_percent": 75.0
        }
    ]

    def fake_get_latest_snapshots(
        limit
    ):
        assert limit == 1
        return expected_snapshots

    monkeypatch.setattr(
        main,
        "get_latest_snapshots",
        fake_get_latest_snapshots
    )

    with TestClient(main.app) as client:
        response = client.get(
            "/api/v1/snapshots?limit=1"
        )

    assert response.status_code == 200
    assert response.json() == expected_snapshots

@pytest.mark.parametrize(
    "invalid_limit",
    [0, 101]
)
def test_get_snapshots_rejects_invalid_limit(monkeypatch,invalid_limit):
    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None
    )


    def fail_if_database_is_called(_limit):
        raise AssertionError(
            "get_latest_snapshots nie powinno "
            "zostać wywołane"
        )

    monkeypatch.setattr(
        main,
        "get_latest_snapshots",
        fail_if_database_is_called
    )

    with TestClient(main.app) as client:
        response = client.get(
            f"/api/v1/snapshots"
            f"?limit={invalid_limit}"
        )

    assert response.status_code == 422

def test_get_snapshots_uses_default_limit(
    monkeypatch
):
    monkeypatch.setattr(
        main,
        "initialize_database",
        lambda: None
    )

    def fake_get_latest_snapshots(
        limit
    ):
        assert limit == 10
        return []

    monkeypatch.setattr(
        main,
        "get_latest_snapshots",
        fake_get_latest_snapshots
    )

    with TestClient(main.app) as client:
        response = client.get(
            "/api/v1/snapshots"
        )

    assert response.status_code == 200
    assert response.json() == []