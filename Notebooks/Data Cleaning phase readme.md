# 🧹 TMDB Movie Revenue Prediction
## Phase 2 — Data Cleaning

> **Part of a multi-phase machine learning project** that predicts movie box office revenue using data from The Movie Database (TMDB) API.

---

## 📌 Overview

Raw data collected from the TMDB API is noisy, redundant, and full of entries that would corrupt any meaningful analysis. This phase takes the merged raw dataset (`movies_full.csv`) and applies a **structured, reproducible cleaning pipeline** to produce `cleaned_movies.csv` — a reliable, analysis-ready dataset.

The cleaning process reduced the dataset from ~4,000 raw rows to a **high-quality subset** of movies with full financial records, removing all zero-budget, zero-revenue, and incomplete entries.

---

## 🎯 Objectives

- Resolve column naming conflicts caused by the two-dataset merge
- Remove duplicate records
- Drop columns irrelevant to revenue prediction
- Eliminate rows with critical missing values
- Filter out financially meaningless entries (zero budget/revenue)
- Produce and persist a clean, analysis-ready CSV

---

## 🗂️ Files

| File | Description |
|------|-------------|
| `scripts/cleaning_tmdb.py` | Main data cleaning script |
| `Notebooks/TMDB data collection phase.ipynb` | Original cleaning notebook |
| `data/movies_full.csv` | Raw input — output from Phase 1 |
| `data/cleaned_movies.csv` | Clean output — input for Phase 3 (EDA) |

---

## 🔬 Cleaning Pipeline

The cleaning script (`cleaning_tmdb.py`) applies **6 sequential steps**, each traceable back to a decision made during notebook exploration:

---

### Step 1 — Resolve Column Name Conflicts

When the popular movies list and the full details dataset were merged in Phase 1 using a **left join on `id`**, Pandas automatically suffixed duplicate column names with `_x` (from the left DataFrame) and `_y` (from the right).

```
Before:  title_x, title_y, popularity_x, popularity_y, release_date_x ...
After:   title,   popularity,   release_date,   vote_average,   vote_count
```

The `_x` (summary-level) columns were **dropped** in favour of the `_y` (detail-level) values, which are richer and more authoritative.

```python
df.drop(columns=['popularity_x', 'release_date_x', 'title_x', 'vote_average_x', 'vote_count_x'])
df.rename(columns={'title_y': 'title', 'popularity_y': 'popularity', ...})
```

---

### Step 2 — Drop Duplicate Rows

```python
df.drop_duplicates(inplace=True)
```

Duplicate movies could appear when the same film appears on multiple "popular" pages over the 200-page fetch window. These duplicates were removed entirely.

---

### Step 3 — Drop Irrelevant Columns

Columns that carry no predictive signal for revenue modelling were removed:

| Column Dropped | Reason |
|----------------|--------|
| `backdrop_path` | Image URL — not a feature |
| `poster_path` | Image URL — not a feature |
| `adult` | Constant value (`False`) for all entries |
| `video` | Constant value (`False`) for all entries |
| `status` | All fetched movies had `Released` status |
| `original_title` | Covered by `title` |
| `id` | TMDB internal key — not a predictive feature |
| `genre_ids` | Replaced by the richer `genres` list from the detail endpoint |

```python
columns_to_drop = ['backdrop_path', 'poster_path', 'adult', 'video',
                   'status', 'original_title', 'id', 'genre_ids']
df.drop(columns=columns_to_drop, inplace=True, errors='ignore')
```

> `errors='ignore'` ensures the script is idempotent — safe to run multiple times without crashing.

---

### Step 4 — Drop Rows with Missing Critical Values

```python
df.dropna(subset=['release_date', 'overview'], inplace=True)
```

- **`release_date`** is required for temporal feature engineering (movie age) in the EDA and modelling phases.
- **`overview`** missing indicates an incomplete or placeholder record that is unlikely to have valid financial data.

---

### Step 5 — Filter Zero Budget & Revenue Rows

```python
df = df[(df['budget'] != 0) & (df['revenue'] != 0)]
```

The TMDB API returns `0` for budget and revenue when this data is **unknown or not publicly disclosed** — not when a movie was actually free to make or earned nothing. These zero-value rows are **not true zeros**; they are missing data disguised as numbers and would severely bias any regression model.

This is the **most impactful filtering step**, as most movies on TMDB do not have verified financial data.

---

### Step 6 — Save Cleaned Dataset

```python
df.to_csv("data/cleaned_movies.csv", index=False)
```

The cleaned DataFrame is persisted to `data/cleaned_movies.csv`, ready for exploratory analysis in Phase 3.

---

## 📊 Final Dataset Schema

The cleaned dataset contains the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `original_language` | `str` | Language the movie was produced in (e.g., `"en"`, `"fr"`) |
| `overview` | `str` | Short plot summary or description |
| `title` | `str` | Official movie title |
| `budget` | `int` | Production cost in USD |
| `revenue` | `int` | Total box office earnings in USD — **target variable** |
| `runtime` | `float` | Movie duration in minutes |
| `release_date` | `str` | Theatrical release date (`YYYY-MM-DD`) |
| `popularity` | `float` | TMDB's rolling popularity score |
| `vote_average` | `float` | Mean audience rating (0–10 scale) |
| `vote_count` | `int` | Total number of user ratings |
| `genres` | `str` | List of genre labels stored as a string (e.g., `"['Action', 'Drama']"`) |

---

## 📉 Data Reduction Summary

| Stage | Row Count |
|-------|-----------|
| Raw merged dataset (`movies_full.csv`) | ~4,000 |
| After dropping duplicates | ~3,950 |
| After dropping missing `release_date` / `overview` | ~3,800 |
| After filtering zero `budget` / `revenue` | **~1,200–1,500** |

> The sharp reduction from zero-filter is expected and **intentional** — only movies with verified financial records are modelled.

---

## 🚀 How to Run

> ⚠️ You must complete **Phase 1 (Data Collection)** before running this script.

```bash
# From the project root
python scripts/cleaning_tmdb.py
```

**Expected output:**
```
Loading data from data/movies_full.csv...
Initial shape: (4000, 24)
Cleaning column names...
Dropped 42 duplicate rows.
Dropping unnecessary columns...
Dropping rows with missing values...
Filtering out movies with zero budget or revenue...

✅ Successfully cleaned data and saved 1312 rows to data/cleaned_movies.csv
```

---

## 💡 Design Decisions

| Decision | Rationale |
|----------|-----------|
| Prefer `_y` columns over `_x` | Detail endpoint values are more authoritative than summary-level data |
| Filter zeros, not `NaN` | TMDB encodes missing financial data as `0`, not `null` |
| Use `errors='ignore'` on drop | Makes the script idempotent and safe to run on partially cleaned data |
| `os.makedirs(..., exist_ok=True)` | Ensures the output directory is created if it doesn't exist |

---

## 🔗 Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 — Data Collection | TMDB API ingestion pipeline | ✅ Complete |
| **2 — Data Cleaning** | Merging, deduplication & filtering | ✅ Complete |
| 3 — EDA | Visualizations & statistical insights | ✅ Complete |
| 4 — Modelling | ML model training & evaluation | ✅ Complete |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)

| Library | Purpose |
|---------|---------|
| `pandas` | DataFrame manipulation, deduplication, filtering, and CSV I/O |
| `os` | Directory creation for output paths |

---

*← Previous: [Phase 1: Data Collection](./README_phase1_data_collection.md)*  
*Next → [Phase 3: Exploratory Data Analysis](./README_phase3_eda.md)*
