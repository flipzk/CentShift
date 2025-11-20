from fastapi import FastAPI, Depends
from sqlmodel import Session
from . import models, schemas, crud, db, budget  # Importações relativas

app = FastAPI(title="CentShift API") 

# Cria a base de dados quando a app arranca
@app.on_event("startup")
def on_startup():
    db.create_db_and_tables()

@app.post("/transactions/", response_model=schemas.TransactionRead)
def create_transaction(tx: schemas.TransactionCreate, session: Session = Depends(db.get_session)):
    transaction = models.Transaction.from_orm(tx)
    return crud.create_transaction(session, transaction)

@app.get("/transactions/", response_model=list[schemas.TransactionRead])
def get_transactions(skip: int = 0, limit: int = 100, session: Session = Depends(db.get_session)):
    return crud.list_transactions(session, skip, limit)

@app.get("/budget/calculate")
def get_budget_allocation(amount: float, strategy: str):
    # Chama a lógica pura que criámos no budget.py
    return budget.calculate_allocation(amount, strategy)