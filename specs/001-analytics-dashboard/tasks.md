---
description: "Task list for Sales Performance Dashboard"
---

# Tasks: Sales Performance Dashboard

**Input**: specs/001-analytics-dashboard/spec.md
**Prerequisites**: spec.md ✅ | plan.md ⚠ (skipped — tech stack inferred from constitution)
**Tests**: None (visual verification per constitution Principle III)
**Granularity**: Fine-grained for P1 (MVP), medium for P2 and P3

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3)
- Exact file paths included in all descriptions

## Path Conventions

Single-file structure: `app.py` at repository root + `data/sales-data.csv` (pre-existing)

---

## Phase 1: Setup

**Purpose**: Project initialization — dependency declaration and Docker scaffolding

- [x] T001 Create `pyproject.toml` at repo root declaring dependencies: streamlit, plotly, pandas (Python 3.11+, managed via uv)
- [x] T002 [P] Create `Dockerfile` at repo root: Python 3.11 slim base image, install uv, copy `pyproject.toml` + `data/` + `app.py`, expose port 8501, set entrypoint to `streamlit run app.py --server.port=8501 --server.address=0.0.0.0`
- [x] T003 [P] Create `app.py` at repo root with imports (streamlit, plotly.express, pandas) and a bare `st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")` call

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Data loading pipeline — MUST complete before any user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Implement `load_data()` function in `app.py` that reads `data/sales-data.csv` with pandas, parses the `date` column as datetime, decorates with `@st.cache_data`, and returns a DataFrame
- [x] T005 Add null/empty data guard in `app.py`: after `load_data()` call, if DataFrame is empty display `st.error("No sales data found. Please check that data/sales-data.csv is present and contains records.")` and `st.stop()`
- [x] T006 Add file-not-found error handler in `app.py`: wrap `load_data()` call in try/except, catch `FileNotFoundError` and display `st.error("Sales data file not found at data/sales-data.csv.")` and `st.stop()` — no raw traceback exposed (FR-010)
- [x] T007 Add null `total_amount` filtering in `load_data()` in `app.py`: drop rows where `total_amount` is null before returning DataFrame; display `st.info(f"{n} rows excluded due to missing amount values.")` if any rows are dropped

**Checkpoint**: Run `streamlit run app.py` — app launches, loads CSV, shows no errors with valid data. Ready for user story implementation.

---

## Phase 3: User Story 1 — Instant KPI Snapshot (Priority: P1) 🎯 MVP

**Goal**: Two KPI cards visible above the fold — Total Sales (currency) and Total Orders (count)

**Independent Test**: Open dashboard. "Total Sales" shows ~$650K–$700K and "Total Orders" shows 482. No scrolling or clicking required.

### Implementation for User Story 1

- [ ] T008 [US1] Add `st.title("Sales Performance Dashboard")` as the first visible element in `app.py` (FR-001)
- [ ] T009 [US1] Compute `total_sales = df["total_amount"].sum()` and `total_orders = len(df)` in `app.py`
- [ ] T010 [US1] Create two-column layout with `col1, col2 = st.columns(2)` in `app.py` for KPI cards
- [ ] T011 [US1] Render "Total Sales" metric in `col1` in `app.py` using `st.metric(label="Total Sales", value=f"${total_sales:,.0f}")` (FR-002)
- [ ] T012 [US1] Render "Total Orders" metric in `col2` in `app.py` using `st.metric(label="Total Orders", value=f"{total_orders:,}")` (FR-003)

**Checkpoint**: KPI cards visible, values match expected baselines. US1 is fully functional — deployable as a minimal dashboard.

---

## Phase 4: User Story 2 — Sales Trend Over Time (Priority: P2)

**Goal**: Monthly line chart below KPIs showing revenue over 12 months with hover tooltips

**Independent Test**: A "Sales Trend Over Time" line chart appears with 12 monthly x-axis labels and interactive tooltips on hover.

### Implementation for User Story 2

- [ ] T013 [US2] Compute monthly revenue in `app.py`: `df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()` then `monthly = df.groupby("month")["total_amount"].sum().reset_index()`
- [ ] T014 [US2] Render "Sales Trend Over Time" line chart in `app.py` using `px.line(monthly, x="month", y="total_amount", title="Sales Trend Over Time", labels={"month": "Month", "total_amount": "Revenue ($)"})` and `st.plotly_chart(fig, use_container_width=True)` (FR-004)

