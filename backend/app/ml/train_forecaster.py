import os
import sys
import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error

def train_and_evaluate_forecaster():
    # 1. Locate Data File
    data_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../data/processed/freight_features_processed.csv'))

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Processed dataset not found at {data_path}. Run Phase 5 data pipeline first.")

    df = pd.read_csv(data_path)
    print(f"Loaded dataset with {len(df)} records for training.")

    # 2. Define Features and Target
    feature_cols = [
        'freight_rate_usd_per_ton',
        'bunker_fuel_price_usd',
        'cargo_demand_index',
        'vessel_availability_index',
        'port_congestion_days',
        'rate_lag_1',
        'rate_lag_7',
        'rate_lag_14',
        'rate_roll_7_mean',
        'rate_roll_14_mean',
        'rate_roll_7_std',
        'demand_vessel_ratio',
        'fuel_price_lag_1',
        'month_sin',
        'month_cos'
    ]
    target_col = 'target_rate_30d'

    X = df[feature_cols]
    y = df[target_col]

    # 3. Chronological Time-Series Train/Test Split (80% Train, 20% Test)
    split_idx = int(len(df) * 0.8)
    X_train, X_test = X.iloc[:split_idx], X.iloc[split_idx:]
    y_train, y_test = y.iloc[:split_idx], y.iloc[split_idx:]

    print(f"Training set size: {len(X_train)} | Test set size: {len(X_test)}")

    # 4. Feature Scaling
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 5. Model Candidate Initialization
    models = {
        "Linear Regression (Baseline)": LinearRegression(),
        "Random Forest Regressor": RandomForestRegressor(n_estimators=100, max_depth=8, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=5, random_state=42)
    }

    best_model = None
    best_model_name = ""
    lowest_mae = float("inf")
    model_results = {}

    print("\n--- MODEL EVALUATION METRICS (30-DAY FREIGHT RATE FORECAST) ---")
    for name, model in models.items():
        # Fit model
        if "Linear" in name:
            model.fit(X_train_scaled, y_train)
            preds = model.predict(X_test_scaled)
        else:
            model.fit(X_train, y_train)
            preds = model.predict(X_test)

        mae = mean_absolute_error(y_test, preds)
        rmse = np.sqrt(mean_squared_error(y_test, preds))
        model_results[name] = {"MAE": mae, "RMSE": rmse}

        print(f"Model: {name:<30} | MAE: ${mae:.2f}/ton | RMSE: ${rmse:.2f}/ton")

        if mae < lowest_mae:
            lowest_mae = mae
            best_model_name = name
            best_model = model

    print(f"\nCHAMPION MODEL SELECTED: {best_model_name} (Lowest MAE: ${lowest_mae:.2f}/ton)")

    # 6. Save Champion Model & Scaler Artifacts
    models_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../models'))
    os.makedirs(models_dir, exist_ok=True)

    model_path = os.path.join(models_dir, "forecaster_model.pkl")
    scaler_path = os.path.join(models_dir, "forecaster_scaler.pkl")

    joblib.dump(best_model, model_path)
    joblib.dump(scaler, scaler_path)

    print(f"Saved Champion Model artifact to: {model_path}")
    print(f"Saved Feature Scaler artifact to: {scaler_path}")

if __name__ == "__main__":
    train_and_evaluate_forecaster()