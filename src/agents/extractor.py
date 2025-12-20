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
    print("Running Extractor Agent test...")
    # NEW: Computer Science sample text
    sample_text = """
    Machine Learning is a subfield of Artificial Intelligence that gives computers the ability to learn without being explicitly programmed. It is broadly divided into Supervised Learning, which uses labeled data, and Unsupervised Learning, which finds patterns in unlabeled data. A common Supervised Learning algorithm is Linear Regression. Web Development involves creating websites and applications. It consists of Frontend development, which focuses on the user interface using tools like React, and Backend development, which manages the server, database, and application logic using technologies like Node.js.
    """
    concepts = extract_concepts(sample_text)
    print(json.dumps(concepts, indent=2))
