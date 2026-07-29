from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.emergency import router as emergency_router

from database.database import engine, Base
from models.emergency import Emergency

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Emergency Response Coordinator",
    version="1.0"
)

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

app.include_router(emergency_router)