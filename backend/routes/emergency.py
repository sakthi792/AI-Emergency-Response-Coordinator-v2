from fastapi import APIRouter
from agents.coordinator import analyze_emergency
from agents.hospital_agent import hospital_agent
from services.database_service import get_all_emergencies

router = APIRouter()

@router.get("/analyze")
def analyze(emergency: str):
    return analyze_emergency(emergency)

@router.get("/hospital")
def hospital(emergency: str):
    return hospital_agent(emergency)

@router.get("/history")
def history():
    return get_all_emergencies()