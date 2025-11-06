import pandas as pd
import os

def clean_movie_data(input_path, output_path):
    """
    Loads the merged TMDB dataset, performs all cleaning steps,
    and saves the result to a new CSV file.
    
    Cleaning steps include:
    - Renaming columns
    - Dropping duplicates
    - Dropping unnecessary columns (e.g., adult, video, status)
    - Dropping rows with missing values (release_date, overview)
    - Filtering out movies with 0 budget or 0 revenue
    """
    
    try:
        # --- 1. Load Data ---
        print(f"Loading data from {input_path}...")
        df = pd.read_csv(input_path)
        print(f"Initial shape: {df.shape}")

        # --- 2. Clean Column Names ---
        # (This combines cells 5 and 6 from your notebook)
        print("Cleaning column names...")
        
        # Check if 'popularity_x' exists before dropping (in case script is run twice)
        if 'popularity_x' in df.columns:
            # Drop the redundant '_x' columns
            df = df.drop(columns=[
                'popularity_x', 'release_date_x', 'title_x', 
                'vote_average_x', 'vote_count_x'
            ])
            
            # Rename the '_y' columns to be clean
            df = df.rename(columns={
                'title_y': 'title',
                'popularity_y': 'popularity',
                'release_date_y': 'release_date',
                'vote_average_y': 'vote_average',
                'vote_count_y': 'vote_count'
            })
        
        # --- 3. Drop Duplicates ---
        # (From cell 12)
        initial_rows = df.shape[0]
        df.drop_duplicates(inplace=True)
        print(f"Dropped {initial_rows - df.shape[0]} duplicate rows.")

        # --- 4. Drop Unnecessary Columns ---
        # (From cell 16)
        print("Dropping unnecessary columns...")
        columns_to_drop = [
            'backdrop_path', 'poster_path', 'adult', 'video', 'status',
            'original_title', 'id', 'genre_ids'
        ]
        # We use 'errors="ignore"' in case a column was already dropped
        df.drop(columns=columns_to_drop, inplace=True, errors='ignore')

        # --- 5. Handle Missing Values ---
        # (From cells 18 and 19)
        print("Dropping rows with missing values...")
        df.dropna(subset=['release_date', 'overview'], inplace=True)

        # --- 6. Filter 0 Budget/Revenue ---
        # (From cell 23)
        print("Filtering out movies with zero budget or revenue...")
        df = df[(df['budget'] != 0) & (df['revenue'] != 0)]

        # --- 7. Save Data ---
        # (From cell 27)
        
        # Ensure the output directory exists
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        df.to_csv(output_path, index=False)
        print(f"\n✅ Successfully cleaned data and saved {df.shape[0]} rows to {output_path}")
        
        return df

    except FileNotFoundError:
        print(f"⚠️ Error: Input file not found at {input_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# This part makes the script runnable from the command line
if __name__ == "__main__":
    # Define the file paths.
    # Note: These are relative paths, assuming 'data' is in the same folder.
    # This is more flexible than the absolute 'C:/Users/...' path.
    INPUT_FILE = "data/movies_full.csv"
    OUTPUT_FILE = "data/cleaned_movies.csv"
    
    # Run the cleaning function
    clean_movie_data(INPUT_FILE, OUTPUT_FILE)