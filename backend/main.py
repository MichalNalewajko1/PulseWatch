from typing import Self
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, status
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, model_validator
from database import get_latest_snapshots, initialize_database, save_snapshot

STATIC_DIRECTORY = (
    Path(__file__).resolve().parent
    / "static"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield


app = FastAPI(
    title="PulseWatch API",
    lifespan=lifespan
)

app.mount(
    "/dashboard",
    StaticFiles(
        directory=STATIC_DIRECTORY,
        html=True
    ),
    name="dashboard"
)

class MemoryMetrics(BaseModel):
    total_bytes: int = Field(ge=0)
    available_bytes: int = Field(ge=0)
    used_bytes: int = Field(ge=0)
    usage_percent: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_byte_values(self) -> Self:
        calculated_total = (
            self.available_bytes
            + self.used_bytes
        )

        if calculated_total != self.total_bytes:
            raise ValueError(
                "available_bytes + used_bytes "
                "musi być równe total_bytes"
            )

        return self


class DiskMetrics(BaseModel):
    total_bytes: int = Field(ge=0)
    free_bytes: int = Field(ge=0)
    used_bytes: int = Field(ge=0)
    usage_percent: float = Field(ge=0, le=100)

    @model_validator(mode="after")
    def validate_byte_values(self) -> Self:
        calculated_total = (
            self.free_bytes
            + self.used_bytes
        )

        if calculated_total != self.total_bytes:
            raise ValueError(
                "free_bytes + used_bytes "
                "musi być równe total_bytes"
            )

        return self


class SystemSnapshotPayload(BaseModel):
    timestamp: str = Field(min_length=1)
    computer_name: str = Field(min_length=1, max_length=255)
    cpu_usage_percent: float = Field(ge=0, le=100)
    memory: MemoryMetrics
    disk: DiskMetrics


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/v1/snapshots")
def read_snapshots(
    limit: int = Query(
        default=10,
        ge=1,
        le=100
    )
):
    return get_latest_snapshots(limit)


@app.post(
    "/api/v1/snapshots",
    status_code=status.HTTP_201_CREATED
)
def receive_snapshot(snapshot: SystemSnapshotPayload):
    snapshot_id = save_snapshot(
        snapshot.model_dump()
    )

    return {
        "status": "accepted",
        "id": snapshot_id,
        "computer_name": snapshot.computer_name,
        "timestamp": snapshot.timestamp
    }