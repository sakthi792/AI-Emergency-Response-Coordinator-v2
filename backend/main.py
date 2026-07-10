from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from agents.coordinator import analyze_emergency
from agents.hospital_agent import recommend_hospital

app = FastAPI(
    title="AI Emergency Response Coordinator",
    version="1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {
        "message": "AI Emergency Response Coordinator"
    }

@app.get("/analyze")
def analyze(emergency: str):
    return analyze_emergency(emergency)

@app.get("/hospital")
def hospital(emergency: str):
    return recommend_hospital(emergency)