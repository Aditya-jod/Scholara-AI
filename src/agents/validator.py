import json
import re
from typing import Optional
from src.utils.llm_client import call_gemini_api

def _extract_json_object(text: str) -> Optional[str]:
    """
    Extracts the first JSON object found in a string.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return None

def validate_question_difficulty(question: dict) -> dict:
    """
    Uses an LLM to validate if the assigned difficulty of a single question is logical.

    Args:
        question: A single question object with a "difficulty" key.

    Returns:
        A validation result object from the LLM.
    """
    
    prompt = f"""
You are a Lead Quality Engineer reviewing a quiz. Your task is to validate if the assigned difficulty for a given question is logical.

RULES:
- Broad, high-level concepts should be "Medium" or "Hard". A question about "Machine Learning" should not be "Easy".
- Specific, niche concepts should be "Easy" or "Medium". A question about "Linear Regression" should not be "Hard".
- Your output MUST be a single JSON object with two keys:
  - "decision": Your decision, either "approve" or "reject".
  - "reason": A brief, one-sentence explanation for your decision.

EXAMPLE OUTPUT 1:
{{
  "decision": "approve",
  "reason": "The difficulty 'Hard' is appropriate for a broad, foundational concept."
}}

EXAMPLE OUTPUT 2:
{{
  "decision": "reject",
  "reason": "The concept is a specific algorithm, so a 'Hard' difficulty is illogical; it should be 'Easy' or 'Medium'."
}}

Here is the question to validate:
{json.dumps(question, indent=2)}

Now, provide your validation as a JSON object.
"""

    try:
        raw_response = call_gemini_api(prompt)
        json_str = _extract_json_object(raw_response)
        if not json_str:
            return {"decision": "reject", "reason": "Failed to get a valid JSON response from validator LLM."}
            
        validation_result = json.loads(json_str)
        return validation_result

    except (json.JSONDecodeError, Exception) as e:
        print(f"Validator failed to parse response: {e}")
        return {"decision": "reject", "reason": f"An exception occurred during validation: {e}"}

if __name__ == '__main__':
    # Sample inputs that might be logically inconsistent
    sample_question_1 = {
        "concept": "Machine Learning",
        "question": "What is the primary goal of Machine Learning?",
        "options": ["To explicitly program computers", "To enable computers to learn from data", "To design user interfaces", "To manage server logic"],
        "correct_answer": "To enable computers to learn from data",
        "difficulty": "Easy"  # This is illogical, should be rejected
    }
    
    sample_question_2 = {
        "concept": "React",
        "question": "Which part of Web Development is the tool 'React' primarily used for?",
        "options": ["Backend development", "Database management", "Frontend development", "Server deployment"],
        "correct_answer": "Frontend development",
        "difficulty": "Easy" # This is logical, should be approved
    }

    print("Running Validator Agent test...")
    
    print("\n--- Testing Illogical Question (ML as Easy) ---")
    validation_1 = validate_question_difficulty(sample_question_1)
    print(json.dumps(validation_1, indent=2))

    print("\n--- Testing Logical Question (React as Easy) ---")
    validation_2 = validate_question_difficulty(sample_question_2)
    print(json.dumps(validation_2, indent=2))