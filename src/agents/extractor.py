import json
import re

from src.utils.llm_client import call_gemini_api
import src.utils.llm_client as llm

print("LLM CLIENT FILE PATH:", llm.__file__)


def _extract_json_array(text: str) -> str | None:
    """
    Extracts the first JSON array found in a string.
    """
    match = re.search(r"\[[\s\S]*\]", text)
    if match:
        return match.group(0)
    return None


def extract_concepts(text: str) -> list:
    """
    Extracts key educational concepts using Gemini (AI Studio).
    Returns a validated list of structured concepts.
    """

    prompt = f"""
You are an information extraction agent.

TASK:
Extract the key educational concepts from the text below.

RULES:
- Return ONLY valid JSON
- Do NOT include explanations
- Do NOT include markdown
- Each concept must be an object with:
  - concept (string)
  - type (definition | process | principle | term)
  - importance (float between 0 and 1)

OUTPUT FORMAT:
[
  {{
    "concept": "Photosynthesis",
    "type": "process",
    "importance": 0.95
  }}
]

TEXT:
{text}
"""
    raw_text = call_gemini_api(prompt)

    if not raw_text:
        print("Failed to get a response from the API.")
        return []

    try:
        json_str = _extract_json_array(raw_text)
        if not json_str:
            raise ValueError("No JSON array found in model output.")

        concepts = json.loads(json_str)

        validated = []
        for c in concepts:
            if (
                isinstance(c, dict)
                and isinstance(c.get("concept"), str)
                and c.get("type") in {"definition", "process", "principle", "term"}
                and isinstance(c.get("importance"), (int, float))
                and 0 <= c["importance"] <= 1
            ):
                validated.append(c)

        return validated

    except Exception as e:
        print("Extractor parsing failed:", e)
        print("Raw model output:\n", raw_text)
        return []


if __name__ == "__main__":
    sample_text = """
    Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy.
    Cellular respiration allows organisms to extract energy from food using oxygen. It involves glycolysis, the Krebs cycle, and the electron transport chain.
    Newton's First Law of Motion states that an object at rest stays at rest and an object in motion stays in motion unless acted upon by an external force.
    """

    print("Running Extractor Agent test...")
    concepts = extract_concepts(sample_text)
    print(json.dumps(concepts, indent=2))
