import pytest

from pydantic import ValidationError

from schemas import SystemSnapshotPayload


def build_valid_payload() -> dict:
    return {
        "timestamp": "2026-08-30 12:00:00",
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


def test_valid_snapshot_is_accepted():
    payload = build_valid_payload()

    snapshot = SystemSnapshotPayload(
        **payload
    )

    assert snapshot.computer_name == "TEST-PC"
    assert snapshot.timestamp == "2026-08-30 12:00:00"


def test_invalid_timestamp_is_rejected():
    payload = build_valid_payload()

    payload["timestamp"] = (
        "2026-13-30 12:00:00"
    )

    with pytest.raises(
        ValidationError,
        match="timestamp musi mieć format"
    ):
        SystemSnapshotPayload(
            **payload
        )

def test_cpu_above_100_is_rejected():
    payload = build_valid_payload()

    payload["cpu_usage_percent"] = 150.0

    with pytest.raises(ValidationError):
        SystemSnapshotPayload(
            **payload
        )


def test_inconsistent_memory_bytes_are_rejected():
    payload = build_valid_payload()

    payload["memory"]["used_bytes"] = 700

    with pytest.raises(ValidationError):
        SystemSnapshotPayload(
            **payload
        )


def test_inconsistent_disk_bytes_are_rejected():
    payload = build_valid_payload()

    payload["disk"]["used_bytes"] = 1600

    with pytest.raises(ValidationError):
        SystemSnapshotPayload(
            **payload
        )