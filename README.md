# Daily Research Dashboard

Autonomer Research Agent, der täglich definierte Themen recherchiert und als interaktives Web-Dashboard publiziert.

## Stack

- **Agent**: Python 3.11+ mit [Anthropic Claude API](https://docs.anthropic.com/) + Web Search
- **Dashboard**: Statisches HTML (vanilla CSS/JS), hostbar auf GitHub Pages
- **Scheduling**: GitHub Actions (täglich 06:00 UTC)
- **Daten**: JSON-Files pro Tag (`data/YYYY-MM-DD.json`)

## Setup

```bash
# Abhängigkeiten installieren
pip install -r agent/requirements.txt

# API Key setzen
export ANTHROPIC_API_KEY="sk-ant-..."

# Agent manuell ausführen
python -m agent.researcher
```

Das generierte Dashboard liegt unter `site/index.html`.

## Themen konfigurieren

Themen werden in `agent/config.py` definiert. Neues Thema hinzufügen:

```python
TOPICS.append({
    "name": "ILS & Catastrophe Bonds",
    "slug": "ils-cat-bonds",
    "focus_areas": [
        "Neue Cat Bond Emissionen",
        "Parametrische Versicherung",
        "ILS Fund Performance",
    ],
})
```

## GitHub Actions

Der Workflow `.github/workflows/daily-research.yml` führt den Agent täglich um 06:00 UTC aus. Voraussetzung: `ANTHROPIC_API_KEY` als Repository Secret konfigurieren.

## Architektur

```
agent/researcher.py  →  data/YYYY-MM-DD.json  →  agent/publisher.py  →  site/index.html
     (Claude API)           (Rohdaten)              (HTML Generator)      (Dashboard)
```
