from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from agents.blood_resources import router as blood_router
from services.database_service import get_all_emergencies
from routes.emergency import router as emergency_router
from agents.weather_alerts import router as weather_router
from database.database import engine, Base
from agents.earthquake_agent import router as earthquake_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Emergency Response Coordinator",
    version="1.0",
    description="AI-powered emergency triage and hospital recommendation system."
)
app.include_router(earthquake_router)
app.include_router(blood_router)
app.include_router(weather_router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Home"])
def home():
    return {
        "message": "AI Emergency Response Coordinator"
    }

@app.get("/history", tags=["History"])
def history():
    return get_all_emergencies()

@app.get("/health", tags=["Health"])
def health():
    return {
        "status": "healthy",
        "server": "running"
    }

app.include_router(emergency_router)