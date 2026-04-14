# 🎬 TMDB Movie Revenue Prediction
### An End-to-End Machine Learning Project

![Status](https://img.shields.io/badge/Status-Complete-brightgreen)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-Champion_Model-FF6600)
![TMDB](https://img.shields.io/badge/TMDB-API-01B4E4?logo=themoviedatabase&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 Project Overview

Can data predict a movie's box office success?

This project answers that question by building a **full, production-style machine learning pipeline** — from raw API data collection all the way through to a tuned, persisted predictive model. Using the **TMDB (The Movie Database) API**, data was gathered for over 4,000 films, cleaned, explored, and fed into four regression algorithms to identify the best predictor of movie revenue.

The final champion — a **Tuned XGBoost Regressor** — explains **~57.4% of revenue variance** with an average prediction error of **$67.4 million**, a strong result given the inherent unpredictability of box office performance.

---

## 🏆 Final Results at a Glance

> Dataset mean revenue: **$128,210,875**

| Model | R² Score | MAE | RMSE |
|-------|----------|-----|------|
| 🥇 **Tuned XGBoost (GridSearchCV)** | **0.5744** | **$67,412,206** | **$140,863,770** |
| Tuned XGBoost (RandomizedSearchCV) | 0.5505 | $68,520,713 | $144,760,660 |
| Default XGBoost | 0.5378 | $70,072,567 | $146,790,839 |
| Default Random Forest | 0.5212 | $68,464,761 | $149,403,008 |
| Tuned Random Forest (Grid) | 0.4887 | $70,059,528 | $154,394,718 |
| Default Decision Tree | 0.3805 | $78,862,572 | $169,942,852 |
| Default Linear Regression | -0.8118 | $98,878,627 | $290,627,437 |

---

## 📂 Project Structure

```
TMDB project/
│
├── 📓 Notebooks/
│   ├── TMDB data collection phase.ipynb   # Interactive data fetching notebook
│   ├── TMDB EDA phase.ipynb               # Full exploratory analysis (2.2 MB)
│   ├── TMDB modelling phase.ipynb         # Model training, tuning & evaluation
│   └── TMDB pipeline.ipynb                # Pipeline assembly notebook
│
├── 📊 data/
│   ├── popular_movies.csv                 # Raw: ~4,000 movies from TMDB popular endpoint
│   ├── movies_full.csv                    # Raw: merged with full movie details
│   ├── cleaned_movies.csv                 # Cleaned: deduplicated, filtered, typed
│   └── encoded_movies.csv                 # Final: genre-encoded, ready for modelling
│
├── 🐍 scripts/
│   ├── fetch_tmdb.py                      # Phase 1 — API data collection
│   ├── cleaning_tmdb.py                   # Phase 2 — Data cleaning pipeline
│   ├── EDA_tmdb.py                        # Phase 3 — EDA & visualization export
│   └── modelling_tmdb.py                  # Phase 4 — Model training & selection
│
├── 📄 README.md                           # ← You are here (Master overview)
├── README_phase1_data_collection.md       # Phase 1 deep-dive
├── README_phase2_data_cleaning.md         # Phase 2 deep-dive
├── README_phase3_eda.md                   # Phase 3 deep-dive
├── README_phase4_modelling.md             # Phase 4 deep-dive
│
├── .env                                   # TMDB API key (not committed)
├── .gitignore                             # Excludes .env, data, models, plots
└── requirements.txt                       # All Python dependencies
```

---

## 🗺️ Project Pipeline

```
┌─────────────────────┐
│   TMDB REST API      │
│  /movie/popular      │
│  /movie/{id}         │
└────────┬────────────┘
         │  ~4,000 movies fetched
         ▼
┌─────────────────────┐
│  Phase 1            │
│  Data Collection    │  fetch_tmdb.py
│  popular_movies.csv │
│  movies_full.csv    │
└────────┬────────────┘
         │  raw merged dataset
         ▼
┌─────────────────────┐
│  Phase 2            │
│  Data Cleaning      │  cleaning_tmdb.py
│  cleaned_movies.csv │  ~1,300 quality rows
└────────┬────────────┘
         │  clean dataset
         ▼
┌─────────────────────┐
│  Phase 3            │
│  EDA & Analysis     │  EDA_tmdb.py
│  encoded_movies.csv │  14 visualizations
│  plots/             │
└────────┬────────────┘
         │  feature insights
         ▼
┌─────────────────────┐
│  Phase 4            │
│  Modelling          │  modelling_tmdb.py
│  4 models trained   │
│  2 models tuned     │
│  best_model.joblib  │
└─────────────────────┘
```

---

## 🔬 Phase Summaries

### [Phase 1 — Data Collection](./README_phase1_data_collection.md)

Data was acquired directly from the **TMDB REST API** using a two-stage pipeline:

1. **Popular Movie List** — 200 pages × 20 movies = ~4,000 entries via `/movie/popular`
2. **Full Movie Details** — individual API calls per movie via `/movie/{id}` for budget, revenue, runtime, and genres

Key engineering decisions: Bearer token auth, `time.sleep(0.25)` rate limiting, graceful error handling, and environment variable management via `.env`.

📄 [Read the full Phase 1 README →](./README_phase1_data_collection.md)

---

### [Phase 2 — Data Cleaning](./README_phase2_data_cleaning.md)

A 6-step cleaning pipeline reduced ~4,000 raw rows to ~1,300 high-quality records:

| Step | Action |
|------|--------|
| 1 | Resolved `_x`/`_y` column conflicts from the merge |
| 2 | Removed duplicate rows |
| 3 | Dropped 8 irrelevant columns (image paths, constant-value flags) |
| 4 | Dropped rows missing `release_date` or `overview` |
| 5 | **Filtered zero `budget` and `revenue` rows** — TMDB uses `0` for unknown financials |
| 6 | Saved clean dataset to `data/cleaned_movies.csv` |

📄 [Read the full Phase 2 README →](./README_phase2_data_cleaning.md)

---

### [Phase 3 — Exploratory Data Analysis](./README_phase3_eda.md)

14 visualizations were produced to understand the data and guide modelling decisions:

| Key Finding | Modelling Implication |
|-------------|----------------------|
| Budget is the strongest revenue predictor (r = 0.68) | Primary feature; apply log transform |
| Revenue & budget are heavily right-skewed | Apply `log1p` before regression |
| Genre significantly affects revenue ceiling | One-hot encode genres |
| Newer films earn more (ticket inflation + recency bias) | Include `release_year` as a feature |
| Runtime has almost no effect on popularity | Low-priority feature; bin rather than use raw |
| Long-tail distribution — most films aren't blockbusters | Tree-based models will outperform linear ones |

📄 [Read the full Phase 3 README →](./README_phase3_eda.md)

---

### [Phase 4 — Modelling](./README_phase4_modelling.md)

A structured ML pipeline was built using `scikit-learn`:

- **Preprocessing:** `StandardScaler` for numerics, `OneHotEncoder` for `original_language`, `log1p` on budget & revenue, runtime binning
- **Models trained:** Linear Regression, Decision Tree, Random Forest, XGBoost
- **Tuning:** `RandomizedSearchCV` + `GridSearchCV` on top performers
- **Champion:** Tuned XGBoost — `R² = 0.5744`, `MAE = $67.4M`, `RMSE = $140.9M`

📄 [Read the full Phase 4 README →](./README_phase4_modelling.md)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- A free TMDB API key → [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tmdb-revenue-prediction.git
cd tmdb-revenue-prediction
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure your API key

```bash
# Create a .env file in the project root
echo "TMDB_API_KEY=your_api_key_here" > .env
```

### 4. Run the full pipeline

```bash
# Phase 1 — Collect data (~30–45 min due to rate limiting)
python scripts/fetch_tmdb.py

# Phase 2 — Clean the data
python scripts/cleaning_tmdb.py

# Phase 3 — Run EDA and export plots
python scripts/EDA_tmdb.py

# Phase 4 — Train, evaluate, and save the best model
python scripts/modelling_tmdb.py
```

> Or explore each phase interactively in the `Notebooks/` directory.

---

## 💡 Key Takeaways

1. **Budget dominates** — The strongest single predictor of revenue is production budget (r = 0.68). It's not a guarantee, but it's the closest thing to one in the data.

2. **Genre matters more than runtime** — Adventure, Animation, and Family films are high-ceiling genres. Runtime has almost no effect on popularity or revenue.

3. **Linear models fail here** — Revenue relationships are deeply non-linear. Linear Regression produced a **negative R²**, making it worse than predicting the mean. Ensemble methods are essential.

4. **Tuning isn't always better** — GridSearchCV improved XGBoost significantly, but *hurt* Random Forest (overfitting). Always validate tuned models on held-out test data.

5. **Box office is genuinely hard to predict** — Even the champion model has a ~52.6% average error relative to mean revenue. This reflects real-world volatility, not a modelling failure.

---

## 🛠️ Tech Stack

| Category | Tools |
|----------|-------|
| **Language** | Python 3.10+ |
| **Data Collection** | `requests`, `python-dotenv`, `tqdm` |
| **Data Manipulation** | `pandas`, `numpy` |
| **Visualization** | `seaborn`, `matplotlib` |
| **Machine Learning** | `scikit-learn`, `xgboost` |
| **Model Persistence** | `joblib` |
| **Notebooks** | `jupyter` |

---

## 📚 Phase Documentation

| README | Phase | Focus |
|--------|-------|-------|
| [README_phase1_data_collection.md](./README_phase1_data_collection.md) | Phase 1 | API pipeline, authentication, rate limiting |
| [README_phase2_data_cleaning.md](./README_phase2_data_cleaning.md) | Phase 2 | 6-step cleaning pipeline, schema documentation |
| [README_phase3_eda.md](./README_phase3_eda.md) | Phase 3 | 14 visualizations, EDA insights, feature selection |
| [README_phase4_modelling.md](./README_phase4_modelling.md) | Phase 4 | Model training, tuning, evaluation, champion selection |

---

## 🔮 Future Work

- [ ] **Add NLP features** — Sentiment analysis on movie `overview` text using TF-IDF or BERT embeddings
- [ ] **Incorporate cast & crew data** — Director track record and star power as features
- [ ] **Deploy as a web API** — Wrap the saved model in a FastAPI or Flask endpoint
- [ ] **Build a Streamlit dashboard** — Interactive UI for revenue predictions by movie parameters
- [ ] **Retrain on a larger dataset** — TMDB contains hundreds of thousands of titles; financial data availability is the limiting factor

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgements

- [The Movie Database (TMDB)](https://www.themoviedb.org/) for their free and well-documented API
- [scikit-learn](https://scikit-learn.org/) for the machine learning framework
- [XGBoost](https://xgboost.readthedocs.io/) for the gradient boosting implementation

---

*Built with 🎬 data, ☕ coffee, and a genuine curiosity about what makes movies succeed.*
