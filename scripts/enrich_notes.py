import json
import os

LATEST = "latest.json"
HISTORY = "history.json"

# Fields we want to guarantee exist
NOTE_FIELDS = {
    "notes": None,
    "description": None,
    "icu_notes": None,
    "comments": [],
    "athlete_comments": [],
    "coach_comments": []
}

def normalize(workout):
    """Ensure all note/comment fields exist."""
    for key, default in NOTE_FIELDS.items():
        workout.setdefault(key, default)
    return workout

def load_json(path):
    if not os.path.exists(path):
        return None
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def main():
    latest = load_json(LATEST)
    history = load_json(HISTORY)

    if latest:
        latest = normalize(latest)
        save_json(LATEST, latest)

    if history:
        # history is a list of entries
        for entry in history:
            # Only merge if IDs match
            if latest and entry.get("id") == latest.get("id"):
                for key in NOTE_FIELDS:
                    entry[key] = latest.get(key)
        save_json(HISTORY, history)

    print("Post-processing complete.")

if __name__ == "__main__":
    main()
