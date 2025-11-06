import os
import time
import requests
import pandas as pd
from tqdm import tqdm
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv('TMDB_API_KEY')
BASE_URL = "https://api.themoviedb.org/3"
DATA_DIR = "data"
POPULAR_MOVIES_FILE = os.path.join(DATA_DIR, "popular_movies.csv")
FULL_MOVIES_FILE = os.path.join(DATA_DIR, "movies_full.csv")

# --- Helper Functions ---

def fetch_from_api(url):
    """Handles a single request to the TMDB API, returning the JSON or None."""
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {API_KEY}" # Recommended way
    }
    # Note: Using API_KEY as a query param is also fine, but Bearer token is preferred.
    # url_with_key = f"{url}&api_key={API_KEY}" 
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ API request error: {e}")
        return None

def get_popular_movies(page=1):
    """Fetches one page (20 movies) of popular movies."""
    url = f"{BASE_URL}/movie/popular?language=en-US&page={page}"
    data = fetch_from_api(url)
    if data:
        return data.get('results', [])
    return []

def get_movie_details(movie_id):
    """Fetches full details for a single movie by its ID."""
    url = f"{BASE_URL}/movie/{movie_id}?language=en-US"
    return fetch_from_api(url)

# --- Main Logic ---

def fetch_all_popular_movies(num_pages=200):
    """Fetches and saves the list of popular movies."""
    print("--- Phase 1: Fetching Popular Movie List ---")
    all_movies = []
    for page in tqdm(range(1, num_pages + 1), desc="Fetching popular movies"):
        movies = get_popular_movies(page)
        if not movies:
            print(f"No results on page {page}, stopping.")
            break
        all_movies.extend(movies)
        time.sleep(0.25)  # Pause to avoid rate limit

    popular_df = pd.DataFrame(all_movies)
    
    # --- FIX WAS HERE ---
    # Original said: df.to_csv(...)
    # Corrected: popular_df.to_csv(...)
    popular_df.to_csv(POPULAR_MOVIES_FILE, index=False)
    
    # --- FIX WAS HERE ---
    # Original said: len(df)
    # Corrected: len(popular_df)
    print(f"\n✅ Saved {len(popular_df)} movies to {POPULAR_MOVIES_FILE}")
    
    # --- FIX WAS HERE ---
    # Original said: df[['title', ...]]
    # Corrected: popular_df[['title', ...]]
    print(popular_df[['title', 'release_date', 'vote_average']].head())
    
    return popular_df

def fetch_all_details(popular_df):
    """Fetches and saves the full details for the movies in popular_df."""
    print("\n--- Phase 2: Fetching Full Movie Details ---")
    if 'id' not in popular_df.columns:
        print("Error: 'id' column not found in DataFrame.")
        return

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
        time.sleep(0.25)  # Avoid rate limits

    details_df = pd.DataFrame(details_list)
    
    # Merge the details with the original summary dataset
    merged_df = pd.merge(popular_df, details_df, on='id', how='left')
    
    # Save the merged file
    merged_df.to_csv(FULL_MOVIES_FILE, index=False)
    
    print(f"\n✅ Merged dataset saved: {FULL_MOVIES_FILE}")
    print(merged_df[['title_x', 'budget', 'revenue', 'runtime']].head())
    return merged_df

def main():
    """Main function to run the data fetching process."""
    if not API_KEY:
        print("Error: TMDB_API_KEY not found. Please set it in your .env file.")
        return

    os.makedirs(DATA_DIR, exist_ok=True)
    
    try:
        # Phase 1
        popular_df = fetch_all_popular_movies(num_pages=200)
        
        # Phase 2
        if not popular_df.empty:
            fetch_all_details(popular_df)
        else:
            print("No popular movies fetched, skipping detail fetch.")
            
        print("\nAll data fetching complete.")
        
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()