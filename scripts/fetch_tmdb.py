import os
import requests
from dotenv import load_dotenv

load_dotenv()  # loads your .env file
API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"

def get_movie(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Example
movie = get_movie(550)  # Fight Club
print(movie)

#now that we have confirmed that our connection is working , we go ahead and fetch foer more movies
import time
import pandas as pd
from tqdm import tqdm  # for progress bar 
#we define our function
def get_popular_movies(page=1):
    """Fetch one page (20 movies) of popular movies."""
    url = f"{BASE_URL}/movie/popular?api_key={API_KEY}&language=en-US&page={page}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('results', [])
    else:
        print(f"⚠️  Error {response.status_code} on page {page}")
        return []

# Fetch multiple pages safely
all_movies = []
num_pages = 200  # ~4000 movies

for page in tqdm(range(1, num_pages + 1), desc="Fetching popular movies"):
    movies = get_popular_movies(page)
    all_movies.extend(movies)
    time.sleep(0.25)  # pause to avoid rate limit

# Convert to DataFrame and save
popular_df = pd.DataFrame(all_movies)
os.makedirs("data", exist_ok=True)
df.to_csv("data/popular_movies.csv", index=False)

print(f"\n✅ Saved {len(df)} movies to data/popular_movies.csv")
print(df[['title', 'release_date', 'vote_average']].head())

# --- Function to fetch full details for one movie ---
def get_movie_details(movie_id):
    url = f"{BASE_URL}/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# --- Fetch details for all movies ---
details_list = []
for mid in tqdm(popular_df['id'], desc="Fetching movie details"):
    data = get_movie_details(mid)
    if data:
        details_list.append({
            'id': data.get('id'),
            'title': data.get('title'),
            'budget': data.get('budget'),
            'revenue': data.get('revenue'),
            'runtime': data.get('runtime'),
            'status': data.get('status'),
            'release_date': data.get('release_date'),
            'popularity': data.get('popularity'),
            'vote_average': data.get('vote_average'),
            'vote_count': data.get('vote_count'),
            'genres': [g['name'] for g in data.get('genres', [])]
        })
    time.sleep(0.25)  # avoid rate limits

details_df = pd.DataFrame(details_list)

# --- Merge the details with your original summary dataset ---
merged_df = pd.merge(popular_df, details_df, on='id', how='left')

# --- Save the merged file ---
os.makedirs("data", exist_ok=True)
merged_df.to_csv("data/movies_full.csv", index=False)

print(f"\n✅ Merged dataset saved: data/movies_full.csv")
print(merged_df[['title_x', 'budget', 'revenue', 'runtime']].head())
