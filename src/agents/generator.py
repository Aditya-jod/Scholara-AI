import json
import re
import random
from src.utils.llm_client import call_gemini_api

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
    selected_concepts = selected_concepts[:min(len(selected_concepts), num_questions)]

    questions = []
    for concept_obj in selected_concepts:
        concept_name = concept_obj.get("concept", "Unknown")
        print(f"Generating question for concept: {concept_name}...")

        prompt = f"""
You are an expert Quiz Designer for an educational platform.
Your task is to create a single, high-quality multiple-choice question based on the provided source text and a specific concept.

RULES:
- The question must directly test the understanding of the concept: "{concept_name}".
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

Now, generate the JSON for the multiple-choice question about "{concept_name}".
"""
        try:
            raw_response = call_gemini_api(prompt)
            json_str = _extract_json_object(raw_response)
            if not json_str:
                print(f"Generator Error: No JSON object found for concept '{concept_name}'. Skipping.")
                continue
            
            question_obj = json.loads(json_str)
            
            # Basic validation
            if all(k in question_obj for k in ["concept", "question", "options", "correct_answer"]):
                questions.append(question_obj)
            else:
                print(f"Generator Warning: Invalid JSON structure for concept '{concept_name}'. Skipping.")

        except (json.JSONDecodeError, Exception) as e:
            print(f"Generator failed for concept '{concept_name}': {e}")
            continue
            
    return questions

if __name__ == '__main__':
    sample_source_text = """
    Photosynthesis is a process used by plants, algae, and certain bacteria to convert light energy into chemical energy, 
    through a process that converts carbon dioxide and water into glucose (a sugar) and oxygen. 
    This process is crucial for life on Earth as it produces most of the oxygen in the atmosphere.
    Cellular respiration is the process by which organisms combine oxygen with foodstuff molecules, 
    diverting the chemical energy in these substances into life-sustaining activities and discarding, 
    as waste products, carbon dioxide and water.
    """
    sample_concepts = [
        { "concept": "Photosynthesis", "type": "process", "importance": 0.95 },
        { "concept": "Cellular respiration", "type": "process", "importance": 0.95 },
        { "concept": "Glucose", "type": "term", "importance": 0.8 },
        { "concept": "Plants", "type": "term", "importance": 0.9 },
        { "concept": "Light energy", "type": "term", "importance": 0.75 },
        { "concept": "Chemical energy", "type": "term", "importance": 0.75 },
        { "concept": "Oxygen", "type": "term", "importance": 0.7 },
        { "concept": "Carbon Dioxide", "type": "term", "importance": 0.7 }
    ]

    print("Running Generator Agent test...")
    generated_questions = generate_quiz_questions(sample_concepts, sample_source_text, num_questions=5)

    if generated_questions:
        print("\nSuccessfully generated quiz questions:")
        print(json.dumps(generated_questions, indent=2))
    else:
        print("\nFailed to generate any questions.")
