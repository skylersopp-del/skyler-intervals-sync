from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COACH_DIR = ROOT / "coach"
OUTPUT_DIR = ROOT / "coach" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def save_output(kind: str, content: str):
    OUTPUT_DIR.mkdir(exist_ok=True)
    path = OUTPUT_DIR / f"{kind}.md"
    path.write_text(content, encoding="utf-8")
    return path
