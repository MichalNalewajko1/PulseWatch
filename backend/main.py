from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(title="PulseWatch API")


class MemoryMetrics(BaseModel):
    total_bytes: int
    available_bytes: int
    used_bytes: int
    usage_percent: float


class DiskMetrics(BaseModel):
    total_bytes: int
    free_bytes: int
    used_bytes: int
    usage_percent: float


class SystemSnapshotPayload(BaseModel):
    timestamp: str
    computer_name: str
    cpu_usage_percent: float
    memory: MemoryMetrics
    disk: DiskMetrics


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/api/v1/snapshots")
def receive_snapshot(snapshot: SystemSnapshotPayload):
    print(snapshot.model_dump())

    return {
        "status": "accepted",
        "computer_name": snapshot.computer_name,
        "timestamp": snapshot.timestamp
    }