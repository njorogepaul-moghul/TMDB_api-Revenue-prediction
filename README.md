# 🎬 TMDB Movie Revenue Prediction
### End-to-End ML Pipeline | TMDB API · Feature Engineering · XGBoost | Films up to 2025

![Python](https://img.shields.io/badge/Python-3.11-blue)
![XGBoost](https://img.shields.io/badge/Champion-XGBoost-brightgreen)
![API](https://img.shields.io/badge/Data-TMDB_API-01B4E4)
![Movies](https://img.shields.io/badge/Dataset-4,000+_Movies-orange)

---

## 📌 Project Overview

This project builds an **end-to-end machine learning pipeline** to predict movie box office revenue using data fetched directly from **The Movie Database (TMDB) API**. The dataset covers films released up to 2025, including budget, popularity, genres, runtime, language, and audience ratings.

| Metric | Value |
|---|---|
| Movies Fetched | 4,000+ (200 pages × 20 movies) |
| Clean Modelling Dataset | ~2,300 movies |
| Features Used | 26 (after encoding) |
| Mean Dataset Revenue | $128.2 million |
| Champion Model R² | **0.5744** |
| Champion Model MAE | **$67,412,206** |

---

## 🎯 The Problem

Movie studios, investors, and distributors need to estimate a film's potential revenue **before** release. Traditional methods rely on gut feel and historical precedent. This project asks: **can machine learning predict box office performance from pre-release data alone?**

---

## 🏗️ Project Architecture

```
TMDB Revenue Prediction
│
├── Phase 1 — Data Collection
│   ├── 4,000 movies fetched via TMDB /movie/popular endpoint
│   ├── Full details fetched per movie via /movie/{id} endpoint
│   └── Two-stage merge → movies_full.csv
│
├── Phase 2 — Data Cleaning
│   ├── Duplicate removal, column standardisation
│   ├── Filtered: zero-budget and zero-revenue movies removed
│   └── Final clean dataset → cleaned_movies.csv
│
├── Phase 3 — EDA
│   ├── Revenue, budget, genre, runtime distribution analysis
│   ├── Correlation heatmap — budget:revenue = 0.68
│   └── Key insight: budget is strongest revenue predictor
│
└── Phase 4 — Modelling
    ├── 4 models compared: Linear Regression, Decision Tree, RF, XGBoost
    ├── Two-stage tuning: RandomizedSearchCV → GridSearchCV
    └── Champion: Tuned XGBoost — R² 0.5744, MAE $67.4M
```

---

## 📊 Final Model Performance

| Model Version | R² | MAE | RMSE |
|---|---|---|---|
| **Tuned XGBoost (Grid) ✅** | **0.5744** | **$67,412,206** | **$140,863,770** |
| Tuned XGBoost (Random) | 0.5505 | $68,520,713 | $144,760,660 |
| Default XGBoost | 0.5378 | $70,072,567 | $146,790,839 |
| Default Random Forest | 0.5212 | $68,464,761 | $149,403,008 |
| Tuned Random Forest (Grid) | 0.4887 | $70,059,528 | $154,394,718 |
| Default Decision Tree | 0.3805 | $78,862,572 | $169,942,852 |
| Linear Regression | -0.8118 | $98,878,627 | $290,627,437 |

> The champion model explains **57.4% of variance in movie revenue** and predicts within ~$67M on average against a mean revenue of $128M.

---

## 🔑 Key EDA Findings

| Finding | Correlation | Insight |
|---|---|---|
| Budget → Revenue | **0.68** | Strongest predictor — you have to spend to make |
| Vote Count → Revenue | **0.65** | Engagement and commercial success move together |
| Movie Age → Revenue | Negative | Newer films earn more — recency effect |
| Runtime → Vote Average | **0.34** | Longer films tend to earn higher ratings |
| Popularity → Revenue | **0.15** | Positive but weak — buzz alone doesn't guarantee success |

**Top Revenue Genres:** Adventure · Animation · Family consistently highest median revenue

**Genre Production Volume:** Drama · Comedy · Thriller most frequently produced

---

## 🛠️ Tech Stack

| Layer | Tools |
|---|---|
| Data Collection | Python · requests · TMDB API · python-dotenv · tqdm |
| Data Cleaning | Pandas · os |
| EDA | Matplotlib · Seaborn · ast |
| Modelling | Scikit-Learn · XGBoost · Joblib |
| Pipelines | sklearn Pipeline · ColumnTransformer |

---

## 📁 Repository Structure

```
├── fetch_tmdb.py                    # Phase 1: TMDB API data collection
├── cleaning_tmdb.py                 # Phase 2: Data cleaning pipeline
├── EDA_tmdb.py                      # Phase 3: EDA & visualisations
├── modelling_tmdb.py                # Phase 4: Modelling pipeline
│
├── TMDB_data_collection_phase.ipynb # Phase 1 notebook (interactive)
├── TMDB_EDA_phase.ipynb             # Phase 3 notebook (interactive)
├── TMDB_modelling_phase.ipynb       # Phase 4 notebook (interactive)
│
├── data/
│   ├── popular_movies.csv           # Raw 4,000 movie list
│   ├── movies_full.csv              # Merged raw + details dataset
│   ├── cleaned_movies.csv           # Cleaned modelling-ready dataset
│   └── encoded_movies.csv           # Final encoded feature matrix
│
├── models/
│   └── best_revenue_predictor.joblib  # Saved champion model
│
├── plots/                           # All generated EDA visualisations
├── requirements.txt
└── .env                             # TMDB API key (not committed)
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Add your TMDB API key to .env
echo "TMDB_API_KEY=your_key_here" > .env

# 3. Fetch data
python fetch_tmdb.py

# 4. Clean data
python cleaning_tmdb.py

# 5. Run EDA
python EDA_tmdb.py

# 6. Train models
python modelling_tmdb.py
```

---

## 🔭 Roadmap

- Add cast/director features via TMDB credits endpoint
- Integrate NLP on movie overview for sentiment-based revenue signal
- Build Streamlit app for interactive revenue prediction
- Expand dataset to 10,000+ movies for improved model generalisation

---

## 📬 Contact

**Paul Njoroge** | larneymogul@gmail.com | Kenyatta University, Kenya
