import sys
import os
import numpy as np
import pandas as pd

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from app.database.session import SessionLocal
from app.models.freight_rate import FreightRate

def run_data_pipeline():
    print("Extracting raw freight observations from PostgreSQL...")
    db = SessionLocal()

    try:
        # Query historical data
        query = db.query(FreightRate).order_by(FreightRate.date.asc())
        df = pd.read_sql(query.statement, db.bind)

        if df.empty:
            print("No data found in PostgreSQL! Please run scripts/seed_database.py first.")
            return

        print(f"Loaded {len(df)} historical observations from Database.")

        # Ensure correct datatypes
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)

        print("Constructing engineered time-series features...")

        # 1. Target Variable: Future Freight Rate in 30 days
        df['target_rate_30d'] = df['freight_rate_usd_per_ton'].shift(-30)

        # 2. Lag Features
        df['rate_lag_1'] = df['freight_rate_usd_per_ton'].shift(1)
        df['rate_lag_7'] = df['freight_rate_usd_per_ton'].shift(7)
        df['rate_lag_14'] = df['freight_rate_usd_per_ton'].shift(14)

        # 3. Rolling Moving Averages & Volatility
        df['rate_roll_7_mean'] = df['freight_rate_usd_per_ton'].rolling(window=7).mean()
        df['rate_roll_14_mean'] = df['freight_rate_usd_per_ton'].rolling(window=14).mean()
        df['rate_roll_7_std'] = df['freight_rate_usd_per_ton'].rolling(window=7).std()

        # 4. Domain Metrics
        df['demand_vessel_ratio'] = df['cargo_demand_index'] / (df['vessel_availability_index'] + 1e-5)
        df['fuel_price_lag_1'] = df['bunker_fuel_price_usd'].shift(1)

        # 5. Cyclical Seasonality Features
        df['month'] = df['date'].dt.month
        df['month_sin'] = np.sin(2 * np.pi * df['month'] / 12.0)
        df['month_cos'] = np.cos(2 * np.pi * df['month'] / 12.0)

        # Drop rows with NaN caused by lagging/shifting
        df_clean = df.dropna().reset_index(drop=True)

        print(f"Dataset preprocessed successfully. Final usable rows: {len(df_clean)}")

        # Define file save paths
        raw_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/raw/historical_freight_raw.csv'))
        processed_csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/processed/freight_features_processed.csv'))

        # Save outputs
        df.to_csv(raw_csv_path, index=False)
        df_clean.to_csv(processed_csv_path, index=False)

        print(f"Raw data saved to: {raw_csv_path}")
        print(f"Processed dataset saved to: {processed_csv_path}")

    except Exception as e:
        print(f"Data Pipeline Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    run_data_pipeline()