**Checkpoint**: Line chart renders with 12 data points and hover tooltips. US1 + US2 both functional independently.

---

## Phase 5: User Story 3 — Category & Region Breakdowns (Priority: P3)

**Goal**: Two bar charts side by side at the bottom — Sales by Category (5 bars) and Sales by Region (4 bars), both sorted descending

**Independent Test**: Two bar charts visible side by side. Category chart has 5 bars (Electronics, Accessories, Audio, Wearables, Smart Home), region chart has 4 bars (North, South, East, West). Both sorted highest to lowest.

### Implementation for User Story 3

- [ ] T015 [P] [US3] Compute category revenue in `app.py`: `cat = df.groupby("category")["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)`
- [ ] T016 [P] [US3] Compute region revenue in `app.py`: `reg = df.groupby("region")["total_amount"].sum().reset_index().sort_values("total_amount", ascending=False)`
- [ ] T017 [US3] Create two-column layout in `app.py` with `col_cat, col_reg = st.columns(2)` for the bar charts (FR-007)
- [ ] T018 [US3] Render "Sales by Category" bar chart in `col_cat` in `app.py` using `px.bar(cat, x="category", y="total_amount", title="Sales by Category", labels={"category": "Category", "total_amount": "Revenue ($)"})` sorted by value (FR-005)
- [ ] T019 [US3] Render "Sales by Region" bar chart in `col_reg` in `app.py` using `px.bar(reg, x="region", y="total_amount", title="Sales by Region", labels={"region": "Region", "total_amount": "Revenue ($)"})` sorted by value (FR-006)

**Checkpoint**: Both bar charts visible side by side, sorted correctly, with hover tooltips. All three user stories functional.

---

## Phase 6: Polish & Deployment

**Purpose**: Docker verification and full visual sign-off

- [ ] T020 Build Docker image: `docker build -t sales-dashboard .` and verify build completes without errors
- [ ] T021 Run Docker container: `docker run -p 8501:8501 sales-dashboard` and open `http://localhost:8501` — verify all four views render correctly inside the container
- [ ] T022 [P] Visual sign-off checklist in `app.py`: confirm page title, KPI values (~$650K–$700K / 482), 12-point trend line, 5-bar category chart, 4-bar region chart, side-by-side layout, interactive tooltips on all charts (SC-001 through SC-007)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately; T002 and T003 can run in parallel
- **Foundational (Phase 2)**: Depends on T003 (app.py skeleton) — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational completion — no dependency on US2 or US3
- **US2 (Phase 4)**: Depends on Foundational completion — no dependency on US1 or US3
- **US3 (Phase 5)**: Depends on Foundational completion — T015 and T016 can run in parallel
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### Within Each User Story

- US1: T008 → T009 → T010 → T011 → T012 (sequential, all in app.py)
- US2: T013 → T014 (sequential)
- US3: T015 [P] + T016 [P] → T017 → T018 → T019 (parallel aggregations, then layout)

### Parallel Opportunities

- T002 and T003 (Dockerfile + app.py skeleton) can run in parallel during Setup
- T015 and T016 (category + region aggregations) can run in parallel within US3

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001–T003)
2. Complete Phase 2: Foundational (T004–T007) — CRITICAL
3. Complete Phase 3: US1 KPI Snapshot (T008–T012)
4. **STOP and VALIDATE**: Two KPI cards visible, values correct
5. Ship/demo if sufficient

### Incremental Delivery

1. Setup + Foundational → data pipeline ready
2. Add US1 → KPI snapshot → validate → demo (MVP!)
3. Add US2 → trend chart → validate → demo
4. Add US3 → category + region charts → validate → demo
5. Polish + Docker → production-ready

---

## Notes

- [P] tasks = different concerns, no file conflicts, safe to parallelize
- [Story] label maps each task to its user story for traceability
- All tasks target `app.py` (single-file architecture) — no intra-story file conflicts
- No test tasks generated (constitution Principle III: visual verification)
- Commit after each phase checkpoint with Jira issue key (e.g., `ECOM-1: Add KPI cards`)
