# Todo List Backend

A simple FastAPI backend for managing a todo list, built using Python and SQLAlchemy.

## Getting Started

This project uses [uv](https://docs.astral.sh/uv/) for package management and dependency installation.

### Prerequisites

Make sure you have `uv` installed:
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Install Dependencies

After installing `uv`, install the project dependencies with:

```powershell
uv sync
```

This will create a virtual environment and install `fastapi`, `pydantic`, `sqlalchemy`, `uvicorn`, and any other dependencies listed in `pyproject.toml`.

### Running the Application

To start the development server with auto-reload:

```powershell
uv run uvicorn main:app --reload
```

The server will be available at `http://127.0.0.1:8000`.

## API Documentation

Once the server is running, you can access the modern API documentation at:
- **Scalar**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Project Structure

- `main.py`: Entry point and API routes.
- `models.py`: SQLAlchemy database models.
- `schemas.py`: Pydantic models for data validation.
- `database.py`: Database connection and session management.
- `todo.db`: SQLite database file (generated on first run).
