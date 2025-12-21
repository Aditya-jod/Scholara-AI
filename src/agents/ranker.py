from src.utils.llm_client import call_gemini_api
import json
import re

def _extract_json_object(text: str):
    match = re.search(r"\{[\s\S]*\}", text)
    return match.group(0) if match else None

def rank_questions(questions: list, concept_map: dict) -> list:
    """
    Uses LLM to assign difficulty and importance based on concept hierarchy.
    """
    ranked_questions = []

    for idx, question in enumerate(questions, start=1):
        concept_name = question.get("concept", "Unknown")
        
        prompt = f"""
You are an Educational Assessment Expert. Analyze this concept's position in the knowledge hierarchy and assign appropriate difficulty and importance.

CONCEPT: {concept_name}

FULL CONCEPT HIERARCHY:
{json.dumps(concept_map, indent=2)}

RULES FOR DIFFICULTY:
- Root/broad concepts (depth 0-1): "Hard"
- Mid-level concepts (depth 2-3): "Medium"  
- Leaf/specific concepts (depth 4+): "Easy"

RULES FOR IMPORTANCE:
- Core concepts: "Core"
- Supporting concepts: "Important"
- Detailed concepts: "Supporting"

Return ONLY this JSON:
{{
  "difficulty": "Hard|Medium|Easy",
  "importance": "Core|Important|Supporting"
}}
"""

        try:
            raw_response = call_gemini_api(prompt)
            json_str = _extract_json_object(raw_response)
            ranking = json.loads(json_str) if json_str else {}
            
            difficulty = ranking.get("difficulty", "Medium")
            importance = ranking.get("importance", "Important")
            
        except Exception as e:
            print(f"Ranker LLM error: {e}")
            difficulty = "Medium"
            importance = "Important"

        ranked_question = {
            **question,
            "question_id": idx,
            "difficulty": difficulty,
            "importance": importance
        }
        ranked_questions.append(ranked_question)

    return ranked_questions

if __name__ == "__main__":
    sample_questions = [
        {
            "concept": "Machine Learning",
            "question": "What is the primary goal of Machine Learning?",
            "options": [
                "To explicitly program computers",
                "To enable computers to learn from data",
                "To design user interfaces",
                "To manage server logic"
            ],
            "correct_answer": "To enable computers to learn from data"
        },
        {
            "concept": "React",
            "question": "Which part of Web Development is React used for?",
            "options": [
                "Backend development",
                "Database management",
                "Frontend development",
                "Server deployment"
            ],
            "correct_answer": "Frontend development"
        }
    ]

    sample_concept_map = {
        "concept_map": [
            {
                "concept": "Artificial Intelligence",
                "children": [
                    {
                        "concept": "Machine Learning",
                        "children": [
                            {
                                "concept": "Supervised Learning",
                                "children": [
                                    {"concept": "Linear Regression", "children": []}
                                ]
                            },
                            {"concept": "Unsupervised Learning", "children": []}
                        ]
                    }
                ]
            },
            {
                "concept": "Web Development",
                "children": [
                    {
                        "concept": "Frontend development",
                        "children": [
                            {"concept": "React", "children": []}
                        ]
                    }
                ]
            }
        ]
    }

    ranked = rank_questions(sample_questions, sample_concept_map)
    print(json.dumps(ranked, indent=2))
