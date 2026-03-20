import json
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data")
HISTORY_PATH = DATA_DIR / "history.json"
INTERVALS_PATH = DATA_DIR / "intervals.json"
LATEST_PATH = DATA_DIR / "latest.json"
CSV_PATH = DATA_DIR / "activities.csv"
FULL_WORKOUTS_PATH = DATA_DIR / "full_workouts.json"


def main():
    print("=== Enrich Start ===")

    # ----------------------------------------
    # Load full workouts (the biggest data dump)
    # ----------------------------------------
    full_workouts = []
    if FULL_WORKOUTS_PATH.exists():
        try:
            full_workouts = json.loads(FULL_WORKOUTS_PATH.read_text())
            print(f"Loaded {len(full_workouts)} full workouts from full_workouts.json")
        except Exception as e:
            print(f"Failed to load full_workouts.json: {e}")
    else:
        print("full_workouts.json not found — cannot build intervals.json or latest.json")

    # ----------------------------------------
    # Build intervals.json from full workouts
    # ----------------------------------------
    intervals = []
    for w in full_workouts:
        entry = {
            "id": w.get("id"),
            "date": w.get("start_date_local") or w.get("start_date"),
            "name": w.get("name"),
            "type": w.get("type"),
            "duration": w.get("duration"),
            "distance": w.get("distance"),
            "avg_hr": w.get("avg_hr"),
            "max_hr": w.get("max_hr"),
            "power": w.get("power"),
            "cadence": w.get("cadence"),
            "pace": w.get("pace"),
            "tss": w.get("tss"),
            "ftp": w.get("ftp"),
            "notes": w.get("notes"),
            "laps": w.get("laps"),
            "splits": w.get("splits"),
            "intervals": w.get("intervals"),
            "equipment": w.get("equipment"),
            "tags": w.get("tags"),
            "route": w.get("route"),
        }
        intervals.append(entry)

    print(f"Built intervals.json with {len(intervals)} workouts from full data")

    # ----------------------------------------
    # Merge CSV data into intervals
    # ----------------------------------------
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
                    new_entry = {
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
                    }
                    intervals.append(new_entry)
                    intervals_by_date[date] = new_entry

        except Exception as e:
            print(f"CSV load failed: {e}")
    else:
        print("activities.csv not found")

    # ----------------------------------------
    # Merge history (CTL/ATL/TSB)
    # ----------------------------------------
    if HISTORY_PATH.exists():
        try:
            history = json.loads(HISTORY_PATH.read_text())
            daily = history.get("daily_90d", [])
            for entry in intervals:
                date_str = entry.get("date")
                if not date_str:
                    continue
                match = next((d for d in daily if d.get("date") == date_str), None)
                if match:
                    entry["ctl"] = match.get("ctl")
                    entry["atl"] = match.get("atl")
                    entry["tsb"] = match.get("tsb")
        except Exception as e:
            print(f"History merge failed: {e}")

    # ----------------------------------------
    # Build latest.json from the most recent 5 workouts
    # ----------------------------------------
    latest = sorted(full_workouts, key=lambda w: w.get("start_time", ""), reverse=True)[:5]
    save_json(LATEST_PATH, latest)
    print(f"latest.json saved with {len(latest)} workouts")

    # ----------------------------------------
    # FIX 4: Prevent overwriting with empty intervals
    # ----------------------------------------
    if len(intervals) == 0:
        print("No intervals found — NOT overwriting intervals.json")
        return

    # ----------------------------------------
    # FIX 5A: Backup existing intervals.json
    # ----------------------------------------
    backup_path = DATA_DIR / "intervals_backup.json"
    if INTERVALS_PATH.exists():
        INTERVALS_PATH.replace(backup_path)
        print("Backed up previous intervals.json")

    # Save new intervals.json
    save_json(INTERVALS_PATH, intervals)

    # ----------------------------------------
    # FIX 5B: Validate new intervals.json
    # ----------------------------------------
    try:
        new_data = json.loads(INTERVALS_PATH.read_text())
        if not isinstance(new_data, list) or len(new_data) == 0:
            raise ValueError("New intervals.json is empty or invalid")
    except Exception as e:
        print(f"Validation failed: {e}")
        if backup_path.exists():
            print("Restoring backup intervals.json")
            backup_path.replace(INTERVALS_PATH)
    else:
        print("intervals.json validated successfully")


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
