# 📊 TMDB Movie Revenue Prediction
## Phase 3 — Exploratory Data Analysis (EDA)

> **Part of a multi-phase machine learning project** that predicts movie box office revenue using data from The Movie Database (TMDB) API.

---

## 📌 Overview

With a clean dataset in hand, this phase dives deep into the data through **statistical analysis and rich visualizations** to uncover the patterns, distributions, correlations, and anomalies that drive movie revenue. Every chart produced here directly informed the feature engineering decisions made in the modelling phase.

The EDA was conducted in a Jupyter Notebook (`TMDB EDA phase.ipynb`) and productionized into a standalone Python script (`EDA_tmdb.py`) that exports all plots to a `plots/` directory.

---

## 🎯 Objectives

- Understand the shape and distribution of every key feature
- Identify which variables have the strongest relationship with revenue
- Detect skewness, outliers, and long-tail distributions
- Engineer and validate new features (movie age, genre encoding)
- Produce a visual "story" that supports modelling decisions

---

## 🗂️ Files

| File | Description |
|------|-------------|
| `Notebooks/TMDB EDA phase.ipynb` | Full interactive EDA notebook (2.2 MB) |
| `scripts/EDA_tmdb.py` | Productionized script — exports all plots |
| `data/cleaned_movies.csv` | Input dataset from Phase 2 |
| `data/encoded_movies.csv` | Output — genre-encoded dataset for modelling |
| `plots/` | Output directory for all generated visualizations |

---

## 🔧 Feature Engineering

Before any plotting, two new features were engineered from existing columns:

### 🗓️ Movie Age
```python
df['release_date'] = pd.to_datetime(df['release_date'])
df['release_year'] = df['release_date'].dt.year
df['release_month'] = df['release_date'].dt.month
```
`release_year` and `release_month` allow temporal trend analysis and serve as features in the model.

### 🎭 Genre Parsing
```python
df['genres'] = df['genres'].apply(ast.literal_eval)
```
The `genres` column is stored as a **string representation of a Python list** (e.g., `"['Action', 'Drama']"`). `ast.literal_eval` safely converts it to a real list, enabling genre-level analysis and later one-hot encoding via `MultiLabelBinarizer`.

---

## 📈 Visualizations & Insights

### 1. 🌍 Movie Language Distribution
**Chart:** Horizontal bar chart of movie count per `original_language`

> **Insight:** The dataset is overwhelmingly dominated by **English-language films**. Any conclusions drawn from this analysis primarily reflect the English-language movie market — an important caveat for model interpretation.

---

### 2. 💰 Budget & Revenue Distributions
**Chart:** Two histograms — one for `budget`, one for `revenue`

> **Insight:** Both follow a classic **"long tail"** distribution. The vast majority of films have modest budgets (under $50M) and modest returns. A tiny fraction of blockbusters skew the mean dramatically upward. This skewness is why **log-transformation** is applied during modelling.

---

### 3. 🔥 Popularity Distribution
**Chart:** Histogram with log scale on the x-axis

> **Insight:** Popularity is also long-tailed. The **median popularity score is 7.61**, but a small number of recently released or viral films have scores in the hundreds. Log scale is necessary to visualize this distribution meaningfully.

---

### 4. ⭐ Rating Distribution
**Chart:** Histogram of `vote_average` (0–10 scale)

> **Insight:** Ratings follow a **near-normal distribution**, slightly left-skewed. The **mean rating is 6.86 / 10**, suggesting audiences are generally positive but discriminating. There are very few movies rated below 4 or above 9 in this dataset.

---

### 5. ⏱️ Runtime Distribution
**Chart:** Histogram of `runtime` in minutes (filtered to 0–240 min for readability)

> **Insight:** The vast majority of films run between **90 and 120 minutes**. The **median runtime is 110 minutes**. Films outside the 80–150 minute window are rare, with extreme outliers filtered from the visualization.

---

### 6. 🎭 Genre Distribution
**Chart:** Bar chart of the top 10 genres by frequency

> **Insight:** **Drama**, **Comedy**, and **Thriller** are the three most frequently produced genres in the dataset. This reflects industry production patterns — these genres are considered commercially "safe" by studios.

---

### 7. 💵 Revenue by Genre
**Chart:** Box plot of `revenue` per genre (log scale)

> **Insight — Key Findings:**
> - **Highest earners:** Adventure, Animation, and Family films have the **highest median revenues**
> - **Most volatile:** Adventure and Science Fiction show the **widest revenue ranges** — they produce both blockbusters and flops
> - **Safest (lowest risk/reward):** Horror and Documentary films show the **lowest median revenues**

---

### 8. 📅 Revenue & Popularity vs. Movie Age
**Chart:** Two scatter plots — Revenue vs. Release Year, Popularity vs. Release Year

> **Insight:** Both revenue and popularity scores trend **higher for newer movies**. This is explained by:
> - Ticket price inflation increasing nominal revenue over time
> - TMDB's popularity metric being recency-biased (currently hyped films rank higher)

---

### 9. 💸 Budget vs. Revenue
**Chart:** Scatter plot with log scales on both axes

> **Insight:** There is a **strong positive correlation (r = 0.68)** — the most significant relationship in the dataset. The upward trend confirms the industry axiom: *"You have to spend money to make money."* However, the wide scatter around the trend line shows high-budget flops and low-budget hits are common.

