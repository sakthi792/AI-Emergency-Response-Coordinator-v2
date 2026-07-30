from fastapi import APIRouter
from agents.coordinator import analyze_emergency
from agents.hospital_agent import hospital_agent


router = APIRouter()

@router.get("/analyze", tags=["Emergency"])
def analyze(emergency: str):
    return analyze_emergency(emergency)

@router.get("/hospital", tags=["Hospital"])
def hospital(emergency: str):
    return hospital_agent(emergency)
