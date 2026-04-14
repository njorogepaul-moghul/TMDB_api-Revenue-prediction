# 🎬 TMDB Movie Revenue Prediction
## Phase 1 — Data Collection

> **Part of a multi-phase machine learning project** that predicts movie box office revenue using data from The Movie Database (TMDB) API.

---

## 📌 Overview

This phase covers the **end-to-end data acquisition pipeline** for the project. Raw data was collected directly from the **TMDB REST API** using a two-stage fetching strategy — first gathering a large list of popular movies, then enriching each entry with full financial and metadata details.

The result is a merged, raw dataset of **~4,000 movies** ready for cleaning and analysis in the next phase.

---

## 🎯 Objectives

- Authenticate securely with the TMDB API using environment variables
- Fetch a high-volume list of popular movies across 200 pages
- Enrich each movie with detailed financial metadata (budget, revenue, runtime, genres, etc.)
- Merge both datasets and persist to disk as a structured CSV
- Implement rate-limiting and error handling for robust, production-style API calls

---

## 🗂️ Files

| File | Description |
|------|-------------|
| `scripts/fetch_tmdb.py` | Main data collection script |
| `data/popular_movies.csv` | Raw list of popular movies from TMDB's `/movie/popular` endpoint |
| `data/movies_full.csv` | Merged dataset with full movie details |
| `.env` | Stores the TMDB API key (excluded from version control) |
| `.gitignore` | Ensures `.env` and sensitive files are not committed |

---

## ⚙️ How It Works

The collection script (`fetch_tmdb.py`) runs in two sequential phases:

### Phase 1A — Fetch Popular Movie List

```python
GET /movie/popular?language=en-US&page={page}
```

- Iterates through **200 pages** of TMDB's popularity-ranked movie list
- Each page returns **20 movies**, yielding up to **4,000 entries**
- Saves results to `data/popular_movies.csv`

### Phase 1B — Fetch Full Movie Details

```python
GET /movie/{movie_id}?language=en-US
```

- Loops through every movie ID collected in Phase 1A
- Extracts the following fields for each movie:

| Field | Description |
|-------|-------------|
| `id` | Unique TMDB movie identifier |
| `title` | Official movie title |
| `budget` | Production budget (USD) |
| `revenue` | Total box office earnings (USD) |
| `runtime` | Movie duration in minutes |
| `release_date` | Theatrical release date |
| `popularity` | TMDB's rolling popularity score |
| `vote_average` | Mean audience rating (0–10) |
| `vote_count` | Total number of user ratings |
| `genres` | List of genre labels (e.g., `['Action', 'Drama']`) |

- Results are **merged with the popular movies list** on the `id` column using a left join
- Final dataset is saved to `data/movies_full.csv`

---

## 🔐 Authentication

API requests use **Bearer Token authentication** (TMDB's recommended method):

```python
headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {API_KEY}"
}
```

The API key is loaded from a `.env` file using `python-dotenv`:

```ini
# .env
TMDB_API_KEY=your_api_key_here
```

> ⚠️ **Never commit your `.env` file.** It is listed in `.gitignore`.  
> Get your free API key at [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

---

## 🛡️ Rate Limiting & Error Handling

| Strategy | Implementation |
|----------|----------------|
| Respectful rate limiting | `time.sleep(0.25)` between every API call |
| HTTP error handling | `response.raise_for_status()` catches 4xx/5xx responses |
| Network error handling | `try/except requests.exceptions.RequestException` |
| Graceful early exit | Stops fetching if a page returns no results |

---

## 📦 Output

| File | Rows (approx.) | Description |
|------|----------------|-------------|
| `data/popular_movies.csv` | ~4,000 | Basic movie metadata from the popular endpoint |
| `data/movies_full.csv` | ~4,000 | Enriched dataset after merging with full details |

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/your-username/tmdb-revenue-prediction.git
cd tmdb-revenue-prediction
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up your API key
```bash
# Create a .env file in the project root
echo "TMDB_API_KEY=your_key_here" > .env
```

### 4. Run the data collection script
```bash
python scripts/fetch_tmdb.py
```

> **Expected runtime:** ~30–45 minutes for 200 pages + 4,000 detail calls (due to rate limiting)

---

## 🔗 Project Phases

| Phase | Description | Status |
|-------|-------------|--------|
| **1 — Data Collection** | TMDB API ingestion pipeline | ✅ Complete |
| 2 — Data Cleaning | Merging, deduplication & filtering | ✅ Complete |
| 3 — EDA | Visualizations & statistical insights | ✅ Complete |
| 4 — Modelling | ML model training & evaluation | ✅ Complete |

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-HTTP-orange)
![TMDB](https://img.shields.io/badge/TMDB-API-01B4E4?logo=themoviedatabase&logoColor=white)

| Library | Purpose |
|---------|---------|
| `requests` | HTTP calls to the TMDB REST API |
| `pandas` | DataFrame creation and CSV persistence |
| `tqdm` | Progress bars for long-running loops |
| `python-dotenv` | Secure API key management via `.env` |
| `time` | Rate limiting between API requests |

---

*Next → [Phase 2: Data Cleaning](./README_phase2_data_cleaning.md)*
