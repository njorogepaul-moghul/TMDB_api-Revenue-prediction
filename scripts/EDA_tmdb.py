import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import ast  # For safely evaluating the string-list of genres

# --- Configuration ---
DATA_FILE = "data/cleaned_movies.csv"
PLOT_DIR = "plots"

# --- Helper Functions ---

def preprocess_data(df):
    """Prepares the DataFrame for plotting."""
    print("Preprocessing data...")
    
    # Convert release_date to datetime objects
    df['release_date'] = pd.to_datetime(df['release_date'])
    
    # Extract year and month
    df['release_year'] = df['release_date'].dt.year
    df['release_month'] = df['release_date'].dt.month
    
    # Convert 'genres' column from string-list to actual list
    # e.g., "['Action', 'Drama']" -> ['Action', 'Drama']
    try:
        df['genres'] = df['genres'].apply(ast.literal_eval)
    except ValueError as e:
        print(f"Warning: Could not process genres. Error: {e}")
        # Fill with empty list if conversion fails
        df['genres'] = df['genres'].apply(lambda x: [] if pd.isna(x) else x)
        
    return df

def plot_genre_counts(df, save_path):
    """Generates and saves a bar plot of top movie genres."""
    print(f"Generating genre plot -> {save_path}")
    
    # Explode the genres list into separate rows
    df_exploded = df.explode('genres')
    genre_counts = df_exploded['genres'].value_counts().head(10)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x=genre_counts.values, y=genre_counts.index, palette='viridis')
    plt.title('Top 10 Movie Genres', fontsize=16)
    plt.xlabel('Number of Movies', fontsize=12)
    plt.ylabel('Genre', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_revenue_distribution(df, save_path):
    """Generates and saves a histogram of movie revenue."""
    print(f"Generating revenue distribution -> {save_path}")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['revenue'], kde=True, bins=30, color='blue')
    plt.title('Distribution of Movie Revenue', fontsize=16)
    plt.xlabel('Revenue (in Billions USD)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_budget_revenue_scatter(df, save_path):
    """Generates and saves a scatter plot of budget vs. revenue."""
    print(f"Generating budget vs. revenue scatter -> {save_path}")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='budget', y='revenue', data=df, alpha=0.5)
    plt.title('Revenue vs. Budget', fontsize=16)
    plt.xlabel('Budget', fontsize=12)
    plt.ylabel('Revenue', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_correlation_heatmap(df, save_path):
    """Generates and saves a heatmap of numeric correlations."""
    print(f"Generating correlation heatmap -> {save_path}")
    numeric_cols = ['budget', 'revenue', 'runtime', 'popularity', 
                    'vote_average', 'vote_count', 'release_year']
    
    corr_matrix = df[numeric_cols].corr()
    
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', vmin=-1, vmax=1)
    plt.title('Correlation Heatmap of Numeric Features', fontsize=16)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_revenue_by_year(df, save_path):
    """Generates and saves a line plot of total revenue by year."""
    print(f"Generating revenue by year plot -> {save_path}")
    
    yearly_revenue = df.groupby('release_year')['revenue'].sum().reset_index()
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(x='release_year', y='revenue', data=yearly_revenue, marker='o')
    plt.title('Total Movie Revenue by Release Year', fontsize=16)
    plt.xlabel('Release Year', fontsize=12)
    plt.ylabel('Total Revenue', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_vote_average_distribution(df, save_path):
    """Generates and saves a histogram of vote averages."""
    print(f"Generating vote average distribution -> {save_path}")
    plt.figure(figsize=(10, 6))
    sns.histplot(df['vote_average'], kde=True, bins=20, color='green')
    plt.title('Distribution of Vote Average (Rating)', fontsize=16)
    plt.xlabel('Vote Average (0-10)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def plot_runtime_distribution(df, save_path):
    """Generates and saves a histogram of movie runtimes."""
    print(f"Generating runtime distribution -> {save_path}")
    plt.figure(figsize=(10, 6))
    # Filter out extreme outliers for a better plot
    runtime_filtered = df[df['runtime'].between(0, 240)]
    sns.histplot(runtime_filtered['runtime'], kde=True, bins=30, color='purple')
    plt.title('Distribution of Movie Runtime (in minutes)', fontsize=16)
    plt.xlabel('Runtime (minutes)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()
    
# --- Main Execution ---

def main():
    """Main function to run the EDA process."""
    
    # Ensure the plot directory exists
    os.makedirs(PLOT_DIR, exist_ok=True)
    
    # Load data
    try:
        df = pd.read_csv(DATA_FILE)
        print(f"Successfully loaded data from {DATA_FILE} ({df.shape[0]} rows)")
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE}")
        print("Please run the fetching and cleaning scripts first.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # Prepare data for plotting
    df = preprocess_data(df)
    
    # --- Generate All Plots ---
    plot_genre_counts(df, os.path.join(PLOT_DIR, "1_genre_counts.png"))
    plot_revenue_distribution(df, os.path.join(PLOT_DIR, "2_revenue_distribution.png"))
    plot_budget_revenue_scatter(df, os.path.join(PLOT_DIR, "3_budget_revenue_scatter.png"))
    plot_correlation_heatmap(df, os.path.join(PLOT_DIR, "4_correlation_heatmap.png"))
    plot_revenue_by_year(df, os.path.join(PLOT_DIR, "5_revenue_by_year.png"))
    plot_vote_average_distribution(df, os.path.join(PLOT_DIR, "6_vote_average_distribution.png"))
    plot_runtime_distribution(df, os.path.join(PLOT_DIR, "7_runtime_distribution.png"))

    print(f"\n✅ All plots have been generated and saved to the '{PLOT_DIR}' directory.")

if __name__ == "__main__":
    main()