import os
import json
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"

print("Using .env:", dotenv_path)
print("Exists:", dotenv_path.exists())

load_dotenv(dotenv_path=dotenv_path, override=True)

print("Groq Key:", os.getenv("GROQ_API_KEY"))

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def recommend_hospital(emergency: str):

    prompt = f"""
You are an Emergency Hospital Recommendation AI.

Emergency:
{emergency}

Recommend the MOST SUITABLE hospital.

Return ONLY valid JSON.

{{
    "hospital_name":"",
    "department":"",
    "reason":"",
    "priority":""
}}
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        text = response.choices[0].message.content.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}