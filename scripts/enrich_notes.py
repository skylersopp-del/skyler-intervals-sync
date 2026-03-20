import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
HISTORY_PATH = DATA_DIR / "history.json"
INTERVALS_PATH = DATA_DIR / "intervals.json"
CSV_PATH = DATA_DIR / "activities.csv"

def main():
    print("Enrich start")
    intervals = []

    if INTERVALS_PATH.exists():
        try:
            intervals = json.loads(INTERVALS_PATH.read_text())
            print(f"Loaded {len(intervals)} intervals from sync.py")
        except Exception as e:
            print(f"Failed to load intervals.json: {e}")
    else:
        print("intervals.json not found — starting with empty list")


# ----------------------------------------
# FIX 3: Merge CSV data into existing intervals
# ----------------------------------------

# Build a lookup table for fast merging by date
intervals_by_date = {entry.get("date"): entry for entry in intervals}

if CSV_PATH.exists():
    try:
         df = pd.read_csv(CSV_PATH)
         print(f"CSV rows: {len(df)}")
         print("Columns:", df.columns.tolist())

         for _, row in df.tail(60).iterrows():
            date = row.get("Date")
            if pd.isna(date):
                continue

            # If this workout already exists from Intervals.icu → enrich it
             
            if date in intervals_by_date:
                entry = intervals_by_date[date]
                entry.update({
                    "csv_distance": row.get("Distance"),
                    "csv_moving_time": row.get("Moving Time"),
                    "csv_avg_hr": row.get("Avg HR"),
                    "csv_norm_power": row.get("Norm Power"),
                    "csv_tss": row.get("Load"),
                    "csv_ftp": row.get("FTP"),
                    "csv_weight": row.get("Weight"),
                })
            else:
                # Optional: include CSV-only workouts
                intervals.append({
                    "date": date,
                    "name": row.get("Name"),
                    "source": "csv_only",
                    "csv_distance": row.get("Distance"),
                    "csv_moving_time": row.get("Moving Time"),
                    "csv_avg_hr": row.get("Avg HR"),
                    "csv_norm_power": row.get("Norm Power"),
                    "csv_tss": row.get("Load"),
                    "csv_ftp": row.get("FTP"),
                    "csv_weight": row.get("Weight"),
                })

    except Exception as e:
        print(f"CSV load failed: {e}")
else:
    print("activities.csv not found")

    # Merge history if available
    history = None
    if HISTORY_PATH.exists():
        history = json.loads(HISTORY_PATH.read_text())
        daily = history.get("daily_90d", [])
        for entry in intervals:
            date_str = entry["date"]
            match = next((d for d in daily if d.get("date") == date_str), None)
            if match:
                entry["ctl"] = match.get("ctl")
                entry["atl"] = match.get("atl")
                entry["tsb"] = match.get("tsb")
                # add more fields as needed

    save_json(INTERVALS_PATH, intervals)
    print(f"intervals.json saved with {len(intervals)} non-null entries")

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

if __name__ == "__main__":
    main()
