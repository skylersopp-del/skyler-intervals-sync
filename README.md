# skyler-intervals-sync

API key hardcoded for personal private use only — **do not share repo.**


# Skyler’s Section‑11 Automated Coaching System

This repository implements a fully automated, Section‑11‑compliant endurance coaching system built on top of Intervals.icu data. It synchronizes workouts, enriches notes, generates coaching reports using any LLM provider, and stores all outputs directly in the repository.

The system is designed to be:
- **Model‑agnostic** (OpenAI, Anthropic, Gemini, Azure, etc.)
- **Fully automated** (via GitHub Actions)
- **Section‑11 compliant**
- **Extensible and transparent**
- **Readable by any LLM (Copilot, Claude, GPT‑4, Gemini, etc.)**

---

## 📌 System Overview

### **1. Data Sync (Every 4 Hours)**
The workflow pulls:
- `latest.json` — most recent workout  
- `history.json` — full workout history  
- `intervals.json` — athlete profile  

Then a post‑processing step enriches:
- notes  
- comments  
- descriptions  
- coach/athlete chat  

This ensures a consistent schema for all coaching prompts.

---

### **2. Coaching Engine (Daily / Weekly / Sunday Block)**
The coaching engine runs automatically and generates:

| Day | Output |
|-----|--------|
| Every day | `coach/outputs/daily.md` |
| Monday | `coach/outputs/weekly.md` |
| Sunday | `coach/outputs/analysis.md` + `coach/outputs/plan.md` |

The engine uses:
- `coach/prompts/*.txt`  
- `coach/DOSSIER.md`  
- `data/*.json`  
- `coach/engine/*.py`  

Outputs are committed back into the repo.

---

## 📁 Repository Structure
data/ 
  latest.json 
  history.json 
  intervals.json 
  notes.json
coach/ 
  DOSSIER.md 
    prompts/ 
      daily.txt 
      weekly.txt 
      analysis.txt 
      plan.txt 
    templates/ 
      daily_output.md 
      weekly_output.md 
      analysis_output.md 
      plan_output.md 
    engine/ 
      run_coach.py 
        load_data.py 
        format_output.py 
        llm.py 
      providers/ 
        openai_provider.py
        anthropic_provider.py
        gemini_provider.py
        azure_provider.py
      outputs/
        daily.md 
        weekly.md
        analysis.md
        plan.md
        
---

## ⚙️ LLM Provider Support

The system supports multiple providers out of the box:

- OpenAI  
- Anthropic  
- Google Gemini  
- Azure OpenAI  

You can switch providers by changing the GitHub Action environment variables or by running:
  python coach/engine/run_coach.py --kind daily --provider openai --model gpt-4.1-mini


---

## 🧠 How to Use This Repo with Any LLM

Any LLM (Copilot, Claude, GPT‑4, Gemini, etc.) can:

- Read your dossier  
- Read your synced data  
- Read your coaching outputs  
- Help interpret or extend the coaching  
- Generate new plans or insights  

This makes the repo a **universal coaching backend**.

---

## 🛠️ GitHub Actions

Two workflows power the system:

### **1. Sync Intervals.icu Data**
Runs every 4 hours  
Updates `data/*.json`

### **2. Run AI Coach**
Runs:
- Daily coaching (every morning)
- Weekly summary (Monday)
- Analysis + planning (Sunday)

Outputs saved to `coach/outputs/`.

---

## 📄 License
This repository is for personal use and experimentation with Section‑11‑style coaching workflows.

