import os
import json
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

dotenv_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=dotenv_path)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def police_agent(emergency: str):

    prompt = f"""
You are a Police Emergency AI.

Determine whether police assistance is required.

Emergency:
{emergency}

Return ONLY valid JSON.

{{
    "police_required": true,
    "priority": "",
    "reason": "",
    "response_time": ""
}}
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    text = response.choices[0].message.content.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").replace("```", "").strip()

    return json.loads(text)