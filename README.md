# PulseWatch

PulseWatch is a local system monitoring application for Windows.

A native C++ agent collects CPU, memory and disk usage metrics and sends them as JSON to a FastAPI backend. The backend validates the data, stores it in SQLite and exposes it through a REST API. A browser dashboard displays the latest measurement and resource usage history.

## Features

- Windows system metrics collected by a native C++ agent
- CPU, RAM and disk usage monitoring
- JSON serialization and HTTP communication through WinHTTP- REST API built with FastAPI
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
- WinHTTP
- nlohmann/json
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

## Requirements

- Windows 10 or Windows 11
- CMake 3.16 or newer
- A compiler supporting C++20
- Git
- Python 3
- A modern web browser
- An internet connection during the first CMake configuration

## Building the C++ agent

Run the following commands from the project root:

```powershell
cmake -S . -B build
```

```powershell
cmake --build build --config Release
```

CMake automatically downloads the required `nlohmann/json` dependency during the first configuration.

The executable location depends on the selected CMake generator.

For a Visual Studio generator:

```powershell
.\build\Release\PulseWatch_or.exe
```

For a single-configuration generator such as Ninja or MinGW:

```powershell
.\build\PulseWatch_or.exe
```

If the executable location is unknown, find it with:

```powershell
Get-ChildItem .\build -Filter PulseWatch_or.exe -Recurse
```

Start the FastAPI backend before running the agent. The agent sends collected snapshots to:

```text
http://127.0.0.1:8000/api/v1/snapshots
```

## Backend setup

Run the following commands from the project root:

```powershell
python -m venv backend\.venv
```

```powershell
.\backend\.venv\Scripts\python.exe -m pip install -r backend\requirements.txt
```

Start the FastAPI development server:

```powershell
.\backend\.venv\Scripts\fastapi.exe dev .\backend\main.py
```

The following addresses will then be available:

- Dashboard: http://127.0.0.1:8000/dashboard/
- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Running tests

Enter the backend directory:

```powershell
cd backend
```

Run the complete test suite:

```powershell
.\.venv\Scripts\python.exe -m pytest tests -q
```

The tests use temporary SQLite databases and do not modify the local `pulsewatch.db` file.

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/health` | Checks whether the API is running |
| `POST` | `/api/v1/snapshots` | Validates and stores a system snapshot |
| `GET` | `/api/v1/snapshots?limit=10` | Returns the latest snapshots |
| `GET` | `/dashboard/` | Opens the browser dashboard |
