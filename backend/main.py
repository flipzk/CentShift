from fastapi import FastAPI, Depends
from sqlmodel import Session
from . import models
from . import schemas
from . import crud
from . import db

app = FastAPI(title="CentShift API") 

db.create_db_and_tables()

@app.post("/transactions/", response_model=schemas.TransactionRead)
def create_transaction(tx: schemas.TransactionCreate, session: Session = Depends(db.get_session)):
    transaction = models.Transaction(**tx.dict())
    return crud.create_transaction(session, transaction)

@app.get("/transactions/", response_model=list[schemas.TransactionRead])
def get_transactions(skip: int = 0, limit: int = 100, session: Session = Depends(db.get_session)):
    return crud.list_transactions(session, skip, limit)
