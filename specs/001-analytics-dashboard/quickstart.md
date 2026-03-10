# Quickstart: Sales Performance Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-10

---

## Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) installed
- Docker (for container verification)
- The repository cloned locally with `data/sales-data.csv` present

---

## Local Development

### First run (installs dependencies automatically)

```bash
uv run streamlit run app.py
```

uv creates a virtual environment and installs all dependencies from `pyproject.toml`
on the first run. Subsequent runs skip the install step.

Open `http://localhost:8501` in your browser.

### Expected output

```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

### Verify KPI baselines

Once the dashboard loads, confirm:
- **Total Sales**: ~$650,000–$700,000
- **Total Orders**: 482

These are your visual verification checkpoints (Constitution Principle III).

---

## Docker Build & Run

### Build the image

```bash
docker build -t sales-dashboard .
```

### Run the container

```bash
docker run -p 8501:8501 sales-dashboard
```

Open `http://localhost:8501` — the dashboard should load identically to local dev.

### Verify container parity

Check that KPI values, chart shapes, and layout match the local run exactly.
This satisfies Constitution Principle IV (Container-First Deployment).

---

## Validation Checklist

Run through this after every code change before committing:

- [ ] `uv run streamlit run app.py` — app launches without errors
- [ ] "Sales Performance Dashboard" title visible at top
- [ ] "Total Sales" KPI card shows ~$650K–$700K
- [ ] "Total Orders" KPI card shows 482
- [ ] Sales Trend line chart shows 12 monthly data points
- [ ] Hover tooltip on trend chart shows month + revenue value
- [ ] "Sales by Category" bar chart shows 5 bars, sorted descending
- [ ] "Sales by Region" bar chart shows 4 bars, sorted descending
- [ ] Both bar charts appear side by side
- [ ] `docker build -t sales-dashboard . && docker run -p 8501:8501 sales-dashboard` — container runs cleanly

---

## Troubleshooting

**`FileNotFoundError: data/sales-data.csv`**
Run the app from the repository root directory, not a subdirectory.

**Port 8501 already in use**
Another Streamlit instance is running. Stop it or use:
```bash
uv run streamlit run app.py --server.port 8502
```

**Docker build fails on pandas/numpy**
Ensure you're using `python:3.11-slim` (not Alpine) as the base image.
