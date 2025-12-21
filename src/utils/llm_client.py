import os
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

# Check if we're in mock mode to avoid importing API dependencies
MODE = os.getenv("MODE", "mock")

def call_gemini_api(prompt: str) -> str:
    """
    Calls Gemini API or returns empty string in mock mode.
    Returns plain text.
    """
    # In mock mode, don't make API calls
    if MODE == "mock":
        print("Mock mode: Skipping API call")
        return ""
    
    try:
        # Only import when actually needed (live mode)
        import google.genai as genai
        
        # Configure the API key
        api_key = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("Please set GOOGLE_API_KEY or GEMINI_API_KEY in your .env file")

        client = genai.Client(api_key=api_key)
        MODEL_NAME = "gemini-1.5-flash"
        
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text
        
    except ImportError:
        print("Error: google-genai package not installed. Install with: pip install google-genai")
        return ""
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return ""
