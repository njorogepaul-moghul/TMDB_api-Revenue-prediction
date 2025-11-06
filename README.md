# 🎬 Movie Revenue Prediction

This project aims to predict movie revenues using data collected from the **TMDB (The Movie Database) API**.  
It combines **data engineering**, **data cleaning**, **exploratory data analysis**, and **predictive modeling** to uncover insights into what drives a movie’s financial success.

---

# 🧠 Project Overview

The movie industry is driven by many factors — budget, popularity, audience ratings, and more.  
This project leverages TMDB data to:
- Explore movie trends and characteristics.
- Understand correlations between movie features and revenue.
- Build a predictive model to estimate a movie’s potential earnings.

---

# ⚙️ Data Collection phase

Data was obtained using the **TMDB API**, fetching details for popular movies and their metadata such as:
- Budget  
- Revenue  
- Genres  
- Runtime  
- Popularity  
- Ratings  
- Overview  

After fetching the data, two datasets were merged:
1. **popular_df** – movies fetched from TMDB’s “popular” endpoint.  
2. **details_df** – full metadata for each movie (via the `/movie/{id}` endpoint).

---

# 🧹 Data Cleaning phase

Cleaning steps included:
- Merging datasets on the `id` column.  
- Dropping duplicate and irrelevant columns (`poster_path`, `backdrop_path`, `video`, `status`, etc.).  
- Removing rows with missing `overview` or `release_date`.  
- Dropping rows with zero `budget` or `revenue`.  
- Ensuring proper column naming and data types.

Final dataset columns:
original_language → language the movie was produced in (e.g., "en", "fr")
overview → short plot summary or description of the movie
title → movie’s official title
budget → production cost (in USD)
revenue → total earnings (in USD) — your target variable
runtime → movie duration in minutes
release_date → when the movie was released
popularity → TMDB’s popularity metric based on views and ratings
vote_average → average user rating (0–10)
vote_count → total number of user ratings
genres → list of movie genres (e.g., Action, Drama, Comedy)


The cleaned dataset was saved as:data/cleaned_movies.csv

# 📊 TMDB Movie Database - Exploratory Data Analysis (EDA) phase

## Setup & Imports

The analysis is conducted in a Jupyter Notebook using the following core Python libraries:
* **pandas:** For data loading and manipulation.
* **seaborn** & **matplotlib.pyplot:** For data visualization.
* **numpy:** For numerical operations.
* **ast.literal_eval:** For processing list-like string data (genres).
* **sklearn.preprocessing.MultiLabelBinarizer:** For one-hot encoding the genre data for correlation analysis.

---

## Data Loading & Feature Engineering

1.  **Load Data:** The analysis begins by loading a pre-cleaned dataset named `cleaned_movies.csv` into a pandas DataFrame.
2.  **Feature Engineering (Genres):** The `genres` column, which is stored as a string (e.g., `['Action', 'Thriller']`), is converted into a proper Python list to be analyzed.
3.  **Feature Engineering (Movie Age):** A new feature, `movie_age`, is engineered by calculating the difference in years between the movie's `release_date` and the analysis date (noted in the notebook as October 29, 2025). This helps us analyze trends over time.

---

## Analysis & Visualizations

### 1. Movie Language Distribution (Bar Chart)
* **Analysis:** A horizontal bar chart was generated to count the number of movies per `original_language`.
* **Insight:** This chart clearly shows that our dataset is overwhelmingly dominated by English-language films. This is important to know because it means our analysis and any conclusions we draw will primarily reflect the English-language movie market.

### 2. Movie Budget & Revenue Distributions (Histograms)
* **Analysis:** Two separate histograms were created to visualize the distribution of movie `budget` and `revenue`.
* **Insight:** Both of these charts tell a similar story: the movie industry is driven by a "long tail." The vast majority of films are made with smaller budgets (e.g., under $50 million) and earn modest returns. Only a tiny handful of films are massive "blockbusters" with huge budgets and revenues. This tells us that blockbusters are the exception, not the rule.

### 3. Movie Popularity Distribution (Histogram)
* **Analysis:** A histogram of `popularity` scores was created. A log scale was used to make the "long tail" pattern clearer.
* **Insight:** Like revenue and budget, popularity is a "long tail" metric. The vast majority of movies have a low popularity score (under 10), while a very small number of recent hits or massive blockbusters have extremely high scores. The median (halfway point) popularity score is **7.61**.

