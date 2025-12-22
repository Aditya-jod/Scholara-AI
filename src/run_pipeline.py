import json
import logging
import os

from src.agents.extractor import extract_concepts
from src.agents.organizer import organize_concepts
from src.agents.generator import generate_quiz_questions
from src.agents.ranker import rank_questions
from src.agents.validator import validate_questions

# --- Configuration ---
MODE = "mock" # Options: "live" or "mock" live is for API calls, mock uses predefined data becasue of rate limits in API usage

os.environ["MODE"] = MODE

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] [%(levelname)s] - %(message)s'
)

def load_mock_data(file_path):
    with open(file_path, "r") as f:
        return json.load(f)

def run_full_pipeline(source_text):
    logging.info(f"Pipeline starting in {MODE.upper()} mode.")

    # ---------- 1. EXTRACTOR ----------
    if MODE == "live":
        logging.info("[Extractor] Extracting concepts...")
        concepts = extract_concepts(source_text)
    else:
        concepts = load_mock_data("mock_data/concepts.json")

    if not concepts:
        raise ValueError("Extractor produced no concepts")

    # ---------- 2. ORGANIZER ----------
    if MODE == "live":
        logging.info("[Organizer] Building concept hierarchy...")
        concept_map = organize_concepts(concepts)
    else:
        concept_map = load_mock_data("mock_data/concept_map.json")

    if not concept_map or "concept_map" not in concept_map:
        raise ValueError("Organizer produced invalid concept map")

    # ---------- 3. GENERATOR (FIXED) ----------
    if MODE == "live":
        logging.info("[Generator] Generating quiz questions...")
        quiz_questions = generate_quiz_questions(
            concepts,       
            source_text,
            num_questions=5
        )
    else:
        quiz_questions = load_mock_data("mock_data/quiz.json")

    if not quiz_questions:
        raise ValueError("Generator produced no questions")

    # ---------- 4. RANKER ----------
    logging.info("[Ranker] Assigning difficulty...")
    ranked_questions = rank_questions(
        questions=quiz_questions,
        concept_map=concept_map  
    )

    # ---------- 5. VALIDATOR ----------
    logging.info("[Validator] Validating questions...")
    validation_results = []

    for idx, question in enumerate(ranked_questions):
        result = validate_questions(question)
        result["question_id"] = idx
        validation_results.append(result)

    # ---------- FINAL MERGE ----------
    for idx, q in enumerate(ranked_questions):
        v = validation_results[idx]
        q["decision"] = v.get("decision", "N/A")
        q["reason"] = v.get("reason", "N/A")

    logging.info("Pipeline finished successfully.")

    return concept_map, ranked_questions, validation_results


if __name__ == "__main__":
    text = "Machine learning includes supervised and unsupervised learning techniques."
    concept_map, quiz, validation = run_full_pipeline(text)

    print(json.dumps(quiz, indent=2))
