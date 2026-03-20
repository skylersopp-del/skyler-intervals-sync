import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"

history_path = DATA_DIR / "history.json"
notes_path = DATA_DIR / "notes.json"

def load_json(path):
    if not path.exists():
        print(f"Missing file: {path}")
        return None
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"JSON decode error in {path}: {e}")
        return None

def main():
    history = load_json(history_path)
    if not history or not isinstance(history, dict):
        print("history.json not found, empty, or not a dict.")
        return

    # The actual list of daily summaries is under "daily_90d" key
    daily_summaries = history.get("daily_90d", [])
    if not isinstance(daily_summaries, list):
        print("'daily_90d' key missing or not a list in history.json.")
        return

    notes_index = []

    for day in daily_summaries:
        if not isinstance(day, dict):
            print(f"Skipping invalid daily entry (not dict): {day}")
            continue

        # Extract relevant note/comment fields if they exist in daily summaries
        # Adjust keys based on what actually appears in your daily_90d dicts
        entry = {
            "date": day.get("date"),
            "notes": day.get("notes") or day.get("description") or "",
            "icu_notes": day.get("icu_notes", ""),
            "comments": day.get("comments", []),
            "athlete_comments": day.get("athlete_comments", []),
            "coach_comments": day.get("coach_comments", []),
            "activity_count": day.get("activity_count", 0),
            "total_tss": day.get("total_tss", 0.0),
            # Add more fields if useful for your notes index (e.g., feel, soreness)
            "feel": day.get("feel"),
            "soreness": day.get("soreness"),
            "fatigue": day.get("fatigue"),
        }

        # Only append if there's something note-like or activity present
        if entry["activity_count"] > 0 or any(entry.get(k) for k in ["notes", "icu_notes", "comments"]):
            notes_index.append(entry)

    notes_path.write_text(json.dumps(notes_index, indent=2), encoding="utf-8")
    print(f"notes.json index created with {len(notes_index)} entries.")

if __name__ == "__main__":
    main()
