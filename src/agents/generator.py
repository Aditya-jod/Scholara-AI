import json
import re
import random
import time
from src.utils.llm_client import call_gemini_api

API_CALL_DELAY_SECONDS = 2

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
    Generates multiple-choice quiz questions based on extracted concepts.
    """

    if not isinstance(concepts, list):
        raise TypeError("Expected concepts to be a list")

    sorted_concepts = sorted(
        concepts,
        key=lambda c: c.get("importance", 0),
        reverse=True
    )

    selected_concepts = sorted_concepts[:min(len(sorted_concepts), num_questions)]

    questions = []

    for concept in selected_concepts:
        concept_name = concept.get("concept")
        if not concept_name:
            continue

        print(f"Generating question for concept: {concept_name}")
        time.sleep(API_CALL_DELAY_SECONDS)

        prompt = f"""
You are an expert Quiz Designer.

Create ONE multiple-choice question for the concept "{concept_name}".

RULES:
- Use ONLY the source text
- Generate 4 options
- 1 correct answer
- Output ONLY valid JSON

FORMAT:
{{
  "concept": "{concept_name}",
  "question": "...",
  "options": ["A", "B", "C", "D"],
  "correct_answer": "A"
}}

SOURCE TEXT:
{source_text}
"""

        try:
            raw_response = call_gemini_api(prompt)
            json_str = _extract_json_object(raw_response)

            if not json_str:
                continue

            question = json.loads(json_str)

            if (
                isinstance(question, dict)
                and "question" in question
                and isinstance(question.get("options"), list)
                and "correct_answer" in question
            ):
                questions.append(question)

        except Exception as e:
            print(f"Generator error for {concept_name}: {e}")

    return questions


if __name__ == '__main__':
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
