from google import genai
import os
from dotenv import load_dotenv
import Categorize
import search
load_dotenv()

api_key= os.getenv('API_KEY')

# Replace with your API key
if not api_key:
    print("bad")

def refineQuery(input):
    client = genai.Client(api_key=api_key)
    query = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"Refine the following for a search query on research articles: {input}",
    )
    return query

def summarize(input):
    client = genai.Client(api_key=api_key)
    category = Categorize.categorize(input)
    query = refineQuery(input)
    articles = search.search(category, query)
    if category == "topic":
        res = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"You are an expert online researcher and summarizer, use this list of research articles" +
        " in the format [title, author(s)] to find the article and summarize each of them." + 
        " Then with using the summarized versions, provide a general consensus on the topic at hand." + 
        "Here is the list {articles}",
    )
    elif category == "specific":
        res = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=f"You are an expert online researcher and summarizer, using the following input" + 
        " in the form [title, author(s), find and and summarize the article in jot notes.",
    )
        

