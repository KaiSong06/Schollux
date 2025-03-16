import google.generativeai as genai
import os
from dotenv import load_dotenv
from . import Categorize
from .search import search_papers
import logging

load_dotenv()

api_key = os.getenv('API_KEY')

if not api_key:
    raise ValueError("API_KEY not found in environment variables")

# Configure the Gemini client
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

def refineQuery(input):
    try:
        response = model.generate_content(
            f"Extract and refine the main research topic or paper title from this query, make it concise and focused for academic search: {input}"
        )
        return response.text
    except Exception as e:
        logging.error(f"Error refining query: {str(e)}")
        return input

def format_articles(articles):
    formatted = "\n\n".join([
        f"**{article['title']}**\n"
        f"Authors: {article['authors']}\n"
        f"Year: {article['year']}"
        for article in articles
    ])
    return formatted

def summarize(input):
    try:
        category = str(Categorize.categorize(input)).lower().strip()
        logging.info(f"Category determined: {category}")
        
        query = refineQuery(input)
        logging.info(f"Refined query: {query}")
        
        articles = search_papers(category, query)
        logging.info(f"Found articles: {articles}")
        
        formatted_articles = format_articles(articles)
        
        if category == "topic":
            prompt = (
                "As an academic researcher, provide a comprehensive analysis of these papers:\n\n"
                f"{formatted_articles}\n\n"
                "Structure your response as follows:\n\n"
                "# Paper Summaries\n"
                "(Provide a 2-3 sentence summary for each paper)\n\n"
                "# Common Themes\n"
                "(Identify and explain the main themes across the papers)\n\n"
                "# Key Implications\n"
                "(Discuss the most important implications for the field)\n\n"
                "Use bullet points where appropriate and be concise but thorough."
            )
        elif category == "specific":
            prompt = (
                "As an academic researcher, provide a detailed analysis of this paper:\n\n"
                f"{formatted_articles}\n\n"
                "Structure your response as follows:\n\n"
                "# Main Findings\n"
                "(List the key findings and contributions)\n\n"
                "# Research Methodology\n"
                "(Describe the research approach)\n\n"
                "# Practical Implications\n"
                "(Explain the real-world applications)\n\n"
                "# Future Directions\n"
                "(Discuss limitations and future research opportunities)\n\n"
                "Use bullet points where appropriate and be concise but thorough."
            )
        else:
            raise ValueError(f"Invalid category: {category}")
        
        response = model.generate_content(prompt)
        return response.text
        
    except Exception as e:
        logging.error(f"Summarization error: {str(e)}")
        return f"Error processing request: {str(e)}"

