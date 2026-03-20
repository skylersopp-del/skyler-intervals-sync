import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
LATEST_PATH = DATA_DIR / "latest.json"
HISTORY_PATH = DATA_DIR / "history.json"
INTERVALS_PATH = DATA_DIR / "intervals.json"
ACTIVITIES_CSV = DATA_DIR / "activities.csv"

def load_json(path):
    if not path.exists(): return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    history = load_json(HISTORY_PATH)
    latest = load_json(LATEST_PATH)

    # Existing note normalization
    if latest: save_json(LATEST_PATH, latest)

    # NEW: Detailed intervals.json from activities.csv + history daily_90d
    intervals = []
    if ACTIVITIES_CSV.exists():
        df = pd.read_csv(ACTIVITIES_CSV)
        for _, row in df.tail(60).iterrows():  # last 60 days
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
                "interval_summary": [],  # placeholder; expand later if streams added
                "notes": row.get("Name") or "",
                "ctl": None,
                "atl": None,
                "tsb": None
            }
            intervals.append(entry)

    # Merge history daily wellness/CTL for extra context
    if history and isinstance(history, dict):
        daily = history.get("daily_90d", [])
        for entry in intervals:
            date_match = next((d for d in daily if d.get("date") == entry["date"]), None)
            if date_match:
                entry.update({
                    "ctl": date_match.get("ctl"),
                    "atl": date_match.get("atl"),
                    "tsb": date_match.get("tsb"),
                    "feel": date_match.get("feel"),
                    "soreness": date_match.get("soreness"),
                    "fatigue": date_match.get("fatigue"),
                    "hrv": date_match.get("hrv"),
                    "rhr": date_match.get("rhr")
                })

    save_json(INTERVALS_PATH, intervals)
    print(f"intervals.json updated with {len(intervals)} detailed sessions (streams + wellness merged)")

    print("Post-processing complete.")

if __name__ == "__main__":
    main()
