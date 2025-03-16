from google import genai
import os
from dotenv import load_dotenv
load_dotenv()


api_key= os.getenv('API_KEY')

# Replace with your API key
if not api_key:
    print("bad")



# Create a Gemini client
client = genai.Client(api_key=api_key)
def categorize(input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Reply with either topic or specific. Categorize the following as eitehr a topic or a specific academic paper: {input}",
    )
    return response