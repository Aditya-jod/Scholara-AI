import json
from typing import Optional, Tuple


def _find_concept_in_tree(
    concept_name: str,
    node: dict,
    depth: int = 0
) -> Optional[Tuple[dict, int]]:
    """
    Recursively searches for a concept node in the concept map.
    Returns (node, depth) if found.
    """
    if node.get("concept") == concept_name:
        return node, depth

    for child in node.get("children", []):
        found = _find_concept_in_tree(concept_name, child, depth + 1)
        if found:
            return found

    return None


def _calculate_difficulty(depth: int, child_count: int) -> str:
    """
    Difficulty heuristic based on concept depth and breadth.
    """
    if depth >= 3:
        return "Hard"
    if child_count == 0:
        return "Easy"
    if child_count <= 2:
        return "Medium"
    return "Hard"


def _calculate_importance(depth: int) -> str:
    """
    Importance reflects conceptual centrality.
    """
    if depth == 0:
        return "Core"
    if depth <= 2:
        return "Important"
    return "Supporting"


def rank_questions(questions: list, concept_map: dict) -> list:
    """
    Assigns difficulty and importance to each question
    based on its concept's position in the concept hierarchy.

    Returns a NEW list (no mutation).
    """
    ranked_questions = []

    for idx, question in enumerate(questions, start=1):
        concept_name = question.get("concept")

        # Safe defaults (never N/A)
        difficulty = "Medium"
        importance = "Important"
        depth = None
        child_count = None

        if concept_name:
            for root_node in concept_map.get("concept_map", []):
                result = _find_concept_in_tree(concept_name, root_node)
                if result:
                    found_node, depth = result
                    child_count = len(found_node.get("children", []))

                    difficulty = _calculate_difficulty(depth, child_count)
                    importance = _calculate_importance(depth)
                    break
            else:
                # Concept not found → treat as simple fact
                difficulty = "Easy"
                importance = "Supporting"

        ranked_question = {
            **question,
            "question_id": question.get("question_id", idx),
            "difficulty": difficulty,
            "importance": importance,
            "ranker_metadata": {
                "concept": concept_name,
                "depth": depth,
                "child_count": child_count
            }
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
