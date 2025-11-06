import pandas as pd
import joblib
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn import metrics

# --- Configuration ---
DATA_FILE = "data/cleaned_movies.csv"
MODEL_DIR = "models"
PLOT_DIR = "plots"
BEST_MODEL_FILE = os.path.join(MODEL_DIR, "best_revenue_predictor.joblib")
EVAL_PLOT_FILE = os.path.join(PLOT_DIR, "best_model_evaluation.png")

def load_data(path):
    """Loads and prepares the data for modeling."""
    print(f"Loading data from {path}...")
    df = pd.read_csv(path)
    
    # Define features (X) and target (y)
    features = ['budget', 'vote_count', 'popularity', 'runtime', 'original_language']
    target = 'revenue'
    
    X = df[features]
    y = df[target]
    
    return X, y

def build_preprocessor():
    """Builds the preprocessing pipeline for all models."""
    
    # Define which columns are which type
    numerical_features = ['budget', 'vote_count', 'popularity', 'runtime']
    categorical_features = ['original_language']

    # Create preprocessing steps for each type
    numeric_transformer = Pipeline(steps=[
        ('scaler', StandardScaler())
    ])

    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
    ])

    # Combine transformers into a single preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numerical_features),
            ('cat', categorical_transformer, categorical_features)
        ],
        remainder='passthrough'
    )
    return preprocessor

def plot_evaluation(y_test, y_pred, model_name, save_path):
    """Generates and saves a scatter plot of actual vs. predicted values for the best model."""
    print(f"Generating evaluation plot for {model_name} -> {save_path}")
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=y_test, y=y_pred, alpha=0.5)
    
    # Add a 45-degree reference line
    max_val = max(y_test.max(), y_pred.max())
    min_val = min(y_test.min(), y_pred.min())
    plt.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
    
    plt.title(f'Actual vs. Predicted Revenue ({model_name})', fontsize=16)
    plt.xlabel('Actual Revenue', fontsize=12)
    plt.ylabel('Predicted Revenue', fontsize=12)
    plt.legend()
    plt.savefig(save_path, bbox_inches='tight')
    plt.close()

def main():
    """Main function to run the model training, comparison, and saving process."""
    
    # Ensure output directories exist
    os.makedirs(PLOT_DIR, exist_ok=True)
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    # --- 1. Load Data ---
    try:
        X, y = load_data(DATA_FILE)
    except FileNotFoundError:
        print(f"Error: Data file not found at {DATA_FILE}")
        print("Please run the cleaning script first.")
        return
    except Exception as e:
        print(f"Error loading data: {e}")
        return

    # --- 2. Split Data ---
    print("Splitting data into train and test sets...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # --- 3. Build Pipelines ---
    preprocessor = build_preprocessor()
    
    # Create a dictionary of models to test
    model_pipelines = {
        "Linear Regression": Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', LinearRegression())
        ]),
        "Random Forest": Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', RandomForestRegressor(random_state=42, n_estimators=100))
        ]),
        "XGBoost": Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('regressor', XGBRegressor(random_state=42, n_estimators=100))
        ])
    }
    
    # --- 4. Train and Evaluate All Models ---
    print("\nTraining and evaluating models...")
    results = []
    
    for name, model in model_pipelines.items():
        print(f"  Training {name}...")
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        
        r2 = metrics.r2_score(y_test, y_pred)
        mae = metrics.mean_absolute_error(y_test, y_pred)
        
        results.append({
            "model_name": name,
            "R-squared": r2,
            "MAE": mae,
            "pipeline_object": model  # Store the trained model
        })

    # --- 5. Compare Models and Select Best ---
    results_df = pd.DataFrame(results).sort_values(by="R-squared", ascending=False)
    
    print("\n--- Model Comparison Results ---")
    print(results_df.drop(columns=['pipeline_object']).to_string(index=False))

    best_model_stats = results_df.iloc[0]
    best_model_name = best_model_stats['model_name']
    best_model_pipeline = best_model_stats['pipeline_object']

    print(f"\n🏆 Best model selected: {best_model_name} (R²: {best_model_stats['R-squared']:.3f})")
    
    # --- 6. Save Artifacts for the Best Model ---
    
    # Save the best model
    print(f"Saving best model to {BEST_MODEL_FILE}...")
    joblib.dump(best_model_pipeline, BEST_MODEL_FILE)
    
    # Save the evaluation plot for the best model
    best_y_pred = best_model_pipeline.predict(X_test)
    plot_evaluation(y_test, best_y_pred, best_model_name, EVAL_PLOT_FILE)

    print("\n✅ Model training and selection process complete.")

if __name__ == "__main__":
    main()