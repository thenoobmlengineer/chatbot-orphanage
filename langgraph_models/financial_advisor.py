import openai
from dotenv import load_dotenv
import os

load_dotenv()  # Load API key from .env file

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_financial_advice(user_input):
    messages = [
        {"role": "system", "content": "You are a financial advisor for children."},
        {"role": "user", "content": user_input}
    ]
    
    response = openai.ChatCompletion.create(
        model="gpt-4",  # Use GPT-4 or gpt-4o-mini if available
        messages=messages,
        temperature=0.7,
        max_tokens=500
    )
    
    return response['choices'][0]['message']['content'].strip()
