# Project Guidelines

## Architecture

- The app is a small FastAPI service in `src/app.py` that also serves the frontend from `src/static/`.
- Keep backend changes in `src/app.py` unless a task clearly justifies splitting modules.
- The frontend is plain HTML, CSS, and vanilla JavaScript in `src/static/index.html`, `src/static/styles.css`, and `src/static/app.js`.
- Application data is stored in the in-memory `activities` dictionary. Do not assume persistence unless the task explicitly adds it.

## Build And Test

- Install dependencies from the repository root with `pip install -r requirements.txt`.
- Run the app from the repository root with `python src/app.py`.
- Use `pytest` for tests. `pytest.ini` sets `pythonpath = .`, so tests should run from the repository root.
- There is no frontend build step.

## Conventions

- Preserve the current teaching-oriented scope of the project: prefer small, readable changes over premature abstraction.
- Keep the API and frontend aligned. If endpoint shapes or error messages change, update the frontend code that calls them.
- Activity names are currently used as identifiers in routes and in the in-memory data model.
- Existing behavior is intentionally simple: no database, no authentication, and limited validation unless the task requires expanding those areas.

## Documentation

- Link to existing docs instead of duplicating them.
- Use `README.md` for repository and exercise context.
- Use `src/README.md` for application behavior, API endpoints, and local usage notes.
- The guided exercise material lives under `.github/steps/`; reference it rather than copying step content into code comments or new docs.