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
    return json.loads(path.read_text(encoding="utf-8"))

def main():
    history = load_json(history_path)
    if not history:
        print("No history.json found or empty.")
        return

    notes_index = []

    for w in history:
        entry = {
            "id": w.get("id"),
            "date": w.get("start_date_local"),
            "notes": w.get("notes"),
            "description": w.get("description"),
            "icu_notes": w.get("icu_notes"),
            "comments": w.get("comments", []),
            "athlete_comments": w.get("athlete_comments", []),
            "coach_comments": w.get("coach_comments", []),
        }
        notes_index.append(entry)

    notes_path.write_text(json.dumps(notes_index, indent=2), encoding="utf-8")
    print(f"notes.json index created with {len(notes_index)} entries.")

if __name__ == "__main__":
    main()
