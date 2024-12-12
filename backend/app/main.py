# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, status, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .models import Transaction,TransactionCreate,TransactionResponse, Base
from .database import engine, SessionLocal
from datetime import datetime
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Tracker API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    return {
        "message": "Finance Tracking API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/transactions/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    db_transaction = Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.get("/transactions/", response_model=List[TransactionResponse])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).all()

@app.get("/transactions/{transaction_id}", response_model=TransactionResponse)
def get_transaction_by_id(transaction_id: int, db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.id == transaction_id).first()

@app.delete("/transactions/{transaction_id}", response_model=TransactionResponse)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"Transaction with id {transaction_id} not found.")
    db.delete(transaction)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)