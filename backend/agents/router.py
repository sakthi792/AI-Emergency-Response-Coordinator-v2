import os
import json
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def route_emergency(emergency: str):

    prompt = f"""
You are an Emergency Dispatch Router.

Your ONLY job is to decide which emergency services are needed.

Emergency:
{emergency}

Return ONLY valid JSON.

{{
    "emergency_type":"",
    "agents":[]
}}

Possible agents:
- ambulance
- police
- fire
- hospital

Examples:

Road accident with injuries
{{
    "emergency_type":"Road Accident",
    "agents":["ambulance","police","hospital"]
}}

House fire
{{
    "emergency_type":"Fire",
    "agents":["fire","ambulance"]
}}

Heart attack
{{
    "emergency_type":"Medical",
    "agents":["ambulance","hospital"]
}}

Bike theft
{{
    "emergency_type":"Crime",
    "agents":["police"]
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
        text = text.replace("```", "").replace("```", "").strip()

    return json.loads(text)