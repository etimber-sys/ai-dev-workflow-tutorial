# Research: Sales Performance Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-10
**Phase**: 0 — Outline & Research

---

## Decision 1: Single-File Architecture (`app.py`)

**Decision**: All application code lives in a single `app.py` at the repository root.

**Rationale**: The dashboard has one screen, one data source, and four views. Splitting
into modules (data.py, charts.py) would add indirection with no benefit at this scope.
Streamlit's top-to-bottom execution model is a natural fit for a linear single file.
The constitution's Principle V (Ship Minimal) explicitly discourages structural
over-engineering.

**Alternatives considered**:
- `app.py` + `data.py` + `charts.py` — rejected; premature abstraction for ~80 lines of code
- `src/` package layout — rejected; adds `__init__.py` overhead with no import benefit

---

## Decision 2: Docker Base Image — `python:3.11-slim`

**Decision**: Use `python:3.11-slim` as the Docker base image.

**Rationale**: The slim variant (~130MB) provides the right balance of image size and
compatibility. pandas and plotly rely on C extensions (numpy, etc.) that can fail to
build on Alpine (`musl libc` incompatibilities). The Debian-based slim image ships
compatible system libraries out of the box.

**Alternatives considered**:
- `python:3.11-alpine` — rejected; known C-extension build failures with pandas/numpy
- `ghcr.io/astral-sh/uv:python3.11-bookworm-slim` — valid option but adds an
  external registry dependency; `python:3.11-slim` + `pip install uv` is more portable
- Multi-stage build — over-engineered for a single-file app; not warranted until
  image size becomes a measurable problem

**Installation approach**: Install uv via `pip install uv` inside the image, then use
`uv sync` to install project dependencies from `pyproject.toml`.

---

## Decision 3: Local Development — `uv run streamlit run app.py`

**Decision**: Developers run the app locally with `uv run streamlit run app.py`.

**Rationale**: `uv run` automatically creates and manages a virtual environment based on
`pyproject.toml` with no manual activation step. This eliminates the "wrong Python"
class of errors and is consistent with how uv is used in the Docker build. First-time
setup is a single command: `uv run streamlit run app.py` (uv creates the venv and
installs deps on first run).

**Alternatives considered**:
- Manual `uv venv` + activate — more explicit but more steps; no advantage for a
  single-developer project
- Docker-only development — too heavy for the inner development loop; local run is
  needed for quick iteration

---

## Decision 4: Streamlit Configuration — Theme Config

**Decision**: Include a `.streamlit/config.toml` with a custom theme and server settings.

**Rationale**: The primary audience is executives in presentation settings. A polished,
professional color scheme (clean blue primary, white background) reinforces trust and
readability. Server settings (`headless = true`) are required for Docker to prevent
Streamlit from attempting to open a browser inside the container.

**Configuration values**:
```toml
[server]
headless = true
port = 8501

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"
```

**Alternatives considered**:
- No config file — simpler but Streamlit defaults show a "Deploy" button and email
  prompt that are distracting in executive presentations
- Full config — `browserServerAddress` not needed; adds complexity without benefit

---

## Decision 5: Data Loading — `@st.cache_data`

**Decision**: Use Streamlit's `@st.cache_data` decorator on the `load_data()` function.

**Rationale**: `@st.cache_data` caches the DataFrame in memory after the first load.
Subsequent page interactions (hover, scroll) do not re-read the CSV from disk.
For a ~1,000-row static file this is negligible in practice, but it's the idiomatic
Streamlit pattern and future-proofs the function if the dataset grows.

**Alternatives considered**:
- `@st.cache_resource` — designed for shared resources (DB connections, ML models);
  wrong semantic for a DataFrame return value
- No caching — functionally fine for this dataset size but non-idiomatic

---

## Decision 6: Dependency Management — `pyproject.toml` (uv)

**Decision**: Declare dependencies in `pyproject.toml` managed by uv; no `requirements.txt`.

**Rationale**: The constitution explicitly lists `uv` as the dependency management tool.
`pyproject.toml` is the modern Python standard (PEP 517/518/621). uv reads it natively.
A `requirements.txt` would be redundant and create a two-source-of-truth problem.

**Pinning strategy**: Specify minimum versions only (e.g., `streamlit>=1.32`, `pandas>=2.0`)
rather than exact pins. The Docker build will resolve to the latest compatible versions,
ensuring security patches are picked up on rebuild.

**Alternatives considered**:
- `requirements.txt` — familiar but not aligned with uv's preferred workflow
- Exact pins (`streamlit==1.32.0`) — prevents security updates; over-constrained for a
  demo dashboard
