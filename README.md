# PulseWatch

PulseWatch is a local system monitoring application for Windows.

A native C++ agent collects CPU, memory and disk usage metrics and sends them as JSON to a FastAPI backend. The backend validates the data, stores it in SQLite and exposes it through a REST API. A browser dashboard displays the latest measurement and resource usage history.

## Features

- Windows system metrics collected by a native C++ agent
- CPU, RAM and disk usage monitoring
- JSON serialization and HTTP communication through WinINet
- REST API built with FastAPI
- Input and output validation with Pydantic
- Persistent storage in SQLite
- Automatically refreshed browser dashboard
- Resource history chart built with Chart.js
- Agent activity status
- Configurable number of chart points
- Automated tests with pytest

## Architecture

```text
C++ monitoring agent
        |
        | POST /api/v1/snapshots
        v
FastAPI + Pydantic
        |
        v
SQLite database
        ^
        |
        | GET /api/v1/snapshots
        |
Browser dashboard
```

## Technologies

### Agent

- C++
- Windows API
- WinINet
- CMake

### Backend

- Python
- FastAPI
- Pydantic
- SQLite

### Frontend

- HTML
- CSS
- JavaScript
- Chart.js

### Testing

- pytest
- FastAPI TestClient
- Temporary SQLite databases
