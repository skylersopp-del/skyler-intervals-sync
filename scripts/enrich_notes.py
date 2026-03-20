import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
HISTORY_PATH = DATA_DIR / "history.json"
INTERVALS_PATH = DATA_DIR / "intervals.json"
ACTIVITIES_CSV = DATA_DIR / "activities.csv"

def load_json(path):
    if not path.exists():
        print(f"{path} missing")
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    history = load_json(HISTORY_PATH)

    # Debug CSV load
    if ACTIVITIES_CSV.exists():
        try:
            df = pd.read_csv(ACTIVITIES_CSV)
            print(f"CSV loaded with {len(df)} rows")
            print(df.tail(5))  # show recent
        except Exception as e:
            print(f"CSV error: {e}")
            df = pd.DataFrame()
    else:
        print("activities.csv missing")
        df = pd.DataFrame()

    intervals = []
    if not df.empty:
        for _, row in df.tail(60).iterrows():
            if pd.isna(row.get("Date")) or pd.isna(row.get("Name")):
                continue  # skip invalid rows
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
                "interval_summary": [],  # expand if streams in CSV
                "notes": row.get("Name") or "",
                "ctl": None,
                "atl": None,
                "tsb": None
            }
            intervals.append(entry)
    else:
        print("No valid CSV data - skipping intervals append")

    # Merge history daily
    if history and isinstance(history, dict):
        daily = history.get("daily_90d", [])
        for entry in intervals:
            date_str = entry["date"]
            match = next((d for d in daily if d.get("date") == date_str), None)
            if match:
                entry.update({
                    "ctl": match.get("ctl"),
                    "atl": match.get("atl"),
                    "tsb": match.get("tsb"),
                    "feel": match.get("feel"),
                    "soreness": match.get("soreness"),
                    "fatigue": match.get("fatigue"),
                    "hrv": match.get("hrv"),
                    "rhr": match.get("rhr")
                })

    save_json(INTERVALS_PATH, intervals)
    print(f"intervals.json saved with {len(intervals)} entries (filtered non-null)")

    print("Enrich complete.")

if __name__ == "__main__":
    main()
