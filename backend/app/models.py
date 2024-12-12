# backend/app/models.py
from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base
from pydantic import BaseModel

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    description = Column(String, nullable=False)
    category = Column(String, nullable=False)
    date = Column(DateTime, default=datetime.utcnow)

class TransactionCreate(BaseModel):
    amount: float
    description: str
    category: str

class TransactionResponse(TransactionCreate):
    id: int
    date: datetime
    
    class Config:
        from_attributes = True