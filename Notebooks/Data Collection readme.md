# 📡 Phase 1: Data Collection
### TMDB Revenue Prediction — API Ingestion Pipeline

> This phase programmatically fetches 4,000+ movies from The Movie Database (TMDB) API using a two-stage ingestion strategy — first collecting a summary list, then enriching each film with full financial and metadata details.

---

## 📌 Overview

| Property | Value |
|---|---|
| API Source | TMDB (The Movie Database) — themoviedb.org |
| Endpoint 1 | `/movie/popular` — summary list |
| Endpoint 2 | `/movie/{id}` — full details per film |
| Pages Fetched | 200 pages × 20 movies = **4,000 movies** |
| Output | `movies_full.csv` — merged dataset |

---

## ⚙️ Two-Stage Collection Strategy

### Stage 1 — Popular Movie List (`/movie/popular`)
Fetches 200 pages of popular movies (20 per page) with summary-level fields:

```
title · release_date · vote_average · vote_count · popularity · genre_ids · id
```

Rate limiting handled with `time.sleep(0.25)` between requests. Progress tracked via `tqdm`.

### Stage 2 — Full Movie Details (`/movie/{id}`)
For each of the 4,000 movie IDs fetched in Stage 1, a second API call retrieves:

```
budget · revenue · runtime · status · genres (named) · popularity · vote_average · vote_count
```

### Stage 3 — Merge
Both datasets are joined on `id` and saved as `movies_full.csv`.

---

## 🛠️ Tech Stack

```
Python · requests · pandas · tqdm · python-dotenv · os · time
```

---

## 🔐 API Key Setup

```bash
# Create a .env file in the project root
echo "TMDB_API_KEY=your_key_here" > .env
```

Get a free API key at [themoviedb.org/settings/api](https://www.themoviedb.org/settings/api)

---

## 📂 Outputs

| File | Description |
|---|---|
| `data/popular_movies.csv` | 4,000 movies — summary fields |
| `data/movie_details.csv` | Full details per movie |
| `data/movies_full.csv` | Merged dataset — ready for cleaning |

---

## 📁 Files

```
fetch_tmdb.py                      # Modular production script
TMDB_data_collection_phase.ipynb   # Interactive notebook version
```

---

> **Next → Phase 2: Data Cleaning**
