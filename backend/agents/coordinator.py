import os
import json
from pathlib import Path
from groq import Groq
from dotenv import load_dotenv

# Load backend/.env
dotenv_path = Path(__file__).resolve().parent.parent / ".env"

print("Using .env:", dotenv_path)
print("Exists:", dotenv_path.exists())

load_dotenv(dotenv_path=dotenv_path, override=True)

print("Groq Key:", os.getenv("GROQ_API_KEY"))

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("❌ GROQ_API_KEY not found in backend/.env")

client = Groq(api_key=api_key)


def analyze_emergency(emergency: str):

    print("1. Function started")

    prompt = f"""
You are an expert Emergency Response Coordinator AI.

Analyze the emergency below.

Emergency:
{emergency}

Return ONLY valid JSON.

{{
    "priority":"",
    "confidence":0,
    "emergency_type":"",
    "summary":"",
    "ambulance_required":false,
    "hospital_department":[],
    "first_aid":[],
    "recommended_action":"",
    "estimated_response_time":"",
    "reason":""
}}
"""

    print("2. Prompt created")

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

        print("3. Response received")

        text = response.choices[0].message.content.strip()

        if text.startswith("```json"):
            text = text.replace("```json", "").replace("```", "").strip()
        elif text.startswith("```"):
            text = text.replace("```", "").strip()

        return json.loads(text)

    except Exception as e:
        return {"error": str(e)}