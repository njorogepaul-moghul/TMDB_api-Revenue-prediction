# 🤖 Phase 4: Modelling & Evaluation
### TMDB Revenue Prediction — From Features to a Validated Revenue Predictor

> Four regression models trained, compared, and tuned. Champion: Tuned XGBoost explaining 57.4% of variance in movie revenue on a $128M mean dataset.

---

## 📌 Objective

Build a validated machine learning model that predicts movie box office revenue from pre-release features — budget, popularity, runtime, language, and vote metrics.

---

## ⚙️ Features Used

| Feature | Type | Notes |
|---|---|---|
| `budget` | Numerical | Log-transformed — strongest predictor |
| `vote_count` | Numerical | Audience engagement signal |
| `popularity` | Numerical | TMDB popularity score |
| `runtime` | Numerical | Film duration in minutes |
| `vote_average` | Numerical | Audience rating 0–10 |
| `original_language` | Categorical | One-hot encoded |
| Genre flags | Binary (×15) | Action, Adventure, Horror, etc. |
| `movie_age` | Numerical | Years since release |
| `budget_popularity_ratio` | Engineered | Interaction feature |

**Total features after encoding: 26**

---

## 🔧 Pipeline Architecture

Each model was wrapped in a Scikit-Learn `Pipeline` with a `ColumnTransformer` preprocessor:

```python
Pipeline([
    ('preprocessor', ColumnTransformer([
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])),
    ('regressor', model)
])
```

---

## 🏆 Model Comparison (Original Dollar Scale)

| Model | R² | MAE | RMSE |
|---|---|---|---|
| **Tuned XGBoost (Grid) ✅** | **0.5744** | **$67,412,206** | **$140,863,770** |
| Tuned XGBoost (Random) | 0.5505 | $68,520,713 | $144,760,660 |
| Default XGBoost | 0.5378 | $70,072,567 | $146,790,839 |
| Default Random Forest | 0.5212 | $68,464,761 | $149,403,008 |
| Tuned Random Forest (Grid) | 0.4887 | $70,059,528 | $154,394,718 |
| Tuned Random Forest (Random) | 0.4740 | $70,886,283 | $156,588,599 |
| Default Decision Tree | 0.3805 | $78,862,572 | $169,942,852 |
| Linear Regression | -0.8118 | $98,878,627 | $290,627,437 |

> Mean dataset revenue: **$128,210,875** — champion MAE of $67.4M represents ~53% of mean revenue.

---

## 🔧 Champion Model: Tuned XGBoost

**Tuning Methodology:** RandomizedSearchCV → GridSearchCV (two-stage)

```python
# Final Grid Search parameters
{
    'colsample_bytree': 0.85,
    'learning_rate': 0.015,
    'max_depth': 3,
    'n_estimators': 700,
    'subsample': 0.9
}
```

**Log-scale R² during tuning: 0.5449** (GridSearch)

---

## 💡 Key Insights

- **Linear Regression failed completely** (R² = -0.8118) — revenue has strong nonlinear relationships that linear models cannot capture
- **Tree-based models dominate** — both Random Forest and XGBoost outperform linear and decision tree baselines by a wide margin
- **Tuning via two-stage search** consistently improves XGBoost: default R² 0.5378 → tuned 0.5744 (+7% improvement)
- **Log transformation on target** was essential — models evaluated on log scale then reversed via `np.expm1` for dollar-scale reporting
- **Budget remains the key signal** — reflected in XGBoost feature importance across all tuning rounds

---

## 💾 Saved Artifacts

| File | Description |
|---|---|
| `models/best_revenue_predictor.joblib` | Full sklearn pipeline — preprocessor + tuned XGBoost |
| `plots/best_model_evaluation.png` | Actual vs predicted scatter plot |

---

## 🛠️ Tech Stack

```
Python · Scikit-Learn · XGBoost · Pandas · Joblib · Matplotlib · Seaborn
```

---

## 📁 Files

```
modelling_tmdb.py           # Modular production script
TMDB_modelling_phase.ipynb  # Interactive notebook version
```

---

> **← Phase 3: EDA** &nbsp;|&nbsp; **Back to Main README →**
