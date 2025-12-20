import argparse
import json
import time
from src.agents.extractor import extract_concepts
from src.agents.organizer import organize_concepts
from src.agents.generator import generate_quiz_questions
from src.agents.ranker import rank_questions
from src.agents.validator import validate_question_difficulty
from src.utils.db_manager import init_db, get_cached_result, set_cached_result

API_CALL_DELAY_SECONDS = 15 # 15 seconds to stay safely within a 5 RPM limit

def run_self_test():
    """
    Runs a full end-to-end test of the agentic pipeline,
    printing the inputs and outputs of each agent.
    """
    print(" STARTING SCHOLARA AI SELF-TEST ")
    print("========================================")

    # Initialize the database
    init_db()

    # 1. Source Text
    source_text = """
    Machine Learning is a subfield of Artificial Intelligence that gives computers the ability to learn without being explicitly programmed. It is broadly divided into Supervised Learning, which uses labeled data, and Unsupervised Learning, which finds patterns in unlabeled data. A common Supervised Learning algorithm is Linear Regression. Web Development involves creating websites and applications. It consists of Frontend development, which focuses on the user interface using tools like React, and Backend development, which manages the server, database, and application logic using technologies like Node.js.
    """
    print("1. [INPUT] Source Text:\n", source_text)
    print("-" * 20)

    print("--------------------")
    print("2. [AGENT] Running Cognito, the Concept Extractor...")
    
    # Check cache for Extractor
    extracted_concepts = get_cached_result('extractor', source_text)
    if not extracted_concepts:
        extracted_concepts = extract_concepts(source_text)
        set_cached_result('extractor', source_text, extracted_concepts)

    if not extracted_concepts:
        print("[ERROR] Extractor failed to produce output.")
        return
    print("   [OUTPUT] Extracted Concepts:\n", json.dumps(extracted_concepts, indent=2))
    print("-" * 20)

    print("--------------------")
    print("3. [AGENT] Running Arbor, the Knowledge Organizer...")

    # Check cache for Organizer
    concept_map = get_cached_result('organizer', source_text, extracted_concepts)
    if not concept_map:
        concept_map = organize_concepts(extracted_concepts)
        set_cached_result('organizer', source_text, concept_map, extracted_concepts)

    if not concept_map:
        print("[ERROR] Organizer failed to produce output.")
        return
    print("   [OUTPUT] Concept Map:\n", json.dumps(concept_map, indent=2))
    print("-" * 20)

    print("--------------------")
    print("4. [AGENT] Running Quest, the Question Generator...")

    # Check cache for Generator
    # Note: Generator has randomness, so caching might not be ideal if you want variety every time.
    # For speed and reliability during testing, we'll cache it.
    generated_questions = get_cached_result('generator', source_text, concept_map)
    if not generated_questions:
        generated_questions = generate_quiz_questions(extracted_concepts, source_text, 5)
        set_cached_result('generator', source_text, generated_questions, concept_map)

    if not generated_questions:
        print("[ERROR] Generator failed to produce output.")
        return
    print(f"   [OUTPUT] Generated {len(generated_questions)} Questions.")

    print("--------------------")
    print("5. [AGENT] Running Scala, the Difficulty Ranker...")
    # Ranker is a local, deterministic function, so caching provides less benefit,
    # but we'll do it for consistency.
    ranked_questions = get_cached_result('ranker', source_text, generated_questions)
    if not ranked_questions:
        ranked_questions = rank_questions(generated_questions, concept_map)
        set_cached_result('ranker', source_text, ranked_questions, generated_questions)

    if not ranked_questions:
        print("[ERROR] Ranker failed to produce output.")
        return
    print("   [OUTPUT] Ranked Questions:\n", json.dumps(ranked_questions, indent=2))
    print("-" * 20)

    # --- Agent 5: Validator (and Correction Loop) ---
    print("--------------------")
    print("6. [AGENT] Running Veritas, the Validator...")

    validated_questions = []
    for q in ranked_questions:
        print(f"\n   Validating question for concept: '{q['concept']}' (Difficulty: {q['difficulty']})")
        print("   ...waiting 2s to respect API rate limit...")
        time.sleep(2)
        validation_result = validate_question_difficulty(q)

        # BUG FIX: Check the 'decision' key in the returned dictionary.
        # The previous check `if "APPROVE" in validation_result:` was incorrect.
        if validation_result and validation_result.get('decision') == 'approve':
            print(f"   [DECISION] Validator says: {validation_result.get('decision')}")
            validated_questions.append(q)
        else:
            reason = validation_result.get('reason') if validation_result else "No response from validator."
            print(f"   [DECISION] Validator says: REJECT. Reason: {reason}")
            print(f"   [ACTION] Re-generating question for '{q['concept']}'...")
            print("   ...waiting 2s to respect API rate limit...")
            time.sleep(2)
            # Try to re-generate once
            new_question_data = generate_quiz_questions([{'concept': q['concept']}], source_text, 1)
            if new_question_data:
                new_q = new_question_data[0]
                # Re-rank the new question
                new_q_ranked_list = rank_questions([new_q], concept_map)
                if new_q_ranked_list:
                    new_q_ranked = new_q_ranked_list[0]
                    print(f"   [SUCCESS] Re-generated and re-ranked. New difficulty: {new_q_ranked['difficulty']}")
                    validated_questions.append(new_q_ranked)
                else:
                    print("   [FAILURE] Could not re-rank the new question.")
            else:
                print("   [FAILURE] Could not re-generate a question.")

    print("="*40)
    print(" SELF-TEST COMPLETE ")
    print(f"Final quiz contains {len(validated_questions)} validated questions.")
    print(json.dumps(validated_questions, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scholara AI - Main Application & Test Runner")
    parser.add_argument(
        "--self-test",
        action="store_true",
        help="Run the full end-to-end agentic pipeline with sample data."
    )
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
    else:
        # This is where the Streamlit app would normally be launched.
        # We will build this part later.
        print("No flags provided. To run the pipeline test, use: python main.py --self-test")
        print("To run the web app, you will eventually use: streamlit run app.py")
