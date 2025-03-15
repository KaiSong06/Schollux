from google import genai


# Replace with your API key
api_key = 'AIzaSyBQGN0XhFcm_-T_IArl37j7E5pHH3nt8V0'

# Create a Gemini client
client = genai.Client(api_key=api_key)
def categorize(input):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Reply with either topic or specific. Categorize the following as eitehr a topic or a specific academic paper: {input}",
    )
    return response

input = "Nutrient requirements of beef cattle"

