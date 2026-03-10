<!--
SYNC IMPACT REPORT
==================
Version change: (unversioned placeholder) → 1.0.0
Ratification: 2026-03-10 (initial adoption)
Last Amended:  2026-03-10

Modified principles: N/A — initial constitution (all principles are new)

Added sections:
  - Core Principles (5 principles)
  - Tech Stack & Data Contract
  - Development Workflow
  - Governance

Removed sections: N/A — first version

Templates reviewed:
  ✅ .specify/templates/plan-template.md
     — "Constitution Check" gate placeholder intact; will resolve per feature
  ✅ .specify/templates/spec-template.md
     — "User Scenarios & Testing" section aligns with visual-verification principle
  ✅ .specify/templates/tasks-template.md
     — Test tasks already marked OPTIONAL; consistent with Principle III

Follow-up TODOs: None — all placeholders resolved.
-->

# ShopSmart E-Commerce Analytics Dashboard Constitution

## Core Principles

### I. Stakeholder Clarity (NON-NEGOTIABLE)

Every chart, KPI card, and UI label MUST be immediately understandable to a
non-technical executive without any onboarding. Concretely:

- All metric names MUST use plain business language (e.g., "Total Revenue",
  not "sum_total_amount").
- Interactive controls MUST be limited to what is strictly necessary; no
  power-user configuration surfaces.
- Chart titles and axis labels MUST always be present and self-explanatory.
- Color choices MUST convey meaning clearly without relying on color alone.

**Rationale**: The primary audience is executives and stakeholders who consume
the dashboard in time-pressured settings. Cognitive load MUST be minimized.

### II. Static Data Contract (NON-NEGOTIABLE)

The dashboard MUST read exclusively from a single local CSV file
(`data/sales-data.csv`). No live database connections, external APIs, or
network calls are permitted.

- Data loading MUST occur once at application startup via `@st.cache_data`.
- The CSV schema (date, order_id, product, category, region, quantity,
  unit_price, total_amount) is the authoritative data contract.
- Any change to the data source MUST be treated as a breaking change requiring
  a constitution amendment.

**Rationale**: A static, predictable data source eliminates an entire class of
runtime failures and makes the dashboard fully offline-capable and auditable.

### III. Visual Verification (NON-NEGOTIABLE)

There are no automated test suites. Correctness is verified manually by running
the dashboard locally and spot-checking KPI values against known data totals.

- Every code change MUST be verified by launching the app (`streamlit run`)
  before committing.
- KPI values MUST be cross-checked against known dataset totals
  (~$650K–$700K total revenue, 482 total orders) as a sanity check.
- Docker image builds MUST be verified by running the container and loading
  the dashboard before tagging for deployment.

**Rationale**: For a single-developer, demo-context dashboard, the overhead of
a formal test suite exceeds its benefit. Visual spot-checking provides
sufficient confidence given the static, bounded dataset.

### IV. Container-First Deployment

The dashboard MUST be deployable as a self-contained Docker image.

- All Python dependencies MUST be declared in a `requirements.txt` (or
  `pyproject.toml` managed by `uv`); no host-installed packages may be assumed.
- The container MUST expose port 8501 and run identically on macOS, Linux,
  and Windows hosts.
- The `data/sales-data.csv` file MUST be bundled inside the image at build
  time; volume mounts are permitted for local development only.

**Rationale**: Containerization eliminates "works on my machine" failures and
provides a consistent, shareable artifact for stakeholder demos on any platform.

### V. Ship Minimal, Iterate on Signal

The initial release MUST contain only the highest-value views: KPI scorecards,
sales trend line chart, sales by category, and sales by region.

- New visualizations or filters are added ONLY after stakeholder feedback
  confirms demand.
- Speculative features (e.g., export buttons, drill-down modals, date range
  pickers) are explicitly prohibited until requested.
- Each addition MUST be traceable to a Jira issue capturing the stakeholder
  request.

**Rationale**: Premature feature additions increase maintenance burden and
dilute visual clarity for the executive audience. Signal-driven iteration
keeps the dashboard focused and the codebase lean.

## Tech Stack & Data Contract

The following stack is fixed for this project. Deviations require a
constitution amendment.

| Concern | Choice |
|---------|--------|
| Language | Python 3.11+ |
| Dashboard framework | Streamlit |
| Charting | Plotly Express |
| Data manipulation | pandas |
| Dependency management | `uv` |
| Containerization | Docker |
| Data source | `data/sales-data.csv` (bundled) |
| Source control | Git + GitHub |

**Known dataset characteristics** (used as verification baselines):
- Total Revenue: ~$650K–$700K
- Total Orders: 482
- Categories: Electronics, Accessories, Audio, Wearables, Smart Home
- Regions: North, South, East, West

## Development Workflow

All changes MUST follow this sequence before being committed:

1. Implement change locally.
2. Run `streamlit run app.py` and visually verify the affected views.
3. Spot-check KPI values against known dataset baselines (Principle III).
4. Build and run the Docker image to verify container parity (Principle IV).
5. Commit with the Jira issue key in the message (e.g., `ECOM-1: Add KPI cards`).
6. Push to GitHub fork.
7. Deploy updated image (Streamlit Community Cloud or Docker host).

AI-generated code MUST be reviewed against all five principles before step 5.
Any complexity violation MUST be documented in the feature's `plan.md`
Complexity Tracking table before merging.

## Governance

This constitution supersedes all other practices and conventions in this
repository. When a conflict arises between this document and any other
guideline, this constitution takes precedence.

**Amendment procedure**:
1. Identify the principle or section requiring change.
2. Draft the amendment with explicit rationale.
3. Increment `CONSTITUTION_VERSION` per semantic versioning:
   - MAJOR: Removal or redefinition of an existing principle.
   - MINOR: New principle or section added.
   - PATCH: Clarification, wording fix, or non-semantic refinement.
4. Update `LAST_AMENDED_DATE` to the amendment date.
5. Re-run the consistency propagation checklist against all templates.
6. Commit with message: `docs: amend constitution to vX.Y.Z (<summary>)`.

**Compliance review**: Every feature plan (`plan.md`) MUST include a
Constitution Check gate that verifies adherence to all five principles before
implementation begins. Any violation MUST be explicitly justified in the
Complexity Tracking table of that plan.

**Version**: 1.0.0 | **Ratified**: 2026-03-10 | **Last Amended**: 2026-03-10
