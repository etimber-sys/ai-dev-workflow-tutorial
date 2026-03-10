# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is a **tutorial documentation repository**, not a software project. It contains the instructional materials for an AI-assisted development workflow workshop. Participants fork this repo, then create their own Streamlit dashboard during the workshop.

The repo contains no application code to build, test, or lint — only Markdown documents and sample data.

## Repository structure

| Path | Purpose |
|------|---------|
| `v2/pre-work-setup.md` | Current pre-work guide (accounts, tool installs, repo setup) |
| `v2/workshop-build-deploy.md` | Current workshop guide (spec-kit → Jira → code → deploy) |
| `v1/` | Original two-session version of the tutorial (reference only) |
| `prd/ecommerce-analytics.md` | The PRD participants build from during the workshop |
| `data/sales-data.csv` | Sample dataset (ShopSmart transactions: date, order_id, product, category, region, quantity, unit_price, total_amount) |

## The workflow participants follow

```
PRD → spec-kit → Jira issues → Claude Code → git commit → GitHub push → Streamlit deploy
```

1. Read `prd/ecommerce-analytics.md`
2. Run `spec-kit` to generate constitution, specification, implementation plan, and tasks
3. Create Jira issues from the plan
4. Build a Streamlit dashboard with Claude Code (Python + pandas + Plotly)
5. Commit with Jira issue key in the message (e.g., `ECOM-1: Add KPI cards`)
6. Push to their GitHub fork
7. Deploy via Streamlit Community Cloud

## What participants build

A Streamlit dashboard reading from `data/sales-data.csv` with:
- KPI scorecards: Total Sales (~$650K–$700K) and Total Orders (482)
- Sales trend line chart (time series)
- Sales by category bar chart (Electronics, Accessories, Audio, Wearables, Smart Home)
- Sales by region bar chart (North, South, East, West)

Tech stack: Python 3.11+, Streamlit, Plotly, pandas, managed via `uv`.

## Editing tutorial content

All content is Markdown. When editing, preserve:
- The ASCII workflow diagrams (they render in Markdown)
- Step numbering (participants follow them sequentially in a live workshop)
- Callout formatting for warnings and tips
- The traceability convention: commit messages include Jira issue keys like `ECOM-1`

## Active Technologies
- Python 3.11+ + Streamlit ≥1.32, Plotly Express ≥5.18, pandas ≥2.0 (001-analytics-dashboard)
- Static file — `data/sales-data.csv` (bundled in Docker image) (001-analytics-dashboard)

## Recent Changes
- 001-analytics-dashboard: Added Python 3.11+ + Streamlit ≥1.32, Plotly Express ≥5.18, pandas ≥2.0
