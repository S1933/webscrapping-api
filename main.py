from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models
import schemas
from models import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
  title="Quotes API",
  description="Test API webscrapping",
  version="1.0.0",
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

@app.get("/")
def read_root():
  return {"message": "Welcome Quotes API"}

@app.get("/quotes/", response_model=List[schemas.Quote])
def read_quotes(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
  quotes = db.query(models.Quote).offset(skip).limit(limit).all()
  return quotes

@app.get("/quotes/{quote_id}", response_model=schemas.Quote)
def read_quote(quote_id: int, db: Session = Depends(get_db)):
  quote = db.query(models.Quote).filter(models.Quote.id == quote_id).first()
  if quote is None:
    raise HTTPException(status_code=404, detail="Quote not found")
  return quote
