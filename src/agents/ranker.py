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
    sample_questions = [
        {
            "concept": "Photosynthesis",
            "question": "What is the primary process plants use to convert light energy into chemical energy?",
            "options": ["Respiration", "Transpiration", "Photosynthesis", "Decomposition"],
            "correct_answer": "Photosynthesis"
        },
        {
            "concept": "Light energy",
            "question": "What type of energy do plants capture to initiate photosynthesis?",
            "options": ["Kinetic energy", "Nuclear energy", "Light energy", "Potential energy"],
            "correct_answer": "Light energy"
        }
    ]
    
    sample_concept_map = {
      "concept_map": [
        {
          "concept": "Plants",
          "children": [
            {
              "concept": "Photosynthesis",
              "children": [
                { "concept": "Light energy", "children": [] },
                { "concept": "Carbon Dioxide", "children": [] },
                { "concept": "Glucose", "children": [] },
                { "concept": "Oxygen", "children": [] },
                { "concept": "Chemical energy", "children": [] }
              ]
            }
          ]
        },
        { "concept": "Cellular respiration", "children": [] }
      ]
    }

    print("Running Ranker Agent test...")
    final_ranked_questions = rank_questions(sample_questions, sample_concept_map)

    print("\nSuccessfully ranked questions:")
    print(json.dumps(final_ranked_questions, indent=2))