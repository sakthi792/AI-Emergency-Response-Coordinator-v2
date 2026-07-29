from sqlalchemy import Column, Integer, String, Boolean, Float
from database.database import Base

class Emergency(Base):
    __tablename__ = "emergencies"

    id = Column(Integer, primary_key=True, index=True)
    emergency_type = Column(String)
    priority = Column(String)
    confidence = Column(Float)
    summary = Column(String)
    ambulance_required = Column(Boolean)
    recommended_action = Column(String)