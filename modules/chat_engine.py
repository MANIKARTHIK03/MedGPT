import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def ask_medgpt(question):
    """
    Sends a user question to the OpenAI LLM and returns the response.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are MedGPT, a helpful AI medical assistant that provides general information. Avoid giving diagnoses; focus on insights and education."},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {str(e)}"
