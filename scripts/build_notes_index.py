import json
from pathlib import Path

DATA_DIR = Path("data")
INTERVALS_PATH = DATA_DIR / "intervals.json"
NOTES_INDEX_PATH = DATA_DIR / "notes.json"
BACKUP_PATH = DATA_DIR / "notes_backup.json"


def main():
    print("=== Build Notes Index Start ===")

    # ----------------------------------------
    # Load intervals.json (full enriched workouts)
    # ----------------------------------------
    if not INTERVALS_PATH.exists():
        print("intervals.json missing — cannot build notes index")
        return

    try:
        intervals = json.loads(INTERVALS_PATH.read_text())
        print(f"Loaded {len(intervals)} workouts from intervals.json")
    except Exception as e:
        print(f"Failed to load intervals.json: {e}")
        return

    # ----------------------------------------
    # Build notes index
    # ----------------------------------------
    notes_index = []

    for w in intervals:
        note_text = w.get("notes") or ""
        if not note_text.strip():
            continue

        entry = {
            "id": w.get("id"),
            "date": w.get("date"),
            "name": w.get("name"),
            "type": w.get("type"),
            "notes": note_text.strip(),
            "tss": w.get("tss"),
            "ctl": w.get("ctl"),
            "atl": w.get("atl"),
            "tsb": w.get("tsb"),
        }
        notes_index.append(entry)

    print(f"Built notes index with {len(notes_index)} entries")

    # ----------------------------------------
    # Prevent overwriting with empty data
    # ----------------------------------------
    if len(notes_index) == 0:
        print("Notes index is empty — NOT overwriting notes.json")
        return

    # ----------------------------------------
    # Backup existing notes.json
    # ----------------------------------------
    if NOTES_INDEX_PATH.exists():
        NOTES_INDEX_PATH.replace(BACKUP_PATH)
        print("Backed up previous notes.json")

    # Save new notes.json
    save_json(NOTES_INDEX_PATH, notes_index)

    # ----------------------------------------
    # Validate new notes.json
    # ----------------------------------------
    try:
        new_data = json.loads(NOTES_INDEX_PATH.read_text())
        if not isinstance(new_data, list) or len(new_data) == 0:
            raise ValueError("New notes.json is empty or invalid")
    except Exception as e:
        print(f"Validation failed: {e}")
        if BACKUP_PATH.exists():
            print("Restoring backup notes.json")
            BACKUP_PATH.replace(NOTES_INDEX_PATH)
    else:
        print("notes.json validated successfully")


def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


if __name__ == "__main__":
    main()
