from pathlib import Path
from .load_data import load_all
from .llm import call_model
from .format_output import save_output

ROOT = Path(__file__).resolve().parents[2]
PROMPTS_DIR = ROOT / "coach" / "prompts"

def build_prompt(kind: str, data: dict) -> str:
    prompt_path = PROMPTS_DIR / f"{kind}.txt"
    base = prompt_path.read_text(encoding="utf-8")

    # Simple interpolation: you can make this richer later
    return base.format(
        DOSSIER=data.get("dossier", ""),
        LATEST_JSON=data.get("latest"),
        HISTORY_JSON=data.get("history"),
        INTERVALS_JSON=data.get("intervals"),
    )

def run(kind: str, provider: str, model: str | None = None):
    data = load_all()
    prompt = build_prompt(kind, data)
    response = call_model(prompt, provider=provider, model=model)
    path = save_output(kind, response)
    print(f"{kind} coaching written to {path}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--kind", choices=["daily", "weekly", "analysis", "plan"], required=True)
    parser.add_argument("--provider", choices=["openai", "anthropic", "gemini", "azure"], required=True)
    parser.add_argument("--model", required=False)
    args = parser.parse_args()

    run(args.kind, provider=args.provider, model=args.model)