### 4. Movie Rating Distribution (Histogram)
* **Analysis:** A histogram showing the distribution of `vote_average` from 0 to 10.
* **Insight:** This chart shows the spread of audience ratings. We can see a "normal" distribution (a bell curve) that is slightly skewed to the left. The mean (or average) rating for all movies in the dataset is **6.86 out of 10**. This suggests that audiences are generally positive but also critical.

### 5. Movie Runtime Distribution (Histogram)
* **Analysis:** A histogram showing the distribution of movie `runtime` in minutes.
* **Insight:** This chart clearly shows how long movies typically are. The vast majority of films run between 90 and 120 minutes (1.5 to 2 hours). The red dotted line shows the median (or halfway point) for all films is **110 minutes**.

### 6. Genre Distribution (Pie & Bar Charts)
* **Analysis:** The `genres` column was analyzed to find the frequency of each individual genre across the entire dataset.
* **Insight:** Across the entire dataset, **Drama**, **Comedy**, and **Thriller** are the three most frequently produced genres. This suggests a consistent market demand for these types of films, or that they are perhaps "safer" for studios to produce.

### 7. Revenue by Genre (Box Plot)
* **Analysis:** A boxplot was generated to compare the range of `revenue` for each genre. A log scale was used for readability.
* **Insight:** This plot gives us a much deeper look at revenue. The "box" in the middle of each line shows the typical range (the middle 50%) of revenue for a genre.
    * **Highest Potential:** **Adventure, Animation, and Family** films have the highest median revenues and their boxes are shifted furthest to the right. This means they are consistently high-earning genres.
    * **Wide Variation:** Genres like **Adventure** and **Science Fiction** have very long lines, showing they have huge variability. They produce some of the biggest blockbusters, but also many lower-earning films.
    * **Lower-Risk, Lower-Reward:** **Horror** and **Documentary** films have the lowest median revenues.

### 8. Relationships Over Time (Scatter Plots)
* **Analysis:** Two scatter plots were created: `Revenue vs. Movie Age` and `Popularity vs. Movie Age`.
* **Insight (Revenue):** This chart suggests that **newer movies tend to earn more revenue**. The trend line slopes downwards, meaning as 'movie_age' goes up (the film gets older), revenue tends to go down. This makes sense due to factors like ticket price inflation and the expansion of the global box office.
* **Insight (Popularity):** Just like revenue, **newer movies tend to have higher 'popularity' scores**. This indicates that the popularity metric on TMDB is heavily influenced by recency. Films that are currently being marketed or just released will naturally have a higher score.

### 9. Budget vs. Revenue (Scatter Plot)
* **Analysis:** A scatter plot (with log scales) was used to visualize the relationship between `budget` and `revenue`.
* **Insight:** This plot confirms one of the strongest relationships in the dataset (a 0.68 correlation). The clear upward trend confirms a simple business reality: **"You have to spend money to make money."** As a film's budget increases, its potential revenue increases significantly. However, the wide scatter of points shows this isn't a guarantee: there are many high-budget flops and low-budget hits.

### 10. Popularity vs. Revenue (Scatter Plot)
* **Analysis:** A scatter plot (with log scales) was used to visualize the relationship between `popularity` and `revenue`.
* **Insight:** This plot shows a clear positive relationship: **as a movie's popularity score goes up, its revenue tends to go up as well.** However, the points form a very wide cloud. This tells us that while popularity is a good indicator, it's not a guarantee of success.

### 11. Runtime vs. Average Rating (Scatter Plot)
* **Analysis:** A scatter plot was created to see if movie `runtime` affects the `vote_average`.
* **Insight:** This plot shows a slight but interesting positive trend (a 0.34 correlation): **longer movies tend to have slightly higher ratings.** This doesn't mean making a movie longer will make it better, but it could suggest that films that *earn* a longer runtime (like epic dramas) are often higher-quality productions.

### 12. Runtime vs. Popularity (Scatter Plot)
* **Analysis:** A scatter plot was created to see if `runtime` affects `popularity`.
* **Insight:** This plot shows a very weak positive relationship (a 0.11 correlation). The trend line is almost flat. This tells us that **runtime is not a strong predictor of popularity.** Audiences enjoy both short and long films.

