import json

def _find_concept_in_tree(concept_name: str, node: dict) -> dict | None:
    """
    Recursively searches for a concept node in the concept map.
    """
    if node.get("concept") == concept_name:
        return node
    
    for child in node.get("children", []):
        found = _find_concept_in_tree(concept_name, child)
        if found:
            return found
            
    return None

def rank_questions(questions: list, concept_map: dict) -> list:
    """
    Assigns a difficulty (Easy, Medium, Hard) to each question based on
    its concept's depth and number of children in the concept map.
    """
    ranked_questions = []
    
    for question in questions:
        concept_name = question.get("concept")
        if not concept_name:
            question["difficulty"] = "Medium"
            ranked_questions.append(question)
            continue

        # Find the concept in the overall map
        found_node = None
        for root_node in concept_map.get("concept_map", []):
            found_node = _find_concept_in_tree(concept_name, root_node)
            if found_node:
                break
        
        if not found_node:
            question["difficulty"] = "Easy"
            ranked_questions.append(question)
            continue
            
        # The Heuristic: child count determines difficulty
        child_count = len(found_node.get("children", []))
        
        if child_count == 0:
            difficulty = "Easy"  # Leaf node, specific fact
        elif child_count <= 2:
            difficulty = "Medium" # Small branch
        else:
            difficulty = "Hard"   # Major concept with many sub-topics
            
        question["difficulty"] = difficulty
        ranked_questions.append(question)
        
    return ranked_questions

if __name__ == '__main__':
    # NEW: Updated sample questions and map for CS topic
    sample_questions = [
        {
            "concept": "Machine Learning",
            "question": "What is the primary goal of Machine Learning?",
            "options": ["To explicitly program computers", "To enable computers to learn from data", "To design user interfaces", "To manage server logic"],
            "correct_answer": "To enable computers to learn from data"
        },
        {
            "concept": "React",
            "question": "Which part of Web Development is the tool 'React' primarily used for?",
            "options": ["Backend development", "Database management", "Frontend development", "Server deployment"],
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
                { "concept": "Supervised Learning", "children": [{"concept": "Linear Regression", "children": []}] },
                { "concept": "Unsupervised Learning", "children": [] }
              ]
            }
          ]
        },
        {
          "concept": "Web Development",
          "children": [
              {"concept": "Frontend development", "children": [{"concept": "React", "children": []}]},
              {"concept": "Backend development", "children": [{"concept": "Node.js", "children": []}]}
          ]
        }
      ]
    }

    print("Running Ranker Agent test...")
    final_ranked_questions = rank_questions(sample_questions, sample_concept_map)

    print("\nSuccessfully ranked questions:")
    print(json.dumps(final_ranked_questions, indent=2))