import os
import json
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def extract_location(emergency: str):

    prompt = f"""
Extract the city from this emergency.

Emergency:
{emergency}

Return ONLY valid JSON.

{{
    "city":""
}}

If no city is mentioned return:

{{
    "city":"Unknown"
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return json.loads(text)