### 13. Correlation Heatmap
* **Analysis:** A heatmap was generated to show the correlation coefficient between all numerical features at a glance.
* **Insight:** This chart is a powerful, high-level summary. The brightest squares show the strongest relationships, confirming our findings:
    * **Revenue & Budget (0.68):** A strong positive link.
    * **Revenue & Vote Count (0.65):** Also a strong link. Commercially successful films get more audience engagement (votes).

### 14. Pairplot (Dashboard Plot)
* **Analysis:** A `pairplot` was created to show all numerical relationships in a single "dashboard" of plots.
* **Insight:** This dashboard confirms all our key findings at a glance. The diagonal shows the (skewed) distributions, and the scatter plots confirm the strong relationship between `budget` and `revenue`, the time-based trends for `movie_age`, and the weaker relationships for `runtime`.

---

## 📈 Executive Summary: Key Takeaways

Based on the full analysis, here are the most important:

1.  **Spend Money to Make Money:** The single strongest predictor of high revenue is a **large budget**. The correlation is strong (0.68). While not a guarantee, bigger budgets lead to bigger returns.
2.  **Genre Matters for Revenue:** If the goal is high revenue, **Adventure**, **Animation**, and **Family** films consistently have the highest median box office. **Horror** and **Documentary** films have the lowest, suggesting they are safer, lower-risk/lower-reward investments.
3.  **Newer is Better:** Newer movies consistently show higher revenue and higher popularity scores. This is likely a combination of ticket price inflation and the recency bias of a "popularity" metric (what's "buzzing" now).
4.  **The Market is a "Long Tail":** Most movies are *not* blockbusters. The vast majority of films have modest budgets, revenues, and popularity scores. Blockbusters are the rare exception, not the rule.
5.  **What *Doesn't* Matter as Much:** A movie's **runtime does not predict its popularity**. While very long films (2.5+ hours) are rare, audiences do not seem to penalize a film for being long or short.

   **The encoded dataset was saved as TMDB project/data/encoded_movies.csv**


# TMDB Movie Revenue Prediction- Modelling phase

## 🧩 Introduction

This project aims to **predict the box office revenue** of movies using data collected from **The Movie Database (TMDB) API**.

This notebook (`TMDB modelling phase.ipynb`) covers the end-to-end process of building and evaluating predictive models. This follows previous stages of data collection, data cleaning, and exploratory data analysis (EDA). The goal is to identify the best-performing algorithm for revenue prediction based on features like `budget`, `popularity`, `runtime`, and `genre`.

## ⚙️ Methodology

The notebook follows a structured approach to modeling:

### 1. Data Loading
* The preprocessed and encoded dataset (`encoded_movies.csv`) is loaded.

### 2. Feature Engineering
Before modeling, several features were engineered to improve performance:
* **Log Transformation:** The `revenue` (target) and `budget` (feature) columns were log-transformed using `np.log1p()` to handle their right-skewed distributions.
* **New Ratio Feature:** A new feature, `budget_popularity_ratio`, was created.
* **Binning & Encoding:** The continuous `runtime` feature was binned into four categories ('Short', 'Medium', 'Long', 'Very Long') and then one-hot encoded for model consumption.

### 3. Model Training
* The dataset was split into training (80%) and testing (20%) sets.
* Four different regression algorithms were trained using their default settings:
    1.  Linear Regression
    2.  Decision Tree Regressor
    3.  Random Forest Regressor
    4.  XGBoost Regressor

### 4. Model Evaluation
* All models were evaluated on the test set using **R²**, **MAE (Mean Absolute Error)**, and **RMSE (Root Mean Squared Error)**.
* Crucially, the log-transformed predictions were reversed (`np.expm1`) to evaluate all models on their **original dollar scale** performance.

## ✅ Results & Comparison

To properly contextualize the errors, the mean revenue of the dataset was calculated: **\$128,210,875**.

The performance of the models on the original dollar scale is as follows:

| Model | R² Score (Higher is Better) | MAE (Lower is Better) | RMSE (Lower is Better) |
| :--- | :--- | :--- | :--- |
| **XGBoost Regressor** | **0.5378** | \$70,072,567 | **\$146,790,839** |
| **Random Forest** | 0.5212 | **\$68,464,761** | \$149,403,008 |
| **Decision Tree** | 0.3805 | \$78,862,572 | \$169,942,852 |
| **Linear Regression** | -0.8118 | \$98,878,627 | \$290,627,437 |

### Analysis
* **Linear Regression** failed to model the non-linear relationships, producing a negative R² score.
* The **Decision Tree** was a major improvement but was clearly outperformed by the ensemble methods.
* **Random Forest** achieved the **best (lowest) MAE**, meaning its predictions were, on average, the closest to the actual revenue (~53% error relative to the mean).
* **XGBoost Regressor** was the **top overall performer**, with the **best R² score** (explaining ~54% of revenue variance) and the **best (lowest) RMSE**, indicating it was most effective at avoiding large, costly prediction errors.

##  Final Model Comparison & Conclusion(after hyperparameter tuning)

We have now built, evaluated, and tuned our models. The final step is to compare our best-performing models to select a single champion for our pipeline.

### Final Model Performance

This table shows the performance of the **best version** of each model we tested, evaluated on the original dollar scale.

| Model Version | R² Score (Higher is Better) | MAE (Lower is Better) | RMSE (Lower is Better) |
| :--- | :--- | :--- | :--- |
| **Tuned XGBoost (Grid Search)** | **0.5744** | **\$67,412,206** | **\$140,863,770** |
| Tuned XGBoost (Random Search) | 0.5505 | \$68,520,713 | \$144,760,660 |
| Default XGBoost | 0.5378 | \$70,072,567 | \$146,790,839 |
| Default Random Forest | 0.5212 | \$68,464,761 | \$149,403,008 |
| Tuned Random Forest (Grid) | 0.4887 | \$70,059,528 | \$154,394,718 |
| Tuned Random Forest (Random) | 0.4740 | \$70,886,283 | \$156,588,599 |
| Default Decision Tree | 0.3805 | \$78,862,572 | \$169,942,852 |
| Default Linear Regression | -0.8118 | \$98,878,627 | \$290,627,437 |

---

##  Conclusion & Insights

### 🏆 The Champion Model

The **Tuned XGBoost Regressor (from `GridSearchCV`)** is the clear and definitive winner. It outperformed all other models across all three evaluation metrics:

1.  **Highest R² (0.5744):** It explains approximately **57.4%** of the variance in movie revenue, the most of any model.
2.  **Lowest MAE (\$67.4M):** Its predictions are the most accurate on average.
3.  **Lowest RMSE (\$140.9M):** It is the most effective at avoiding very large, costly prediction errors.

### 💡 Key Insights

* **Tuning was Critical:** Hyperparameter tuning was highly effective. Our baseline XGBoost model (R²: 0.538) saw a significant performance boost from randomized search (R²: 0.551) and another solid jump from focused grid search (R²: 0.574).
* **Contextualizing Error:** Our final model's average error is **\$67.4 million**. Compared to the dataset's mean revenue of **\$128.2 million**, this means our model's predictions are, on average, off by about **52.6%**. This highlights the inherent difficulty and high variance in predicting box office success, even with good data.
* **Model Selection Matters:** The ensemble methods (XGBoost, Random Forest) were dramatically better than the simpler Linear Regression and Decision Tree models, confirming that the relationships in the data are complex and non-linear.
* **Tuning Isn't Always Better:** For Random Forest, the default parameters (R²: 0.521) were more robust than any of our tuned versions, which appeared to overfit the training data and performed worse on the test set.

**Final Decision:** The model `final_model` (the `best_estimator_` from our `xgb_grid_search`) is our champion model and will be the one we productionalize.

---

## Next Steps: Pipeline Development

The modeling and selection phase is complete. Our next objective is to build a robust, reproducible production **pipeline**.

This will involve:
1.  **Analyzing Feature Importances** from our `final_model` to understand *what* drives its predictions.
2.  **Creating a `ColumnTransformer`** to perform all of our feature engineering steps (log-transforming, binning, encoding) in one object.
3.  **Building a `scikit-learn` Pipeline** that combines the `ColumnTransformer` with our `final_model`.
4.  **Training this single pipeline** on the full dataset and **saving it to a file** (e.g., `final_model.pkl`) so it can be easily loaded in another script or application for predictions.














