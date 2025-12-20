import json
import re
import random
import time
from src.utils.llm_client import call_gemini_api

API_CALL_DELAY_SECONDS = 2  # Reduced delay to 2 seconds

def _extract_json_object(text: str) -> str | None:
    """
    Extracts the first JSON object found in a string.
    """
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        return match.group(0)
    return None

def generate_quiz_questions(concepts: list, source_text: str, num_questions: int = 10) -> list:
    """
    Generates a list of multiple-choice quiz questions based on a list of concepts
    and the original source text.

    Args:
        concepts: The flat list of concept objects from the Extractor.
        source_text: The original text to provide context for question generation.
        num_questions: The desired number of questions.

    Returns:
        A list of quiz question objects.
    """
    
    # Sort concepts by importance to prioritize more significant topics
    # and shuffle to add variety if there are many important concepts.
    concepts.sort(key=lambda x: x.get('importance', 0), reverse=True)
    selected_concepts = concepts[:min(len(concepts), num_questions * 2)] # take a pool of important concepts
    random.shuffle(selected_concepts)
    selected_concepts = selected_concepts[:min(len(selected_concepts), num_questions)] # select final concepts

    questions = []
    # Ensure we don't try to generate more questions than concepts available
    num_to_generate = min(num_questions, len(selected_concepts))

    for concept in selected_concepts[:num_to_generate]:
        print(f"Generating question for concept: {concept['concept']}...")
        # We add a small delay to be respectful of the API rate limits.
        print("   ...waiting 2s to respect API rate limit...")
        time.sleep(2)
        
        prompt = f"""
You are an expert Quiz Designer for an educational platform.
Your task is to create a single, high-quality multiple-choice question based on the provided source text and a specific concept.

RULES:
- The question must directly test the understanding of the concept: "{concept['concept']}".
- The question should be answerable using only the information present in the source text below.
- Generate 4 options: one correct answer and three plausible but incorrect distractors.
- The output must be a SINGLE JSON object with the following keys:
  - "concept": The concept the question is about.
  - "question": The text of the question.
  - "options": A list of 4 strings (the choices).
  - "correct_answer": The string of the correct answer, which must be one of the items in the "options" list.

SOURCE TEXT:
---
{source_text}
---

Now, generate the JSON for the multiple-choice question about "{concept['concept']}".
"""
        try:
            raw_response = call_gemini_api(prompt)
            json_str = _extract_json_object(raw_response)
            if not json_str:
                print(f"Generator Error: No JSON object found for concept '{concept['concept']}'. Skipping.")
                continue
            
            question_obj = json.loads(json_str)
            
            # Basic validation
            if all(k in question_obj for k in ["concept", "question", "options", "correct_answer"]):
                questions.append(question_obj)
            else:
                print(f"Generator Warning: Invalid JSON structure for concept '{concept['concept']}'. Skipping.")

        except (json.JSONDecodeError, Exception) as e:
            print(f"Generator failed for concept '{concept['concept']}': {e}")
            continue
            
    return questions

if __name__ == '__main__':
    # NEW: Updated sample text and concepts for CS topic
    sample_source_text = """
    Machine Learning is a subfield of Artificial Intelligence that gives computers the ability to learn without being explicitly programmed. It is broadly divided into Supervised Learning, which uses labeled data, and Unsupervised Learning, which finds patterns in unlabeled data. A common Supervised Learning algorithm is Linear Regression. Web Development involves creating websites and applications. It consists of Frontend development, which focuses on the user interface using tools like React, and Backend development, which manages the server, database, and application logic using technologies like Node.js.
    """
    sample_concepts = [
        {"concept": "Machine Learning", "type": "process", "importance": 0.95},
        {"concept": "Supervised Learning", "type": "process", "importance": 0.85},
        {"concept": "Linear Regression", "type": "term", "importance": 0.7},
        {"concept": "Web Development", "type": "process", "importance": 0.95},
        {"concept": "React", "type": "term", "importance": 0.75}
    ]

    print("Running Generator Agent test...")
    generated_questions = generate_quiz_questions(sample_concepts, sample_source_text, num_questions=5)

    if generated_questions:
        print("\nSuccessfully generated quiz questions:")
        print(json.dumps(generated_questions, indent=2))
    else:
        print("\nFailed to generate any questions.")
