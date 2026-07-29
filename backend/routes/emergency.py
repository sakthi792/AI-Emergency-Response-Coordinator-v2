from fastapi import APIRouter
from agents.coordinator import analyze_emergency
from agents.hospital_agent import recommend_hospital
from services.database_service import get_all_emergencies

router = APIRouter()

@router.get("/analyze")
def analyze(emergency: str):
    return analyze_emergency(emergency)

@router.get("/hospital")
def hospital(emergency: str):
    return recommend_hospital(emergency)

@router.get("/history")
def history():
    return get_all_emergencies()