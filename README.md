# Scholara AI 🧠✨

**Scholara AI** is an autonomous, multi-agent system designed to transform educational content—from raw text or PDF files—into a structured knowledge base and a comprehensive quiz. Built for the modern learner, Scholara AI uses a sophisticated 5-agent pipeline to deconstruct, organize, and assess knowledge.

This project was developed as part of a 24-hour hackathon, demonstrating the rapid prototyping of complex, multi-agent AI systems.

## 🚀 Key Features

- **Multi-Format Input:** Process educational content from either pasted text or uploaded PDF documents.
- **Autonomous 5-Agent Pipeline:** A team of specialized AI agents work in concert to process information.
- **Hierarchical Concept Mapping:** Automatically generates a tree-like structure of concepts, showing relationships between main topics and sub-topics.
- **Dynamic Quiz Generation:** Creates multiple-choice questions based on the extracted concepts.
- **Intelligent Validation & Ranking:** Agents review generated questions for quality, correctness, and difficulty.
- **Demo-Ready:** Includes pre-canned text examples and a `mock` mode to ensure smooth, API-free demonstrations.

## 🏗️ Architecture

Scholara AI operates through a sequential pipeline of five distinct agents. The system can run in `live` mode (calling the Gemini API) or `mock` mode (using pre-generated data to avoid API rate limits).

```
[Input Text / PDF]
      |
      v
+----------------+   1. [Extractor Agent]   -> Extracts key concepts.
|  AGENT PIPELINE  |   2. [Organizer Agent]   -> Builds a hierarchical concept map.
+----------------+   3. [Generator Agent]   -> Creates quiz questions from concepts.
      |              4. [Ranker Agent]      -> Assigns difficulty to questions.
      v              5. [Validator Agent]   -> Approves or rejects questions.
[Final Quiz]
```

## 🛠️ Tech Stack

- **Backend:** Python
- **AI:** Google Gemini API (`gemini-1.5-flash`)
- **Web Framework:** Streamlit
- **Core Libraries:** `pypdf` (for PDF extraction), `pandas`

## ⚙️ How to Run

### 1. Prerequisites

- Python 3.9+
- A Google AI Studio API Key

### 2. Setup

Clone the repository and install the required dependencies.

```bash
# Clone the repository
git clone <your-repo-url>
cd Scholara-AI

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

Create a file named `.env` in the root of the project and add your API key:

```
GEMINI_API_KEY="YOUR_API_KEY_HERE"
```

### 4. Run the Web Application

To start the Streamlit user interface, run `streamlit_app.py`:

```bash
streamlit run streamlit_app.py
```
The application can be switched between `live` and `mock` modes by changing the `MODE` variable in `run_pipeline.py`.

## 🔮 Future Work

- [ ] **Refactor with PipelineState:** Fully integrate the `PipelineState` class to manage data flow between agents.
- [ ] **User Accounts:** Allow users to save and review past quizzes.
- [ ] **Feedback Loop:** Allow user feedback on question quality to fine-tune the agents.
- [ ] **LangGraph Integration:** Re-architect the agent pipeline using a formal framework like LangGraph for more complex interactions and state management.
