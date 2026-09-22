from sqlalchemy import Column, Integer, Float, String, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from app.database.connection import Base


class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sex = Column(String(10))
    age = Column(Integer)
    height_cm = Column(Float)
    weight_kg = Column(Float)
    activity_level = Column(String(50))
    dietary_preference = Column(String(50))
    goal = Column(String(50))
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
