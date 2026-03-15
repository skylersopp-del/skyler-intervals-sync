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

