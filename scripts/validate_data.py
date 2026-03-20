import json
from pathlib import Path

DATA_DIR = Path("data")

FILES = {
    "full_workouts.json": DATA_DIR / "full_workouts.json",
    "latest.json": DATA_DIR / "latest.json",
    "intervals.json": DATA_DIR / "intervals.json",
    "history.json": DATA_DIR / "history.json",
    "notes.json": DATA_DIR / "notes.json",
}

def validate_json(path: Path, name: str):
    if not path.exists():
        raise ValueError(f"{name} is missing")

    if path.stat().st_size == 0:
        raise ValueError(f"{name} is empty")

    try:
        data = json.loads(path.read_text())
    except Exception as e:
        raise ValueError(f"{name} is invalid JSON: {e}")

    if isinstance(data, list) and len(data) == 0:
        raise ValueError(f"{name} contains an empty list")

    if isinstance(data, dict) and len(data.keys()) == 0:
        raise ValueError(f"{name} contains an empty object")

    print(f"{name} validated successfully")
    return data


def main():
    print("=== Data Validation Start ===")

    for name, path in FILES.items():
        try:
            validate_json(path, name)
        except Exception as e:
            print(f"Validation failed for {name}: {e}")
            raise SystemExit(1)

    print("All data files validated successfully")


if __name__ == "__main__":
    main()
