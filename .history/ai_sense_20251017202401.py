# ai_sense.py
from google import genai
from config import API_KEY, GEMINI_MODEL

# Initialize Gemini Client
client = genai.Client(api_key=API_KEY)

def ask_gemini(prompt):
    """
    Ask Gemini API for response
    """
    try:
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"Gemini API Error: {e}"
# if __name__ == "__main__":
#     answer = ask_gemini("Who was the first programmer?")
#     print(answer)
