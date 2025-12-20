import streamlit as st
import pandas as pd
import pypdf
import io
from run_pipeline import run_full_pipeline, MODE

# --- Page Configuration ---
st.set_page_config(
    page_title="Scholara AI – Multi-Agent Quiz System",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    /* Main title styling */
    h1 {
        color: #FF6B6B; /* Red */
        font-size: 2.8em !important;
        font-weight: 700 !important;
    }

    /* Section header styling */
    h2 {
        color: #FF6B6B; /* Red */
        font-size: 2em !important;
        font-weight: 600 !important;
        border-bottom: 2px solid #e0e0e0;
        padding-bottom: 10px;
        margin-top: 20px;
    }

    /* Specific styling for sidebar headers */
    [data-testid="stSidebar"] h2 {
        color: #FF6B6B; /* Red*/
        font-size: 2.2em !important; /* Make the main sidebar title larger */
        border-bottom: none; /* Remove the bottom border for a cleaner look in the sidebar */
    }
</style>
""", unsafe_allow_html=True)


# --- Session State Initialization ---
if "results" not in st.session_state:
    st.session_state.results = None
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "Custom Text"

# --- Pre-canned Text Examples ---
PRE_CANNED_TEXT = {
    "Custom Text": "Paste your own text here or select a topic above...",
    "Machine Learning & AI": """
    Machine learning (ML) is a field of inquiry devoted to understanding and building methods that 'learn', that is, methods that leverage data to improve performance on some set of tasks. It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on sample data, known as training data, in order to make predictions or decisions without being explicitly programmed to do so. Machine learning algorithms are used in a wide variety of applications, such as in medicine, email filtering, speech recognition, and computer vision, where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks.
    A subset of machine learning is closely related to computational statistics, which focuses on making predictions using computers, but not all machine learning is statistical learning. The study of mathematical optimization delivers methods, theory and application domains to the field of machine learning. Data mining is a related field of study, focusing on exploratory data analysis through unsupervised learning. Some implementations of machine learning use data and neural networks in a way that mimics the working of a biological brain. In its application across business problems, machine learning is also referred to as predictive analytics.
    """,
    "The History of the Internet": """
    The history of the Internet has its origin in the efforts to build and interconnect computer networks that arose from research and development in the United States and involved international collaboration, particularly with researchers in the United Kingdom and France. The ARPANET, as it would become known, was a groundbreaking project. The first successful message on the ARPANET was sent by UCLA student programmer Charley Kline, at 22:30 PST on October 29, 1969, from Boelter Hall.
    The development of the TCP/IP protocol suite in the 1970s by Vint Cerf and Bob Kahn was a pivotal moment, providing a standard for how data should be packetized, addressed, transmitted, routed, and received. This allowed for the creation of a "network of networks," which is the foundation of the modern Internet. In 1983, the ARPANET migrated to TCP/IP. The 1980s also saw the expansion of the network to academic and military institutions. The commercialization of the Internet began in the late 1980s and early 1990s, but it was the invention of the World Wide Web by Tim Berners-Lee at CERN in 1989 that truly brought the Internet to the public. He developed HTML, HTTP, and the first web browser, making the Internet accessible and user-friendly.
    """
}

# --- Helper Functions ---
def extract_text_from_pdf(pdf_file):
    """Extracts text from an uploaded PDF file."""
    try:
        pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_file.read()))
        text = ""
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

def display_concepts_recursively(data, level=0):
    """Recursively displays nested concept data in a readable list."""
    if isinstance(data, dict):
        for key, value in data.items():
            st.markdown(f"{'&#8195;' * level * 2}• **{key}**")
            display_concepts_recursively(value, level + 1)
    elif isinstance(data, list):
        for item in data:
            display_concepts_recursively(item, level)
    elif isinstance(data, str):
        st.markdown(f"{'&#8195;' * level * 2}• {data}")


# --- UI ---
st.title("Scholara AI – Multi-Agent Quiz Generation System")
st.caption("Qualifier Build · Focus on Agent Reasoning & Validation")

with st.sidebar:
    st.header("Scholara AI")
    st.markdown("---")
    st.header("System Overview")
    st.markdown(
        "This dashboard demonstrates a multi-agent AI system that autonomously "
        "generates and validates educational content from raw text."
    )
    st.markdown(f"**Execution Mode:** `{MODE.upper()}`")

    # --- ADDED: Explanation for Mock Mode ---
    if MODE == 'mock':
        st.warning(
            "**Note on Mock Mode:** To avoid hitting free API rate limits and to ensure a smooth demo, this mode uses pre-generated data instead of making live AI calls."
        )

    st.markdown("---")
    
    with st.expander("Meet the Agent Team", expanded=True):
        st.markdown("**1. Extractor:** Scans text to identify key concepts.")
        st.markdown("**2. Organizer:** Arranges concepts into a logical hierarchy.")
        st.markdown("**3. Generator:** Creates quiz questions from the hierarchy.")
        st.markdown("**4. Ranker:** Assigns a difficulty score to each question.")
        st.markdown("**5. Validator:** Reviews each question for quality and correctness.")

    st.markdown("---")

    # --- RESTORED: Project Purpose / Hackathon Info Box ---
    st.markdown(
        """
        <div style='background-color:#1E1E2F; color:white; padding:15px; border-radius:8px; line-height:1.4em;'>
            <h2 style='margin-top:0; margin-bottom:8px; color:#FF6B6B;'>Project Purpose</h2>
            Scholara AI was developed for the <strong>GDG Autonomous Hack26 Hackathon</strong>.<br><br>
            The system demonstrates how a multi-agent AI pipeline can autonomously:
            <ul style='padding-left:18px; margin-top:0;'>
                <li>Extract meaningful knowledge from raw educational text.</li>
                <li>Generate quiz questions based on structured concepts.</li>
                <li>Validate and rank questions for quality and difficulty.</li>
            </ul>
            It highlights AI reasoning, automation capabilities, and architectural clarity in an educational context.
        </div>
        """,
        unsafe_allow_html=True
    )


# ---- Input Area with Tabs ----
input_tab1, input_tab2 = st.tabs(["📝 Text Input", "📄 PDF Upload"])

with input_tab1:
    selected_topic = st.selectbox(
        "Select an Example Topic (Optional)",
        options=list(PRE_CANNED_TEXT.keys()),
        key="selected_topic"
    )
    
    source_text_input = st.text_area(
        "Educational Text Input",
        value=PRE_CANNED_TEXT[st.session_state.selected_topic],
        height=250,
        label_visibility="collapsed"
    )

with input_tab2:
    uploaded_pdf = st.file_uploader(
        "Upload your educational PDF",
        type="pdf",
        label_visibility="collapsed"
    )

if st.button("🚀 Run Multi-Agent Pipeline"):
    source_text = ""
    if uploaded_pdf is not None:
        source_text = extract_text_from_pdf(uploaded_pdf)
    elif source_text_input.strip() and source_text_input != PRE_CANNED_TEXT["Custom Text"]:
        source_text = source_text_input
    
    if not source_text:
        st.error("Please provide input by either pasting text, selecting a topic, or uploading a PDF.")
        st.session_state.results = None
    else:
        with st.spinner("AI agents are reasoning... This may take a moment."):
            try:
                concepts, quiz, validation = run_full_pipeline(source_text)
                st.session_state.results = {
                    "concepts": concepts,
                    "quiz": quiz,
                    "validation": validation
                }
                st.success("Pipeline executed successfully!")
            except Exception as e:
                st.error(f"An error occurred during pipeline execution: {e}")
                st.session_state.results = None

# ---- Output Display ----
if st.session_state.results:
    st.markdown("---")
    
    # ---- 1. Extracted Concepts ----
    with st.container(border=True):
        st.header("1️⃣ Extracted Concept Hierarchy")
        if st.session_state.results["concepts"]:
            display_concepts_recursively(st.session_state.results["concepts"])
        else:
            st.warning("No concepts were extracted.")

    # ---- 2. Generated Quiz ----
    with st.container(border=True):
        st.header("2️⃣ Generated Quiz")
        quiz_data = st.session_state.results.get("quiz")
        validation_data = st.session_state.results.get("validation")

        if quiz_data and validation_data and len(quiz_data) == len(validation_data):
            # --- MODIFIED: Zip quiz and validation data together ---
            for i, (q, v) in enumerate(zip(quiz_data, validation_data), 1):
                with st.expander(f"**Question {i}:** {q['question']}"):
                    st.markdown("**Options:**")
                    for opt in q["options"]:
                        prefix = "✅" if opt == q["correct_answer"] else "◻️"
                        st.markdown(f"> {prefix} {opt}")
                    
                    st.markdown("---") # Add a separator
                    # --- FIXED: Get difficulty and decision from the validation object 'v' ---
                    st.markdown(f"**Difficulty:** `{v.get('difficulty', 'N/A')}`")
                    st.markdown(f"**Validator Decision:** `{v.get('decision', 'N/A')}`")
        else:
            st.warning("No quiz questions were generated or validation data is missing.")

    # ---- 3. Validator Output ----
    with st.container(border=True):
        st.header("3️⃣ Validator Output Analysis")
        if st.session_state.results["validation"]:
            try:
                df = pd.DataFrame(st.session_state.results["validation"])
                st.dataframe(df, use_container_width=True)
            except Exception:
                st.json(st.session_state.results["validation"])
        else:
            st.warning("No validation data was produced.")