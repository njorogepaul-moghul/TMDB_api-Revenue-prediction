# 📊 Phase 3: Exploratory Data Analysis
### TMDB Revenue Prediction — From Clean Data to Actionable Insights

> This phase validates which features are genuinely predictive of movie revenue and identifies the key business patterns in the dataset before any model is built.

---

## 📌 Objectives

- Identify the strongest predictors of movie box office revenue
- Profile the distribution of budget, revenue, runtime, and ratings
- Understand genre-level revenue patterns
- Detect and address skewness in financial variables
- Validate feature engineering decisions for the modelling phase

---

## 📅 Dataset at This Stage

| Property | Value |
|---|---|
| Source | `cleaned_movies.csv` |
| Language Breakdown | 90%+ English · Japanese · French · Korean · Hindi |
| Mean Rating | 6.86 / 10 |
| Median Runtime | 110 minutes |
| Median Popularity Score | 7.61 |

---

## 🔑 Key Findings

### 1. Budget is the Strongest Revenue Predictor (r = 0.68)
The clearest, tightest relationship in the entire dataset. Bigger budgets consistently produce higher revenues — but scatter is wide, confirming blockbusters and flops coexist at all budget levels.

> **"You have to spend money to make money"** — confirmed quantitatively.

### 2. Audience Engagement Mirrors Commercial Success (r = 0.65)
Vote count (total number of ratings) has the second-strongest correlation with revenue. Films that earn more money get more audience engagement — the relationship is bidirectional.

### 3. Newer Films Earn More (Negative Age Correlation)
Movie age is negatively correlated with both revenue and popularity. This reflects ticket price inflation, global box office expansion, and TMDB's recency-weighted popularity scoring.

### 4. Genre Matters for Revenue Ceiling

| Genre Tier | Genres | Revenue Profile |
|---|---|---|
| Highest Median Revenue | Adventure · Animation · Family | Consistently high — blockbuster territory |
| High Variance | Science Fiction · Action | Huge range — biggest hits AND biggest flops |
| Lower-Risk, Lower-Return | Horror · Documentary | Modest, more predictable returns |

### 5. Popularity is Weak Alone (r = 0.15)
Despite intuition, TMDB popularity score is a weak revenue predictor. It is heavily influenced by recency and social media activity — not box office performance directly.

### 6. The Long-Tail Reality
Budget, revenue, and popularity are all **highly right-skewed** — a tiny number of blockbusters dominate while the majority of films earn modest returns. Log transformation applied to budget and revenue before modelling.

---

## 📈 Visualisations Generated

| Plot | Key Insight |
|---|---|
| Revenue distribution histogram | Long-tail — majority earn under $50M |
| Budget vs Revenue scatter | Strong positive trend, wide scatter |
| Genre count bar chart | Drama, Comedy, Thriller most produced |
| Revenue by genre boxplot | Adventure, Animation highest median |
| Revenue by release year line chart | Clear upward trend — recency effect |
| Vote average distribution | Bell curve centred at 6.86 |
| Runtime distribution | Sweet spot: 90–120 minutes |
| Correlation heatmap | Budget (0.68) and vote count (0.65) dominate |
| Pairplot | Full multi-variable relationship dashboard |

---

## 🛠️ Technical Implementation

| Component | Detail |
|---|---|
| Libraries | Pandas · Matplotlib · Seaborn · ast |
| Genre Handling | `ast.literal_eval` to parse string-list format |
| Date Features | `release_year`, `release_month` extracted |
| Transformations | Log scale on popularity distribution |
| Notebook | `TMDB_EDA_phase.ipynb` |
| Script | `EDA_tmdb.py` |

---

> **← Phase 2: Data Cleaning** &nbsp;|&nbsp; **Phase 4: Modelling →**
