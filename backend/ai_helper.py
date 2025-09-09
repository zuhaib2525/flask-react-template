import os
from openai import OpenAI


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_task(prompt):
    """
    Send a prompt to OpenAI API and get a generated task.
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",          # or "gpt-4" if you have access
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content.strip()
