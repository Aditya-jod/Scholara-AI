import json
import logging
from src.agents.extractor import extract_concepts
from src.agents.organizer import organize_concepts
from src.agents.generator import generate_quiz_questions
from src.agents.ranker import rank_questions
from src.agents.validator import validate_question_difficulty

# --- Configuration ---
MODE = "mock"  # Switch to "live" to use APIs

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] [%(levelname)s] - %(message)s')

def load_mock_data(file_path):
    """Loads data from a JSON file."""
    with open(file_path, 'r') as f:
        return json.load(f)

def run_full_pipeline(source_text):
    """
    Orchestrates the full agent pipeline from extraction to validation.
    Supports both 'live' and 'mock' modes.
    """
    logging.info(f"Pipeline starting in {MODE.upper()} mode.")

    # --- 1. Extractor Agent ---
    if MODE == "live":
        logging.info("[Extractor Agent] Starting concept extraction...")
        concepts = extract_concepts(source_text)
        logging.info("[Extractor Agent] Completed.")
    else:
        logging.info("[Extractor Agent] Loading mock concepts...")
        concepts = load_mock_data('mock_data/concepts.json')
        logging.info("[Extractor Agent] Completed.")

    if not concepts:
        logging.error("Extractor failed to produce concepts. Aborting.")
        return None, None, None

    # --- 2. Quiz Generator Agent ---
    if MODE == "live":
        logging.info("[Quiz Agent] Starting question generation...")
        # In a real scenario, you might pass concepts to the generator
        quiz_questions = generate_quiz_questions(concepts, source_text, num_questions=2)
        logging.info(f"[Quiz Agent] Generated {len(quiz_questions)} questions.")
    else:
        logging.info("[Quiz Agent] Loading mock questions...")
        quiz_questions = load_mock_data('mock_data/quiz.json')
        logging.info(f"[Quiz Agent] Loaded {len(quiz_questions)} questions.")

    if not quiz_questions:
        logging.error("Generator failed to produce questions. Aborting.")
        return concepts, None, None

    # --- 3. Validator Agent ---
    final_validations = []
    if MODE == "live":
        logging.info(f"[Validator Agent] Starting validation for {len(quiz_questions)} questions...")
        for i, q in enumerate(quiz_questions):
            validation_result = validate_question_difficulty(q) # Assuming validator takes question and concepts
            validation_result['question_id'] = i
            final_validations.append(validation_result)
        logging.info("[Validator Agent] Completed.")
    else:
        logging.info("[Validator Agent] Loading mock validations...")
        final_validations = load_mock_data('mock_data/validation.json')
        logging.info("[Validator Agent] Completed.")

    # Combine quiz questions with their validation results
    for i, q in enumerate(quiz_questions):
        validation = next((v for v in final_validations if v.get("question_id") == i), None)
        if validation:
            q['decision'] = validation.get('decision', 'N/A')
            q['reason'] = validation.get('reason', 'N/A')
            q['difficulty'] = validation.get('difficulty', 'N/A')

    logging.info("Pipeline finished successfully.")
    return concepts, quiz_questions, final_validations

if __name__ == '__main__':
    # This allows you to test the pipeline directly
    sample_text = "This is a sample text for testing the pipeline."
    concepts_output, quiz_output, validation_output = run_full_pipeline(sample_text)
    
    print("\n--- CONCEPTS ---")
    print(json.dumps(concepts_output, indent=2))
    
    print("\n--- QUIZ ---")
    print(json.dumps(quiz_output, indent=2))
    
    print("\n--- VALIDATION ---")
    print(json.dumps(validation_output, indent=2))
