# Todo App — Implementation Plan

## Overview

Build a minimal todo application with a **Python 3.13 FastAPI backend** and a **Vanilla JS frontend**. The backend persists data in a local **SQLite** database via **SQLAlchemy (sync)**. FastAPI serves both the REST API and the static frontend from a single process bound to `127.0.0.1`.

**Scope:** CRUD only — create, list, toggle complete, delete. No auth, no timestamps, no build step.

**Out of scope:** authentication, multi-user support, async DB, any JS framework or bundler.

---

## Project Structure

```
app/
  main.py          — FastAPI app entry point; mounts StaticFiles; includes router
  database.py      — SQLAlchemy engine, SessionLocal, Base
  models.py        — ORM model: Todo
  schemas.py       — Pydantic request/response schemas
  routers/
    todos.py       — CRUD route handlers
static/
  index.html       — Single-file Vanilla JS frontend
requirements.txt
```

---

## Sub-Tasks

---

### Sub-Task 1 — Project Scaffolding

**Status:** `[ ] pending`

**Intent**
Establish the folder layout and pin all dependencies so every subsequent sub-task has a reproducible base to build on.

**Expected Outcomes**
- `requirements.txt` exists with pinned, actively-maintained, non-EOL package versions compatible with Python 3.13.
- The `app/`, `app/routers/`, and `static/` directories exist with placeholder `__init__.py` files where needed.
- Running `pip install -r requirements.txt` installs without errors.

**Todo List**
- [ ] Create `requirements.txt` with: `fastapi`, `uvicorn[standard]`, `sqlalchemy` — all at their latest stable versions compatible with Python 3.13.
- [ ] Create `app/__init__.py` (empty).
- [ ] Create `app/routers/__init__.py` (empty).
- [ ] Create `static/` directory (can be empty — populated in Sub-Task 4).

**Relevant Context**
- Python version: 3.13.11
- Security rule: use latest stable, actively-maintained versions only; no EOL packages.

---

### Sub-Task 2 — Database Layer

**Status:** `[ ] pending`

**Intent**
Set up SQLAlchemy with a SQLite file-based database and define the `Todo` ORM model. This layer is the single source of truth for persistence; all other layers depend on it.

**Expected Outcomes**
- `app/database.py` exports: `engine`, `SessionLocal`, `Base`, and a `get_db` dependency.
- `app/models.py` exports a `Todo` ORM model with columns: `id` (int, PK, autoincrement), `title` (str, not null), `completed` (bool, default false).
- On first run, `todos.db` is auto-created in the project root via `Base.metadata.create_all`.

**Todo List**
- [ ] Create `app/database.py`: configure SQLAlchemy engine pointing to `todos.db` in the project root; define `SessionLocal`; define `Base`; define `get_db` as a generator dependency (yields session, closes in finally).
- [ ] Create `app/models.py`: define `Todo` class inheriting from `Base` with the three columns described above.

**Relevant Context**
- Use synchronous SQLAlchemy (not async) — keeps the code straightforward.
- `get_db` will be injected via FastAPI's `Depends` in the router.
- Security: the SQLite file path should be configurable via an environment variable with a safe default so it can be overridden without code changes.

---

### Sub-Task 3 — API Layer

**Status:** `[ ] pending`

**Intent**
Define Pydantic schemas for request/response validation, implement the five CRUD endpoints, and wire everything into the FastAPI application. This sub-task produces a fully functional REST API testable with `curl` or a REST client.

**Expected Outcomes**
- `app/schemas.py` defines: `TodoCreate` (title: str), `TodoUpdate` (completed: bool), `TodoResponse` (id, title, completed).
- `app/routers/todos.py` implements:
  - `GET /todos` — return all todos.
  - `POST /todos` — create a new todo; returns 201.
  - `PATCH /todos/{id}` — toggle completed; returns 404 if not found.
  - `DELETE /todos/{id}` — delete by id; returns 204 if deleted, 404 if not found.
- `app/main.py` creates the FastAPI app, includes the todos router, mounts `static/` as StaticFiles at `/static`, and serves `static/index.html` at `GET /`.
- Uvicorn starts the app bound to `127.0.0.1` (never `0.0.0.0`).

**Todo List**
- [ ] Create `app/schemas.py` with `TodoCreate`, `TodoUpdate`, and `TodoResponse` (with `model_config = ConfigDict(from_attributes=True)` for ORM mode).
- [ ] Create `app/routers/todos.py` with the four endpoints listed above, using `Depends(get_db)` for DB access.
- [ ] Create `app/main.py`: instantiate `FastAPI`, call `Base.metadata.create_all(bind=engine)` on startup, include the todos router, mount `StaticFiles`, add root route returning `FileResponse("static/index.html")`.
- [ ] Confirm uvicorn is configured to bind to `127.0.0.1` (document in README or startup command).

**Relevant Context**
- Pydantic v2 ships with FastAPI — use `model_config = ConfigDict(from_attributes=True)` (not the v1 `class Config`).
- Error responses must return generic messages — no stack traces or internal detail exposed to the client (security rule).
- No CORS middleware needed: single-origin, single-process.

---

### Sub-Task 4 — Frontend

**Status:** `[ ] pending`

**Intent**
Build a single `static/index.html` file that uses the browser's native `fetch` API to interact with the backend. No framework, no build step, no external CDN dependencies.

**Expected Outcomes**
- `static/index.html` renders a text input + "Add" button to create todos.
- The todo list renders each item with its title, a checkbox to toggle `completed`, and a delete button.
- All four API endpoints are consumed correctly.
- The UI reflects the current server state on load and after every mutation (re-fetches from API).
- All API calls target relative URLs (e.g. `/todos`) so they work regardless of port.

**Todo List**
- [ ] Create `static/index.html` with inline `<style>` for minimal styling and an inline `<script>` section.
- [ ] Implement `fetchTodos()` — calls `GET /todos`, renders the list.
- [ ] Implement `addTodo()` — reads input value, calls `POST /todos`, clears input, re-renders.
- [ ] Implement `toggleTodo(id, completed)` — calls `PATCH /todos/{id}`, re-renders.
- [ ] Implement `deleteTodo(id)` — calls `DELETE /todos/{id}`, re-renders.
- [ ] Call `fetchTodos()` on `DOMContentLoaded`.

**Relevant Context**
- Use relative URLs only — the frontend is served from the same origin as the API.
- No external scripts or stylesheets — no network dependency at runtime.

---

### Sub-Task 5 — Integration Verification

**Status:** `[ ] pending`

**Intent**
Confirm the full stack works end-to-end: the server starts cleanly, the DB is created, the frontend loads, and all four CRUD operations succeed via the browser UI.

**Expected Outcomes**
- `uvicorn app.main:app --host 127.0.0.1 --port 8000` starts without errors.
- `todos.db` is created in the project root on first run.
- Navigating to `http://127.0.0.1:8000` loads the frontend.
- Adding, toggling, and deleting todos all work correctly through the UI.
- No unhandled exceptions appear in the uvicorn log during normal use.

**Todo List**
- [ ] Start the app and confirm it boots without import or DB errors.
- [ ] Open `http://127.0.0.1:8000` in a browser and confirm the frontend loads.
- [ ] Add a todo item via the UI — confirm it appears in the list and in `todos.db`.
- [ ] Toggle the completed checkbox — confirm the state persists across a page refresh.
- [ ] Delete a todo — confirm it is removed from the list.
- [ ] Confirm uvicorn log shows no unhandled exceptions throughout.

**Relevant Context**
- This sub-task is read/run-only — fix any bugs found in the relevant prior sub-task's files rather than patching here.
