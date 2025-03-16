import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

# Get API key from environment variable
api_key = os.getenv('GEMINI_API_KEY')

# Create a Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

def categorize(input_text):
    try:
        response = model.generate_content(
            f"Reply with either topic or specific. Categorize the following as either a topic or a specific academic paper: {input_text}"
        )
        return response.text
    except Exception as e:
        return f"Error processing request: {str(e)}"