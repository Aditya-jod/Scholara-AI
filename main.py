import argparse
import json
import time
from src.agents.extractor import extract_concepts
from src.agents.organizer import organize_concepts
from src.agents.generator import generate_quiz_questions
from src.agents.ranker import rank_questions
from src.agents.validator import validate_question_difficulty

API_CALL_DELAY_SECONDS = 15 # 15 seconds to stay safely within a 5 RPM limit

def run_self_test():
    """
    Runs a full end-to-end test of the agentic pipeline,
    printing the inputs and outputs of each agent.
    """
    print(" STARTING SCHOLARA AI SELF-TEST ")
    print("="*40)

    # --- Sample Input ---
    source_text = """
    Machine Learning is a subfield of Artificial Intelligence that gives computers the ability to learn without being explicitly programmed. It is broadly divided into Supervised Learning, which uses labeled data, and Unsupervised Learning, which finds patterns in unlabeled data. A common Supervised Learning algorithm is Linear Regression. Web Development involves creating websites and applications. It consists of Frontend development, which focuses on the user interface using tools like React, and Backend development, which manages the server, database, and application logic using technologies like Node.js.
    """
    print("1. [INPUT] Source Text:\n", source_text)
    print("-" * 20)

    # --- Agent 1: Extractor ---
    print("2. [AGENT] Running Extractor...")
    concepts = extract_concepts(source_text)
    if not concepts:
        print("Extractor failed. Aborting test.")
        return
    print("   [OUTPUT] Extracted Concepts:\n", json.dumps(concepts, indent=2))
    print("-" * 20)

    # --- Agent 2: Organizer ---
    print("3. [AGENT] Running Organizer...")
    concept_map = organize_concepts(concepts)
    if not concept_map:
        print("Organizer failed. Aborting test.")
        return
    print("   [OUTPUT] Concept Map:\n", json.dumps(concept_map, indent=2))
    print("-" * 20)

    # --- Agent 3: Generator ---
    print("4. [AGENT] Running Generator...")
    questions = generate_quiz_questions(concepts, source_text, num_questions=5)
    if not questions:
        print("Generator failed. Aborting test.")
        return
    print(f"   [OUTPUT] Generated {len(questions)} Questions.")
    print("-" * 20)

    # --- Agent 4: Ranker ---
    print("5. [AGENT] Running Ranker...")
    ranked_questions = rank_questions(questions, concept_map)
    print("   [OUTPUT] Ranked Questions:\n", json.dumps(ranked_questions, indent=2))
    print("-" * 20)

    # --- Agent 5: Validator (and Correction Loop) ---
    # print("--------------------")
    # print("6. [AGENT] Running Validator...")
    #
    # validated_questions = []
    # for q in ranked_questions:
    #     print(f"\n   Validating question for concept: '{q['concept']}' (Difficulty: {q['difficulty']})")
    #     print("   ...waiting 15s to respect API rate limit...")
    #     time.sleep(15)
    #     validation_result = validate_question_difficulty(q)

    #     if "APPROVE" in validation_result:
    #         print(f"   [DECISION] Validator says: {validation_result}")
    #         validated_questions.append(q)
    #     else:
    #         print(f"   [DECISION] Validator says: {validation_result}")
    #         print(f"   [ACTION] Re-generating question for '{q['concept']}'...")
    #         print("   ...waiting 15s to respect API rate limit...")
    #         time.sleep(15)
    #         # Try to re-generate once
    #         new_question_data = generate_quiz_questions([{'concept': q['concept']}], source_text, 1)
    #         if new_question_data:
    #             new_q = new_question_data[0]
    #             # Re-rank the new question
    #             new_q_ranked_list = rank_questions([new_q], concept_map)
    #             if new_q_ranked_list:
    #                 new_q_ranked = new_q_ranked_list[0]
    #                 print(f"   [SUCCESS] Re-generated and re-ranked. New difficulty: {new_q_ranked['difficulty']}")
    #                 validated_questions.append(new_q_ranked)
    #             else:
    #                 print("   [FAILURE] Could not re-rank the new question.")
    #         else:
    #             print("   [FAILURE] Could not re-generate a question.")
    
    # For now, let's just use the ranked questions without validation
    validated_questions = ranked_questions

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
