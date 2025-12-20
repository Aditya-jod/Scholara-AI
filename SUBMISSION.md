# Scholara AI – Hackathon Submission

## 🧠 Project Overview

Scholara AI is an autonomous multi-agent system that transforms educational content—from raw text or PDF files—into a structured knowledge base and generates quizzes. It demonstrates the rapid prototyping of a complex AI system capable of reasoning, organizing, and evaluating content autonomously.

## 🎯 Problem Statement

Students and educators often face information overload. Extracting key concepts, generating relevant quiz questions, and validating them manually is a time-consuming and inefficient process. Scholara AI automates this entire workflow, making learning and assessment more efficient, scalable, and accessible.

## 🚀 Key Features

- **Multi-Format Input:** Accepts pasted text or direct PDF uploads.
- **5-Agent AI Pipeline:** A team of Extractor, Organizer, Generator, Ranker, and Validator agents work in sequence to process information.
- **Hierarchical Concept Mapping:** Automatically visualizes the relationships between main topics and sub-topics in a clear, tree-like structure.
- **Dynamic Quiz Generation:** Generates relevant multiple-choice questions based on the extracted concepts.
- **Intelligent Validation:** Each generated question is reviewed by an AI agent for quality, relevance, difficulty, and correctness.

## ⛓️ Agent Pipeline & Workflow

The core of Scholara AI is its sequential agent pipeline, where the output of one agent becomes the input for the next. This creates a clear and logical flow of reasoning.

```
[Input Text / PDF]
      |
      v
+----------------+   1. [Extractor Agent]   -> Extracts key concepts.
|  AGENT PIPELINE  |   2. [Organizer Agent]   -> Builds a hierarchical concept map.
+----------------+   3. [Generator Agent]   -> Creates quiz questions from concepts.
      |              4. [Ranker Agent]      -> Assigns difficulty to questions.
      v              5. [Validator Agent]   -> Approves or rejects questions.
[Final Quiz & Analysis]
```

## 🛠️ Technical Highlights

- **AI Engine:** Google Gemini API (`gemini-1.5-flash`) drives the reasoning and generation capabilities across all five agents.
- **Web Framework:** A polished and interactive user interface built with Streamlit.
- **Data Handling:** Python and `pandas` are used for structuring and displaying the final validation results.
- **Execution Modes:** The system includes a `live` mode for real-time API calls and a `mock` mode for API-free offline demonstrations, crucial for development and presentation under API rate limits.

## 🏆 Hackathon Context

- Developed within **24 hours** for the **GDG Autonomous Hack26** competition.
- The primary focus was on demonstrating a robust **agent architecture, clear AI reasoning, and autonomous validation**, rather than UI complexity.
- A video demo was prepared to showcase the end-to-end pipeline execution and highlight the intelligence of each agent's contribution.

## ⚡ How to Demo

1.  Run the Streamlit interface from your terminal:
    ```bash
    streamlit run streamlit_app.py
    ```
2.  In the web app, either paste educational text or upload a PDF document.
3.  Click the **"🚀 Run Multi-Agent Pipeline"** button.
4.  Observe the generated output in the three main sections:
    - **Extracted Concept Hierarchy:** The structured knowledge map.
    - **Generated Quiz:** The list of questions with correct answers marked.
    - **Validator Output Analysis:** A table summarizing the validator's decisions and reasoning.
5.  This workflow is ideal for recording a submission video.