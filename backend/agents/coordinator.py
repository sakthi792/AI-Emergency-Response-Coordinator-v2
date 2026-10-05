import os
import json
from datetime import datetime
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

from services.database_service import save_emergency

from agents.router import route_emergency
from agents.location_agent import extract_location
from agents.ambulance_agent import ambulance_agent
from agents.police_agent import police_agent
from agents.fire_agent import fire_agent
from agents.hospital_agent import hospital_agent

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
    "priority": "",
    "confidence": 0,
    "emergency_type": "",
    "summary": "",
    "ambulance_required": false,
    "hospital_department": [],
    "first_aid": [],
    "recommended_action": "",
    "estimated_response_time": "",
    "reason": ""
}}
"""

    try:

        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
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

        priority = str(result.get("priority", "")).capitalize()

        allowed = ["Low", "Medium", "High", "Critical"]

        if priority not in allowed:
            priority = "Medium"

        result["priority"] = priority

        location = extract_location(emergency)
        result["location"] = location

        routing = route_emergency(emergency)
        result["routing"] = routing

        print("Running specialized agents...")

        agents_result = {}

        required_agents = routing.get("agents", [])

        if "ambulance" in required_agents:
            agents_result["ambulance"] = ambulance_agent(emergency)

        if "police" in required_agents:
            agents_result["police"] = police_agent(emergency)

        if "fire" in required_agents:
            agents_result["fire"] = fire_agent(emergency)

        if "hospital" in required_agents:
            agents_result["hospital"] = hospital_agent(
                emergency,
                location["city"]
            )

        result["agents"] = agents_result

        result["timestamp"] = datetime.now().isoformat()

        print("Saving to database...")

        save_emergency(result)

        print("Saved successfully!")

        return result

    except Exception as e:
        print("Error:", e)
        return {
            "success": False,
            "message": "Emergency analysis failed.",
            "error": str(e)
        }