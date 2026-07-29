import os
import json
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def ambulance_agent(emergency: str):

    prompt = f"""
You are an Ambulance Emergency AI.

Analyze ONLY whether an ambulance is required.

Emergency:
{emergency}

Return ONLY JSON.

{{
    "ambulance_required": true,
    "priority": "",
    "reason": "",
    "response_time": ""
}}
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    text = response.choices[0].message.content
    text = text.replace("```json", "").replace("```", "").strip()

    return json.loads(text)