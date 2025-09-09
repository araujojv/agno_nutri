from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class AgentSession(Base):
    __tablename__ = "agent_sessions"
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    role = Column(String(50))   # "user" ou "assistant"
    content = Column(Text)

class Meal(Base):
    __tablename__ = "meals"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String(20))
    time = Column(String(10))
    period = Column(String(50))  # café da manhã, almoço etc.
    description = Column(Text)
    calories = Column(Integer)
