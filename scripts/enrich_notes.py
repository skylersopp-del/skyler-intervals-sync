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

    # Debug CSV
    if CSV_PATH.exists():
        try:
            df = pd.read_csv(CSV_PATH)
            print(f"CSV rows: {len(df)}")
            print("Columns:", df.columns.tolist())
            print("Tail 5 rows:\n", df.tail(5).to_string())
            for _, row in df.tail(60).iterrows():
                if pd.isna(row.get("Date")) or pd.isna(row.get("Name")):
                    continue
                entry = {
                    "date": row.get("Date"),
                    "name": row.get("Name"),
                    "type": row.get("Type"),
                    "distance": row.get("Distance"),
                    "moving_time": row.get("Moving Time"),
                    "avg_hr": row.get("Avg HR"),
                    "norm_power": row.get("Norm Power"),
                    "tss": row.get("Load"),
                    "ftp": row.get("FTP"),
                    "weight": row.get("Weight"),
                    "w_prime": row.get("W'"),
                    "interval_summary": [],
                    "notes": row.get("Name") or "",
                    "ctl": None,
                    "atl": None,
                    "tsb": None
                }
                intervals.append(entry)
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
