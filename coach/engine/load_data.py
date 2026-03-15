import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
COACH_DIR = ROOT / "coach"

def load_json(name: str):
    path = DATA_DIR / name
    if not path.exists():
        return None
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)

def load_text(path: Path):
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def load_all():
    latest = load_json("latest.json")
    history = load_json("history.json")
    intervals = load_json("intervals.json")
    dossier = load_text(COACH_DIR / "DOSSIER.md")
    return {
        "latest": latest,
        "history": history,
        "intervals": intervals,
        "dossier": dossier,
    }
