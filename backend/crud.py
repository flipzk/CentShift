from sqlmodel import Session, select
from . import models 

def create_transaction(session: Session, transaction: models.Transaction):
    session.add(transaction)
    session.commit()
    session.refresh(transaction)
    return transaction

def list_transactions(session: Session, skip: int = 0, limit: int = 100):
    statement = select(models.Transaction).offset(skip).limit(limit)
    results = session.exec(statement)
    return results.all()