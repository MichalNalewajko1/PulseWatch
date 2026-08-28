from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI, Query, status
from fastapi.staticfiles import StaticFiles
from database import get_latest_snapshots, initialize_database, save_snapshot
from schemas import (SnapshotCreatedResponse, SystemSnapshotPayload, SnapshotResponse)

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


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get(
    "/api/v1/snapshots",
    response_model=list[SnapshotResponse]
)
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
    status_code=status.HTTP_201_CREATED,
    response_model=SnapshotCreatedResponse
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