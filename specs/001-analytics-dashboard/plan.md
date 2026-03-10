# Implementation Plan: Sales Performance Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-10 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-analytics-dashboard/spec.md`

---

## Summary

Build a single-page Streamlit dashboard that reads ShopSmart transaction data from a
static CSV and presents four executive-facing views: KPI scorecards (Total Sales,
Total Orders), a monthly sales trend line chart, and side-by-side bar charts for
revenue by category and revenue by region. The entire application lives in a single
`app.py`, is dependency-managed via uv (`pyproject.toml`), and is deployable as a
Docker container using a `python:3.11-slim` base image.

---

## Technical Context

**Language/Version**: Python 3.11+
**Primary Dependencies**: Streamlit ≥1.32, Plotly Express ≥5.18, pandas ≥2.0
**Dependency Management**: uv (`pyproject.toml`)
**Storage**: Static file — `data/sales-data.csv` (bundled in Docker image)
**Testing**: None — visual verification per Constitution Principle III
**Target Platform**: Docker container (Linux); local dev on macOS/Windows/Linux
**Project Type**: Single-file web dashboard (`app.py`)
**Performance Goals**: Full dashboard load < 5 seconds (SC-002); chart render < 2 seconds
**Constraints**: No external network calls; no authentication; widescreen/desktop only
**Scale/Scope**: ~1,000 CSV rows; single developer; single screen; no user accounts

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

| Principle | Gate | Status |
|-----------|------|--------|
| I. Stakeholder Clarity | All labels use plain business language; no raw field names exposed in UI; chart titles and axis labels present on all four views | ✅ PASS — enforced by FR-001 through FR-007; axis labels explicitly planned |
| II. Static Data Contract | `load_data()` reads only `data/sales-data.csv`; `@st.cache_data` on startup; no DB or API calls | ✅ PASS — single data source; FR-008 non-negotiable |
| III. Visual Verification | No test files; validation via quickstart.md checklist + known KPI baselines | ✅ PASS — quickstart.md checklist generated; automated tests explicitly excluded |
| IV. Container-First Deployment | `python:3.11-slim` Dockerfile; `pyproject.toml` declares all deps; port 8501 exposed; CSV bundled at build time | ✅ PASS — Docker artifacts in scope; T020–T021 verify container parity |
| V. Ship Minimal, Iterate on Signal | Phase 1 scope: KPIs + trend + category + region only; filtering/export/auth explicitly out of scope | ✅ PASS — PRD Phase 2 items excluded; no speculative features in tasks |

**Post-design re-check**: All principles satisfied. No complexity violations to document.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-analytics-dashboard/
├── plan.md              # This file
├── research.md          # Phase 0 — architecture decisions
├── data-model.md        # Phase 1 — entities and derivations
├── quickstart.md        # Phase 1 — local dev + Docker run guide
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Task list (/speckit.tasks output)
```

### Source Code (repository root)

```text
app.py                   # Single-file Streamlit dashboard (all logic)
pyproject.toml           # uv-managed Python dependencies
Dockerfile               # Container build definition
.streamlit/
└── config.toml          # Theme + headless server config
data/
└── sales-data.csv       # Source dataset (pre-existing, bundled in Docker image)
```

**Structure Decision**: Single-file layout. `app.py` contains data loading,
aggregation, and all four UI views in linear top-to-bottom order. No modules,
packages, or subdirectories for source code. Justified by Constitution Principle V
(Ship Minimal) — the scope is too small to warrant abstraction layers.

---

## Phase 0: Research (Complete)

See [research.md](research.md) for full decision log.

**Key decisions**:
- `python:3.11-slim` Docker base — Debian compatibility, avoids Alpine/musl issues
- `uv run streamlit run app.py` — zero-friction local dev, no manual venv activation
- `.streamlit/config.toml` with professional theme — polished executive presentation
- `@st.cache_data` on `load_data()` — idiomatic Streamlit caching pattern
- `pyproject.toml` with minimum version pins — security-patch-compatible

---

## Phase 1: Design (Complete)

### Data Model

See [data-model.md](data-model.md) for full entity definitions.

**Entities**:
- **Transaction** — raw CSV rows; source of all data
- **KPI Summary** — `total_sales` (sum) + `total_orders` (count)
- **Monthly Revenue Summary** — grouped by `to_period("M")`; 12 rows
- **Category Revenue Summary** — grouped by `category`; 5 rows; sorted desc
- **Region Revenue Summary** — grouped by `region`; 4 rows; sorted desc

### Interface Contracts

No external API contracts. This is a self-contained Streamlit UI with no
programmatic interface to other systems. The only "contract" is the CSV schema
defined in the constitution (date, order_id, product, category, region,
quantity, unit_price, total_amount).

### Streamlit Config

`.streamlit/config.toml`:
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

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

RUN pip install uv

COPY pyproject.toml .
RUN uv sync

COPY app.py .
COPY data/ data/
COPY .streamlit/ .streamlit/

EXPOSE 8501

CMD ["uv", "run", "streamlit", "run", "app.py", \
     "--server.port=8501", "--server.address=0.0.0.0"]
```

### pyproject.toml

```toml
[project]
name = "sales-dashboard"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "streamlit>=1.32",
    "plotly>=5.18",
    "pandas>=2.0",
]
```

---

## Complexity Tracking

> No violations — all complexity decisions align with the constitution.

---

## Quickstart

See [quickstart.md](quickstart.md) for local dev and Docker run instructions.

**TL;DR**:
```bash
# Local dev
uv run streamlit run app.py

# Docker
docker build -t sales-dashboard . && docker run -p 8501:8501 sales-dashboard
```
