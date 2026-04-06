"""Daily Research Agent – uses Claude API with web search to research topics."""

import json
import re
import sys
from datetime import date, datetime

import anthropic

from agent.config import DATA_DIR, MODEL, TOPICS

SYSTEM_PROMPT = """\
Du bist ein Senior Research-Analyst für institutionelle Investoren.
Deine Aufgabe ist es, die wichtigsten Entwicklungen der letzten 24 Stunden
zu einem gegebenen Thema zu recherchieren und strukturiert zusammenzufassen.

Nutze die Web-Suche aktiv, um aktuelle, verifizierte Informationen zu finden.
Verwende nur echte Quellen mit URLs – erfinde keine Informationen.

Antworte ausschließlich mit validem JSON (kein Markdown, keine Erklärungen).
"""

TOPIC_PROMPT_TEMPLATE = """\
Recherchiere die wichtigsten Entwicklungen der letzten 24 Stunden zum Thema:
**{name}**

Fokus-Bereiche:
{focus_areas}

Liefere dein Ergebnis als JSON mit exakt diesem Schema:
{{
  "topic": "{name}",
  "headline": "Wichtigste Entwicklung in einem Satz",
  "summary": "3-5 Sätze Executive Summary",
  "developments": [
    {{
      "title": "Titel der Entwicklung",
      "description": "2-3 Sätze Beschreibung",
      "source": "Quellenname",
      "url": "https://...",
      "relevance": "high|medium|low",
      "tags": ["tag1", "tag2"]
    }}
  ],
  "market_signals": ["Signal 1", "Signal 2"],
  "outlook": "1-2 Sätze Einschätzung"
}}

Antworte NUR mit dem JSON, kein Markdown-Codeblock.\
"""

MAX_TOOL_LOOP_ITERATIONS = 20


def _parse_json_from_text(text: str) -> dict:
    """Extract JSON from Claude's text response, handling markdown fences."""
    # Strip markdown code fences if present
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip())
    cleaned = re.sub(r"\s*```$", "", cleaned)

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # Regex fallback: find outermost { ... }
        match = re.search(r"\{.*\}", cleaned, re.DOTALL)
        if match:
            return json.loads(match.group())
        raise ValueError(f"Could not parse JSON from response:\n{text[:500]}")


def research_topic(client: anthropic.Anthropic, topic: dict) -> dict:
    """Research a single topic via Claude API with web search."""
    focus_list = "\n".join(f"- {area}" for area in topic["focus_areas"])
    user_message = TOPIC_PROMPT_TEMPLATE.format(
        name=topic["name"], focus_areas=focus_list
    )

    messages = [{"role": "user", "content": user_message}]
    tools = [{"type": "web_search_20250305", "name": "web_search", "max_uses": 10}]

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        tools=tools,
        messages=messages,
    )

    # Handle tool-use loop (web search may require multiple rounds)
    iterations = 0
    while response.stop_reason == "tool_use" and iterations < MAX_TOOL_LOOP_ITERATIONS:
        iterations += 1

        # Build tool results for each tool_use block
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                tool_results.append(
                    {
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": "Search completed.",
                    }
                )

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})

        response = client.messages.create(
            model=MODEL,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            tools=tools,
            messages=messages,
        )

    # Extract text from final response
    text_parts = [block.text for block in response.content if block.type == "text"]
    full_text = "\n".join(text_parts)

    return _parse_json_from_text(full_text)


def run_daily_research() -> str:
    """Run research for all topics and save results as JSON."""
    today = date.today().isoformat()
    print(f"[{datetime.now().isoformat()}] Starting daily research for {today}")

    client = anthropic.Anthropic()
    results = {
        "date": today,
        "generated_at": datetime.now().isoformat(),
        "topics": [],
    }

    for topic in TOPICS:
        print(f"  Researching: {topic['name']} ...")
        try:
            result = research_topic(client, topic)
            results["topics"].append(result)
            print(f"  \u2713 {topic['name']} \u2013 {len(result.get('developments', []))} developments")
        except Exception as e:
            print(f"  \u2717 {topic['name']} failed: {e}", file=sys.stderr)
            results["topics"].append(
                {
                    "topic": topic["name"],
                    "headline": "Research fehlgeschlagen",
                    "summary": f"Fehler bei der Recherche: {e}",
                    "developments": [],
                    "market_signals": [],
                    "outlook": "Keine Daten verfügbar.",
                }
            )

    # Write JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    output_path = DATA_DIR / f"{today}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"[{datetime.now().isoformat()}] Results saved to {output_path}")
    return str(output_path)


if __name__ == "__main__":
    from agent.publisher import publish

    data_path = run_daily_research()
    publish(data_path)
    print("Done.")
