import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("API_KEY not found in environment variables")

# Configure the Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def categorize(input):
    response = model.generate_content(
        f"Reply with either topic or specific. Categorize the following as either a topic or a specific academic paper: {input}"
    )
    return response.text