# Daily Research Dashboard

## Quick Start

Run the daily research with:
```
/research
```

This will:
1. Web-search all topics defined in `agent/config.py`
2. Save results to `data/YYYY-MM-DD.json`
3. Generate the dashboard at `site/index.html`
4. Open a local server at http://localhost:8080

## Add Topics

Edit `agent/config.py` and add a new dict to `TOPICS`:
```python
{
    "name": "Your Topic",
    "slug": "your-topic",
    "focus_areas": ["Area 1", "Area 2", "Area 3"],
}
```

## Project Structure

```
agent/config.py      → Topic configuration
agent/publisher.py   → HTML dashboard generator
data/*.json          → Daily research results
site/index.html      → Generated dashboard
```
