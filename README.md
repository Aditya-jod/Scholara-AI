# Scholara AI 🧠✨

**Scholara AI** is an autonomous, multi-agent system designed to transform any piece of text into a structured, hierarchical knowledge base and generate a comprehensive quiz from it. Built for the modern learner, Scholara AI uses a sophisticated 5-agent pipeline to deconstruct, organize, and assess knowledge.

This project was developed as part of a 24-hour hackathon, demonstrating rapid prototyping of complex AI systems.

## 🚀 Key Features

- **Autonomous 5-Agent Pipeline:** A team of specialized AI agents work in concert to process information.
- **Hierarchical Concept Mapping:** Automatically generates a tree-like structure of concepts, showing relationships between main topics and sub-topics.
- **Dynamic Quiz Generation:** Creates multiple-choice questions based on the extracted concepts.
- **Intelligent Difficulty Ranking:** A rule-based agent ranks questions as "Easy," "Medium," or "Hard" based on their conceptual depth.
- **AI-Powered Validation:** A "critic" agent reviews generated questions to ensure their difficulty is appropriate.
- **SQLite Caching Layer:** Drastically improves speed and reliability by caching agent results, minimizing redundant API calls and making the system resilient to API rate limits.

## 🏗️ Architecture

Scholara AI operates through a sequential pipeline of five distinct agents, with a caching layer for optimization.

```
[Input Text]
      |
      v
+----------------+   1. [Extractor Agent]   -> Extracts key concepts as a flat list.
|   CACHE CHECK  |   2. [Organizer Agent]   -> Builds a hierarchical concept map.
+----------------+   3. [Generator Agent]   -> Creates quiz questions from concepts.
      |              4. [Ranker Agent]      -> Assigns difficulty to questions.
      v              5. [Validator Agent]   -> Approves or rejects question difficulty.
[Final Quiz]
```

## 🛠️ Tech Stack

- **Backend:** Python
- **AI:** Google Gemini API (`gemini-1.5-flash`)
- **Web Framework:** Streamlit (for the UI)
- **Database:** SQLite (for caching)
- **Core Libraries:** `requests`, `argparse`, `json`, `hashlib`

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

### 4. Run the Self-Test (Backend Pipeline)

To test the entire agent pipeline, run the `main.py` script with the `--self-test` flag. The first run will be slow as it populates the cache. Subsequent runs will be nearly instant.

```bash
python main.py --self-test
```

### 5. Run the Web Application

To start the Streamlit user interface, run `app.py`:

```bash
streamlit run app.py
```

## 🔮 Future Work

- [ ] **Full UI Integration:** Connect the Streamlit UI to the backend agent pipeline.
- [ ] **User Accounts:** Allow users to save and review past quizzes.
- [ ] **Cloud SQL Migration:** Upgrade the caching layer from SQLite to a production-grade database like Google Cloud SQL.
- **Feedback Loop:** Allow user feedback on question quality to fine-tune the agents.
- **LangGraph Integration:** Re-architect the agent pipeline using a formal framework like LangGraph for more complex interactions and state management.
