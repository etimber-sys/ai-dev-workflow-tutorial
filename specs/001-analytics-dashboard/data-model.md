# Data Model: Sales Performance Dashboard

**Branch**: `001-analytics-dashboard` | **Date**: 2026-03-10

---

## Source Entity: Transaction

The atomic unit of data. One row in `data/sales-data.csv` represents one sales
transaction.

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| `date` | datetime | Transaction date | Parse as datetime; reject unparseable rows |
| `order_id` | string | Unique order identifier | Informational only; not used in aggregations |
| `product` | string | Product name | Informational only; not used in aggregations |
| `category` | string | Product category | One of: Electronics, Accessories, Audio, Wearables, Smart Home (display unknown values as-is) |
| `region` | string | Geographic region | One of: North, South, East, West (display unknown values as-is) |
| `quantity` | integer | Units sold | Informational only for Phase 1 |
| `unit_price` | float | Price per unit | Informational only for Phase 1 |
| `total_amount` | float | Total transaction value | **Primary metric**; rows with null value MUST be excluded |

**Loading rules**:
- Read via pandas `read_csv()` with `parse_dates=["date"]`
- Drop rows where `total_amount` is null before any aggregation
- Surface exclusion count to user if any rows dropped
- Raise `FileNotFoundError` if file missing; catch and display user-friendly message

**Expected volume**: ~1,000 rows, 12 months of data, ~50KB file size

---

## Derived Entity: KPI Summary

Computed once from the full Transaction dataset. Used to populate KPI cards.

| Field | Derived From | Formula |
|-------|-------------|---------|
| `total_sales` | `total_amount` | `df["total_amount"].sum()` |
| `total_orders` | row count | `len(df)` |

**Display formatting**:
- `total_sales` → `$672,340` (currency, no decimal, comma separator)
- `total_orders` → `482` (integer, comma separator for large values)

---

## Derived Entity: Monthly Revenue Summary

Aggregated from Transactions. Drives the Sales Trend line chart.

| Field | Type | Description |
|-------|------|-------------|
| `month` | datetime (month start) | Calendar month (truncated to first of month) |
| `total_amount` | float | Sum of all transaction amounts in that month |

**Derivation**:
```
df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
monthly = df.groupby("month")["total_amount"].sum().reset_index()
```

**Expected shape**: 12 rows × 2 columns (one per calendar month in dataset)
**Sort order**: Ascending by `month` (chronological for line chart x-axis)

---

## Derived Entity: Category Revenue Summary

Aggregated from Transactions. Drives the "Sales by Category" bar chart.

| Field | Type | Description |
|-------|------|-------------|
| `category` | string | Product category name |
| `total_amount` | float | Sum of all transaction amounts for that category |

**Derivation**:
```
cat = df.groupby("category")["total_amount"].sum().reset_index()
         .sort_values("total_amount", ascending=False)
```

**Expected shape**: 5 rows × 2 columns
**Sort order**: Descending by `total_amount` (highest-revenue category first)

---

## Derived Entity: Region Revenue Summary

Aggregated from Transactions. Drives the "Sales by Region" bar chart.

| Field | Type | Description |
|-------|------|-------------|
| `region` | string | Geographic region name |
| `total_amount` | float | Sum of all transaction amounts for that region |

**Derivation**:
```
reg = df.groupby("region")["total_amount"].sum().reset_index()
        .sort_values("total_amount", ascending=False)
```

**Expected shape**: 4 rows × 2 columns
**Sort order**: Descending by `total_amount` (highest-revenue region first)

---

## Entity Relationships

```
Transaction (raw CSV rows)
    │
    ├──► KPI Summary          (sum + count of all rows)
    ├──► Monthly Revenue       (grouped by month)
    ├──► Category Revenue      (grouped by category)
    └──► Region Revenue        (grouped by region)
```

All derived entities are computed from the same in-memory DataFrame loaded once
at startup. There are no joins, foreign keys, or persistent storage beyond the
source CSV.