---

### 10. 🔥 Popularity vs. Revenue
**Chart:** Scatter plot with log scales

> **Insight:** A clear **positive relationship** exists between popularity and revenue, but the point cloud is wide. Popularity is a useful signal but not a reliable standalone predictor of box office success.

---

### 11. ⏱️ Runtime vs. Rating
**Chart:** Scatter plot — `runtime` vs. `vote_average`

> **Insight:** A slight positive correlation **(r = 0.34)**. Longer films tend to have marginally higher ratings — likely because films that *earn* a long runtime (epics, prestige dramas) are typically higher-quality productions.

---

### 12. ⏱️ Runtime vs. Popularity
**Chart:** Scatter plot — `runtime` vs. `popularity`

> **Insight:** Almost no relationship **(r = 0.11)**. Runtime is not a meaningful predictor of popularity. Audiences enjoy both short and long films equally.

---

### 13. 🗺️ Correlation Heatmap
**Chart:** Annotated heatmap of all numeric feature correlations

> **Insight — Strongest Correlations with Revenue:**
>
> | Feature Pair | Correlation |
> |-------------|-------------|
> | Revenue & Budget | **0.68** — strongest link |
> | Revenue & Vote Count | **0.65** — commercially successful films attract more ratings |
> | Revenue & Popularity | ~0.5 — moderate link |
> | Revenue & Runtime | ~0.2 — weak link |
> | Revenue & Vote Average | ~0.2 — weak link |

---

### 14. 🧩 Pairplot (Dashboard View)
**Chart:** Grid of all numeric feature scatter plots and distributions

> **Insight:** A comprehensive "dashboard" confirming all key findings at a glance. The diagonal shows right-skewed distributions for budget/revenue/popularity, confirming the need for log transformation before modelling.

---

## 📋 Executive Summary — Key Takeaways

| # | Finding | Implication for Modelling |
|---|---------|--------------------------|
| 1 | **Budget is the strongest revenue predictor (r = 0.68)** | Include `budget` as a primary feature; apply log transformation |
| 2 | **Genre significantly affects revenue ceiling** | One-hot encode genres as model features |
| 3 | **Newer movies earn more and score higher popularity** | Include `release_year` as a temporal feature |
| 4 | **Revenue & budget are heavily right-skewed** | Apply `log1p` transformation before fitting any regression model |
| 5 | **Runtime has almost no effect on popularity** | Runtime is a low-priority feature; may be binned rather than used raw |
| 6 | **The market is a "long tail"** — most films are not blockbusters | Tree-based models (Random Forest, XGBoost) will outperform linear models |

---

## 🚀 How to Run

> ⚠️ You must complete **Phase 2 (Data Cleaning)** before running this script.

```bash
# From the project root
python scripts/EDA_tmdb.py
```

**Expected output:**
```
Successfully loaded data from data/cleaned_movies.csv (1312 rows)
Preprocessing data...
Generating genre plot -> plots/1_genre_counts.png
Generating revenue distribution -> plots/2_revenue_distribution.png
Generating budget vs. revenue scatter -> plots/3_budget_revenue_scatter.png
Generating correlation heatmap -> plots/4_correlation_heatmap.png
Generating revenue by year plot -> plots/5_revenue_by_year.png
Generating vote average distribution -> plots/6_vote_average_distribution.png
Generating runtime distribution -> plots/7_runtime_distribution.png

✅ All plots have been generated and saved to the 'plots' directory.
```

---

## 📁 Generated Plots

| File | Chart Type | Features |
|------|-----------|----------|
| `1_genre_counts.png` | Horizontal bar | Genre frequency |
| `2_revenue_distribution.png` | Histogram + KDE | Revenue |
| `3_budget_revenue_scatter.png` | Scatter | Budget vs. Revenue |
| `4_correlation_heatmap.png` | Annotated heatmap | All numeric features |
| `5_revenue_by_year.png` | Line chart | Total revenue per year |
| `6_vote_average_distribution.png` | Histogram + KDE | Vote average |
| `7_runtime_distribution.png` | Histogram + KDE | Runtime |

---

## 🔗 Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 — Data Collection | TMDB API ingestion pipeline | ✅ Complete |
| 2 — Data Cleaning | Merging, deduplication & filtering | ✅ Complete |
| **3 — EDA** | Visualizations & statistical insights | ✅ Complete |
| 4 — Modelling | ML model training & evaluation | ✅ Complete |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Seaborn](https://img.shields.io/badge/Seaborn-0.13-76B7B2?logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-3.x-11557C?logo=python&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?logo=numpy&logoColor=white)

| Library | Purpose |
|---------|---------|
| `pandas` | Data loading, manipulation, and grouping |
| `seaborn` | Statistical visualizations (histplots, boxplots, heatmaps, pairplots) |
| `matplotlib` | Figure creation, saving, and styling |
| `numpy` | Numerical operations |
| `ast` | Safe parsing of string-encoded genre lists |
| `sklearn.preprocessing.MultiLabelBinarizer` | One-hot encoding of multi-label genre data |

---

*← Previous: [Phase 2: Data Cleaning](./README_phase2_data_cleaning.md)*  
*Next → [Phase 4: Modelling](./README_phase4_modelling.md)*
