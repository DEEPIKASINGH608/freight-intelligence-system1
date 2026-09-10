import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor


def calculate_directional_accuracy(y_true, y_pred, y_spot):
    """
    Calculates the percentage of times the model correctly predicted
    the DIRECTION of price movement (UP or DOWN relative to current spot).
    """
    true_direction = np.sign(y_true - y_spot)
    pred_direction = np.sign(y_pred - y_spot)

    # Exclude instances where no movement occurred to prevent division by zero
    valid_mask = true_direction != 0
    if not np.any(valid_mask):
        return 0.0

    correct_directions = (true_direction[valid_mask] == pred_direction[valid_mask])
    return float(np.mean(correct_directions) * 100)


def walk_forward_backtest(df: pd.DataFrame, n_splits: int = 5):
    """
    Performs Walk-Forward Backtesting across multiple rolling time windows.
    Assumes df contains columns: ['current_spot', 'actual_future', 'feature_1', 'feature_2', ...]
    """
    feature_cols = [c for c in df.columns if c not in ['current_spot', 'actual_future']]

    X = df[feature_cols].values
    y = df['actual_future'].values
    y_spot = df['current_spot'].values

    tscv = TimeSeriesSplit(n_splits=n_splits)

    models = {
        "Naïve Persistence": None,
        "Linear Regression": LinearRegression(),
        "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
        "XGBoost Regressor": XGBRegressor(n_estimators=100, learning_rate=0.05, random_state=42)
    }

    metrics_store = {model_name: {"mae": [], "rmse": [], "mape": [], "dir_acc": []} for model_name in models}

    # Walk-forward cross-validation loop
    for fold, (train_index, test_index) in enumerate(tscv.split(X), 1):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]
        y_test_spot = y_spot[test_index]

        for name, model in models.items():
            if name == "Naïve Persistence":
                # Naive prediction assumes future rate = current spot
                preds = y_test_spot
            else:
                model.fit(X_train, y_train)
                preds = model.predict(X_test)

            mae = mean_absolute_error(y_test, preds)
            rmse = np.sqrt(mean_squared_error(y_test, preds))
            mape = mean_absolute_percentage_error(y_test, preds) * 100
            dir_acc = calculate_directional_accuracy(y_test, preds, y_test_spot)

            metrics_store[name]["mae"].append(mae)
            metrics_store[name]["rmse"].append(rmse)
            metrics_store[name]["mape"].append(mape)
            metrics_store[name]["dir_acc"].append(dir_acc)

    # Compile aggregated cross-window results
    summary_results = []
    for name in models:
        summary_results.append({
            "Model": name,
            "Mean MAE ($/ton)": round(np.mean(metrics_store[name]["mae"]), 2),
            "Mean RMSE ($/ton)": round(np.mean(metrics_store[name]["rmse"]), 2),
            "Mean MAPE (%)": f"{round(np.mean(metrics_store[name]['mape']), 2)}%",
            "Directional Accuracy": f"{round(np.mean(metrics_store[name]['dir_acc']), 1)}%"
        })

    eval_df = pd.DataFrame(summary_results)
    print(f"\n================ WALK-FORWARD BACKTESTING SUMMARY ({n_splits} Windows) ================")
    print(eval_df.to_string(index=False))
    print("===============================================================================\n")

    return eval_df


if __name__ == "__main__":
    # Generate synthetic time-series data for demonstration
    np.random.seed(42)
    n_samples = 300

    spots = np.linspace(20, 30, n_samples) + np.sin(np.linspace(0, 10, n_samples)) * 2
    futures = spots + np.random.uniform(-1.5, 2.5, n_samples)
    f1 = spots * 0.8 + np.random.normal(0, 1, n_samples)
    f2 = np.random.uniform(500, 700, n_samples)  # e.g. bunker fuel price

    synthetic_df = pd.DataFrame({
        'current_spot': spots,
        'actual_future': futures,
        'feature_bunker_fuel': f2,
        'feature_index': f1
    })

    walk_forward_backtest(synthetic_df, n_splits=5)