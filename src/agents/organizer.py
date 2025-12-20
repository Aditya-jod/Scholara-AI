import json
import re
from src.utils.llm_client import call_gemini_api

def _extract_json_object(text: str) -> str | None:
    """
    Extracts the first JSON object found in a string.
    Searches for content between the first '{' and the last '}'.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return None

def organize_concepts(concepts: list) -> dict:
    """
    Takes a flat list of concepts and organizes them into a hierarchical
    tree structure using an LLM.
    """
    concept_names = [c["concept"] for c in concepts]
    
    prompt = f"""
You are a Knowledge Architect. Your task is to organize a given list of concepts into a hierarchical tree structure.
The main, most general concepts should be at the top level, and more specific concepts should be nested as their children.

RULES:
- The final output must be a SINGLE JSON object.
- The root of the object should be named "concept_map".
- "concept_map" should be a list of root-level concept nodes.
- Each node in the tree must be an object with two keys: "concept" (the string name) and "children" (a list of child nodes).
- If a concept has no children, its "children" list should be empty.
- Every single concept from the input list must be placed somewhere in the tree.

EXAMPLE OUTPUT STRUCTURE:
{{
  "concept_map": [
    {{
      "concept": "Main Topic A",
      "children": [
        {{
          "concept": "Sub-topic A.1",
          "children": []
        }}
      ]
    }},
    {{
      "concept": "Main Topic B",
      "children": []
    }}
  ]
}}

Here is the list of concepts to organize:
{json.dumps(concept_names, indent=2)}

Now, generate the JSON object representing the concept map.
"""

    try:
        raw_response = call_gemini_api(prompt)
        json_str = _extract_json_object(raw_response)
        if not json_str:
            print("Organizer Error: No JSON object found in the response.")
            print("Raw model output:\n", raw_response)
            return {}
            
        organized_map = json.loads(json_str)
        return organized_map

    except (json.JSONDecodeError, Exception) as e:
        print(f"Organizer failed to parse response: {e}")
        if 'raw_response' in locals():
            print("Raw model output:\n", raw_response)
        return {}

if __name__ == '__main__':
    # NEW: Plausible Extractor output for the CS text
    sample_extractor_output = [
        {"concept": "Machine Learning", "type": "process", "importance": 0.95},
        {"concept": "Artificial Intelligence", "type": "term", "importance": 0.9},
        {"concept": "Supervised Learning", "type": "process", "importance": 0.85},
        {"concept": "Unsupervised Learning", "type": "process", "importance": 0.85},
        {"concept": "Linear Regression", "type": "term", "importance": 0.7},
        {"concept": "Web Development", "type": "process", "importance": 0.95},
        {"concept": "Frontend development", "type": "term", "importance": 0.8},
        {"concept": "Backend development", "type": "term", "importance": 0.8},
        {"concept": "React", "type": "term", "importance": 0.75},
        {"concept": "Node.js", "type": "term", "importance": 0.75}
    ]

    print("Running Organizer Agent test...")
    hierarchical_map = organize_concepts(sample_extractor_output)
    
    if hierarchical_map:
        print("\nSuccessfully generated concept map:")
        print(json.dumps(hierarchical_map, indent=2))
    else:
        print("\nFailed to generate concept map.")