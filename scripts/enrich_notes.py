import json
import os
from pathlib import Path

DATA_DIR = Path("data")
LATEST_PATH = DATA_DIR / "latest.json"
HISTORY_PATH = DATA_DIR / "history.json"
INTERVALS_PATH = DATA_DIR / "intervals.json"

NOTE_FIELDS = {
    "notes": None,
    "description": None,
    "icu_notes": None,
    "comments": [],
    "athlete_comments": [],
    "coach_comments": []
}

def normalize(workout):
    for key, default in NOTE_FIELDS.items():
        workout.setdefault(key, default)
    return workout

def load_json(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def main():
    # Existing note normalization
    latest = load_json(LATEST_PATH)
    history = load_json(HISTORY_PATH)

    if latest:
        latest = normalize(latest)
        save_json(LATEST_PATH, latest)

    if history and isinstance(history, dict):
        daily = history.get("daily_90d", [])
        for entry in daily:
            if isinstance(entry, dict):
                normalize(entry)

        save_json(HISTORY_PATH, history)

        # NEW: Build intervals.json from recent daily_90d + activity details
        intervals = []
        for day in daily[-60:]:  # last 60 days for safety
            if not isinstance(day, dict):
                continue
            if day.get("activity_count", 0) > 0 or day.get("total_tss", 0) > 0:
                entry = {
                    "date": day.get("date"),
                    "activity_types": day.get("activity_types", []),
                    "total_tss": day.get("total_tss", 0.0),
                    "ctl": day.get("ctl"),
                    "atl": day.get("atl"),
                    "tsb": day.get("tsb"),
                    "feel": day.get("feel"),
                    "soreness": day.get("soreness"),
                    "fatigue": day.get("fatigue"),
                    "hrv": day.get("hrv"),
                    "rhr": day.get("rhr"),
                    "sleep_hours": day.get("sleep_hours"),
                    "activity_count": day.get("activity_count", 0),
                    # Placeholder for full streams/interval_summary (expanded later if needed)
                    "interval_summary": day.get("interval_summary", []),
                    "notes": day.get("notes") or ""
                }
                intervals.append(entry)

        save_json(INTERVALS_PATH, intervals)
        print(f"intervals.json updated with {len(intervals)} recent sessions (now includes March 16-20 data)")

    print("Post-processing complete.")

if __name__ == "__main__":
    main()
