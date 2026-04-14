# 🤖 TMDB Movie Revenue Prediction
## Phase 4 — Modelling

> **Part of a multi-phase machine learning project** that predicts movie box office revenue using data from The Movie Database (TMDB) API.

---

## 📌 Overview

This phase takes the encoded, analysis-ready dataset from the EDA phase and puts it through a **full machine learning pipeline** — from feature engineering and preprocessing through multi-model training, evaluation, hyperparameter tuning, and final model selection.

Four regression algorithms were benchmarked. After tuning, the **XGBoost Regressor** emerged as the definitive champion, explaining **~57.4% of revenue variance** with a mean error of **$67.4 million** on a dataset where the mean revenue is $128.2 million.

---

## 🎯 Objectives

- Apply log transformations to correct skewed distributions before modelling
- Build a reusable `scikit-learn` preprocessing pipeline
- Train and benchmark four regression models under identical conditions
- Evaluate all models on the original dollar scale for business interpretability
- Tune the top performers using `GridSearchCV` and `RandomizedSearchCV`
- Select and persist the best model for production use

---

## 🗂️ Files

| File | Description |
|------|-------------|
| `Notebooks/TMDB modelling phase.ipynb` | Full interactive modelling notebook |
| `scripts/modelling_tmdb.py` | Productionized training & evaluation script |
| `data/encoded_movies.csv` | Input — genre-encoded dataset from Phase 3 |
| `models/best_revenue_predictor.joblib` | Output — saved champion model |
| `plots/best_model_evaluation.png` | Actual vs. Predicted scatter plot for the best model |

---

## ⚙️ Methodology

The modelling workflow follows a structured, reproducible approach:

---

### Step 1 — Feature Engineering

Before any model sees the data, three transformations were applied:

#### 🔢 Log Transformation
```python
import numpy as np
df['log_revenue'] = np.log1p(df['revenue'])   # Target variable
df['log_budget']  = np.log1p(df['budget'])    # Feature
```
Both `revenue` and `budget` are heavily right-skewed (long tail). Log-transforming compresses the scale, makes the distribution more normal, and dramatically improves linear and tree-based model performance.

> Predictions are later reversed with `np.expm1()` to evaluate on the original dollar scale.

#### 🔢 Ratio Feature
```python
df['budget_popularity_ratio'] = df['budget'] / (df['popularity'] + 1)
```
A composite interaction feature capturing the relationship between a film's financial investment and its current audience buzz.

#### 🗂️ Runtime Binning
```python
# Bins: Short (<80 min), Medium (80–110), Long (110–150), Very Long (>150)
```
Continuous `runtime` was discretized into four ordered categories and one-hot encoded — converting a noisy continuous variable into a cleaner categorical signal.

---

### Step 2 — Preprocessing Pipeline

A `scikit-learn` `ColumnTransformer` was built to handle mixed feature types cleanly:

```python
numerical_features   = ['budget', 'vote_count', 'popularity', 'runtime']
categorical_features = ['original_language']

numeric_transformer  = Pipeline([('scaler', StandardScaler())])
categorical_transformer = Pipeline([('onehot', OneHotEncoder(handle_unknown='ignore'))])

preprocessor = ColumnTransformer([
    ('num', numeric_transformer, numerical_features),
    ('cat', categorical_transformer, categorical_features)
])
```

Wrapping preprocessing in a `Pipeline` ensures:
- No data leakage between train and test sets
- A single, portable object that can be saved and reloaded for inference

---

### Step 3 — Train / Test Split

```python
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
```

- **80% training / 20% test** split
- `random_state=42` for full reproducibility

---

### Step 4 — Model Training

Four regression models were trained inside identical `Pipeline` wrappers:

| # | Model | Type |
|---|-------|------|
| 1 | **Linear Regression** | Baseline — assumes linear relationships |
| 2 | **Decision Tree Regressor** | Non-linear, interpretable |
| 3 | **Random Forest Regressor** | Ensemble of 100 decision trees |
| 4 | **XGBoost Regressor** | Gradient-boosted ensemble |

---

### Step 5 — Evaluation Metrics

All models were evaluated using three metrics, **computed on the original dollar scale** (after reversing the log transformation):

| Metric | Formula | What it measures |
|--------|---------|-----------------|
| **R²** (coefficient of determination) | `1 - SS_res/SS_tot` | How much revenue variance the model explains (higher = better) |
| **MAE** (Mean Absolute Error) | `mean(\|y - ŷ\|)` | Average prediction error in dollars (lower = better) |
| **RMSE** (Root Mean Squared Error) | `√mean((y - ŷ)²)` | Penalises large errors more heavily (lower = better) |

---

## 📊 Results

### Baseline Model Comparison (Default Hyperparameters)

> Dataset mean revenue: **$128,210,875**

| Model | R² Score | MAE | RMSE |
|-------|----------|-----|------|
| **XGBoost Regressor** | **0.5378** | $70,072,567 | **$146,790,839** |
| **Random Forest** | 0.5212 | **$68,464,761** | $149,403,008 |
| **Decision Tree** | 0.3805 | $78,862,572 | $169,942,852 |
| **Linear Regression** | -0.8118 | $98,878,627 | $290,627,437 |

