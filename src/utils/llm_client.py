import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

MODEL_NAME = "models/gemini-2.5-flash"

def call_gemini_api(prompt: str) -> str:
    """
    Calls Gemini 2.5 Flash using the NEW Google GenAI SDK (AI Studio compatible)
    Returns plain text.
    """
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text
