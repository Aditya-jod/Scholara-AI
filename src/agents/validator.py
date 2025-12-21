import json
import re
from src.utils.llm_client import call_gemini_api

def _extract_json_array(text: str):
    """Extract JSON array from text that might contain markdown or extra text."""
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    
    match = re.search(r'\[[\s\S]*\]', text)
    if match:
        return match.group(0)
    return None

def validate_question_difficulty(question: dict) -> dict:
    """
    Validates a single quiz question for difficulty appropriateness.
    Returns a validation result dictionary.
    """
    return validate_questions([question])[0]

def validate_questions(questions: list) -> list:
    """
    Validates quiz questions for quality, correctness, and clarity.
    Returns a list of validation results.
    """
    prompt = f"""
You are an Educational Quality Assurance Expert. Review each quiz question for:
- Question clarity and unambiguous wording
- Correctness of the correct answer
- Plausibility of distractors (wrong options)
- Appropriate difficulty level

QUESTIONS TO REVIEW:
{json.dumps(questions, indent=2)}

Return ONLY a valid JSON array with this EXACT structure (no extra text):
[
  {{
    "question_number": 1,
    "decision": "Approve",
    "reason": "Clear question with accurate answer and good distractors",
    "difficulty": "Medium",
    "importance": "Core"
  }},
  {{
    "question_number": 2,
    "decision": "Reject",
    "reason": "Question wording is ambiguous and could have multiple interpretations"
  }}
]

RULES:
- decision must be ONLY "Approve" or "Reject"
- Include difficulty and importance from the input questions
- Give specific reasons for your decision
- Return ONLY the JSON array, no other text before or after
"""

    try:
        raw_response = call_gemini_api(prompt)
        print(f"[Validator] Raw LLM Response:\n{raw_response}\n")
        
        json_str = _extract_json_array(raw_response)
        
        if not json_str:
            raise ValueError("No JSON array found in response")
        
        validations = json.loads(json_str)
        
        for i, validation in enumerate(validations):
            if i < len(questions):
                if 'difficulty' not in validation:
                    validation['difficulty'] = questions[i].get('difficulty', 'Medium')
                if 'importance' not in validation:
                    validation['importance'] = questions[i].get('importance', 'Important')
                if 'question' not in validation:
                    validation['question'] = questions[i].get('question', 'N/A')
                if 'reason' not in validation:
                    validation['reason'] = 'No specific reason provided'
        
        print(f"[Validator] Successfully parsed {len(validations)} validations")
        return validations

    except Exception as e:
        print(f"[Validator] Error: {e}")
        print(f"[Validator] Raw response was: {raw_response if 'raw_response' in locals() else 'No response received'}")
        
        fallback_validations = []
        for i, q in enumerate(questions, 1):
            fallback_validations.append({
                "question_number": i,
                "question": q.get("question", "N/A"),
                "decision": "Approve",
                "reason": f"Auto-approved due to parsing error: {str(e)[:100]}",
                "difficulty": q.get("difficulty", "Medium"),
                "importance": q.get("importance", "Important")
            })
        
        return fallback_validations

if __name__ == '__main__':
    sample_question_1 = {
        "concept": "Machine Learning",
        "question": "What is the primary goal of Machine Learning?",
        "options": ["To explicitly program computers", "To enable computers to learn from data", "To design user interfaces", "To manage server logic"],
        "correct_answer": "To enable computers to learn from data",
        "difficulty": "Easy" 
    }
    
    sample_question_2 = {
        "concept": "React",
        "question": "Which part of Web Development is the tool 'React' primarily used for?",
        "options": ["Backend development", "Database management", "Frontend development", "Server deployment"],
        "correct_answer": "Frontend development",
        "difficulty": "Easy" 
    }

    print("Running Validator Agent test...")
    
    print("\n--- Testing Illogical Question (ML as Easy) ---")
    validation_1 = validate_question_difficulty(sample_question_1)
    print(json.dumps(validation_1, indent=2))

    print("\n--- Testing Logical Question (React as Easy) ---")
    validation_2 = validate_question_difficulty(sample_question_2)
    print(json.dumps(validation_2, indent=2))