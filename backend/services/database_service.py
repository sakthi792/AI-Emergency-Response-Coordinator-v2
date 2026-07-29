from sqlalchemy.orm import Session
from database.database import SessionLocal
from models.emergency import Emergency


def save_emergency(data: dict):
    db: Session = SessionLocal()

    try:
        emergency = Emergency(
            emergency_type=data.get("emergency_type"),
            priority=data.get("priority"),
            confidence=data.get("confidence"),
            summary=data.get("summary"),
            ambulance_required=data.get("ambulance_required"),
            recommended_action=data.get("recommended_action"),
        )

        db.add(emergency)
        db.commit()
        db.refresh(emergency)

        return emergency

    finally:
        db.close()


def get_all_emergencies():
    db: Session = SessionLocal()

    try:
        return db.query(Emergency).order_by(Emergency.id.desc()).all()

    finally:
        db.close()