import os
import json
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

from services.database_service import save_emergency

dotenv_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=dotenv_path, override=True)

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("❌ GROQ_API_KEY not found in backend/.env")

client = Groq(api_key=api_key)


def analyze_emergency(emergency: str):

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

        result = json.loads(text)

        print("Saving to database...")

        save_emergency(result)

        print("Saved successfully!")

        return result

    except Exception as e:
        print("Error:", e)
        return {"error": str(e)}