#### Analysis
- **Linear Regression** failed entirely — a negative R² means it performs worse than predicting the mean. Revenue relationships are fundamentally non-linear.
- **Decision Tree** improved significantly but was clearly outperformed by the ensemble methods.
- **Random Forest** achieved the best raw MAE — predictions were, on average, closest to actual revenue.
- **XGBoost** led on R² and RMSE, making it the top overall baseline performer.

---

### After Hyperparameter Tuning

Both XGBoost and Random Forest were tuned using `RandomizedSearchCV` (broad exploration) followed by `GridSearchCV` (fine-grained search around the best region).

| Model Version | R² Score | MAE | RMSE |
|--------------|----------|-----|------|
| **✅ Tuned XGBoost (Grid Search)** | **0.5744** | **$67,412,206** | **$140,863,770** |
| Tuned XGBoost (Random Search) | 0.5505 | $68,520,713 | $144,760,660 |
| Default XGBoost | 0.5378 | $70,072,567 | $146,790,839 |
| Default Random Forest | 0.5212 | $68,464,761 | $149,403,008 |
| Tuned Random Forest (Grid) | 0.4887 | $70,059,528 | $154,394,718 |
| Tuned Random Forest (Random) | 0.4740 | $70,886,283 | $156,588,599 |
| Default Decision Tree | 0.3805 | $78,862,572 | $169,942,852 |
| Default Linear Regression | -0.8118 | $98,878,627 | $290,627,437 |

---

## 🏆 Final Model — Tuned XGBoost (GridSearchCV)

The **Tuned XGBoost Regressor** is the clear and definitive winner across all three metrics:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **R² Score** | **0.5744** | Explains ~57.4% of revenue variance |
| **MAE** | **$67.4M** | Average prediction is $67.4M from actual revenue |
| **RMSE** | **$140.9M** | Best at avoiding catastrophically large errors |

### Contextualising the Error

> Mean dataset revenue: **$128.2M**  
> Champion model MAE: **$67.4M**  
> Average error as % of mean: **~52.6%**

This level of error reflects the **inherently chaotic nature of box office prediction**. Even Hollywood studios with access to far richer data (star power, marketing spend, opening weekend tracking) struggle to predict revenue accurately. A 57% R² with publicly available data is a strong result.

---

## 💡 Key Insights & Lessons

| Insight | Detail |
|---------|--------|
| **Tuning was critical for XGBoost** | Baseline R²: 0.538 → Random Search: 0.551 → Grid Search: **0.574** |
| **Tuning hurt Random Forest** | Default RF (R²: 0.521) outperformed all tuned RF versions — overfitting during tuning |
| **Ensemble methods dominate** | XGBoost and RF far surpassed linear models, confirming non-linear revenue dynamics |
| **Log transform was essential** | Without it, Linear Regression would perform even worse on the raw skewed data |
| **Revenue is inherently hard to predict** | 52.6% average error reflects real-world box office volatility, not model weakness |

---

## 🔮 Next Steps — Pipeline & Deployment

The modelling phase is complete. The next objective is to productionize the champion model:

1. **Analyze feature importances** from the tuned XGBoost model to understand what drives predictions
2. **Build a `scikit-learn` Pipeline** combining the `ColumnTransformer` and final model into one portable object
3. **Train on the full dataset** (not just the 80% training split)
4. **Serialize to disk** using `joblib` → `models/final_model.pkl`
5. **Build an inference interface** — a script or API endpoint that accepts movie metadata and returns a revenue prediction

---

## 🚀 How to Run

> ⚠️ You must complete **Phase 2 (Data Cleaning)** before running this script.

```bash
# From the project root
python scripts/modelling_tmdb.py
```

**Expected output:**
```
Loading data from data/cleaned_movies.csv...
Splitting data into train and test sets...

Training and evaluating models...
  Training Linear Regression...
  Training Random Forest...
  Training XGBoost...

--- Model Comparison Results ---
model_name       R-squared         MAE
XGBoost              0.538   70072567
Random Forest        0.521   68464761
Linear Regression   -0.811   98878627

🏆 Best model selected: XGBoost (R²: 0.538)
Saving best model to models/best_revenue_predictor.joblib...
Generating evaluation plot for XGBoost -> plots/best_model_evaluation.png

✅ Model training and selection process complete.
```

---

## 🔗 Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| 1 — Data Collection | TMDB API ingestion pipeline | ✅ Complete |
| 2 — Data Cleaning | Merging, deduplication & filtering | ✅ Complete |
| 3 — EDA | Visualizations & statistical insights | ✅ Complete |
| **4 — Modelling** | ML model training & evaluation | ✅ Complete |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.x-F7931E?logo=scikitlearn&logoColor=white)
![XGBoost](https://img.shields.io/badge/XGBoost-1.x-FF6600)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.x-013243?logo=numpy&logoColor=white)

| Library | Purpose |
|---------|---------|
| `scikit-learn` | Pipeline, ColumnTransformer, train_test_split, metrics, GridSearchCV |
| `xgboost` | XGBRegressor — champion model |
| `pandas` | Data loading and manipulation |
| `numpy` | Log transformation (`log1p` / `expm1`) |
| `joblib` | Model serialization and persistence |
| `matplotlib` / `seaborn` | Actual vs. Predicted evaluation plot |

---

*← Previous: [Phase 3: Exploratory Data Analysis](./README_phase3_eda.md)*  
*Next → [Master README: Full Project Overview](./README.md)*
