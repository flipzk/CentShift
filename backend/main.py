from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlmodel import Session
from . import models, schemas, crud, db, budget, ai_service

@asynccontextmanager
async def lifespan(app: FastAPI):
    db.create_db_and_tables()
    yield

app = FastAPI(title="CentShift API", lifespan=lifespan)


@app.post("/transactions/", response_model=schemas.TransactionRead)
def create_transaction(tx: schemas.TransactionCreate, session: Session = Depends(db.get_session)):
    transaction = models.Transaction.from_orm(tx)
    return crud.create_transaction(session, transaction)

@app.get("/transactions/", response_model=list[schemas.TransactionRead])
def get_transactions(skip: int = 0, limit: int = 100, session: Session = Depends(db.get_session)):
    return crud.list_transactions(session, skip, limit)

@app.get("/budget/calculate")
def get_budget_allocation(amount: float, strategy: str):
    return budget.calculate_allocation(amount, strategy)

@app.post("/transactions/scan")
async def scan_receipt(file: UploadFile = File(...)):
    """
    Receives an image file, processes it with Google Gemini AI, 
    and returns structured JSON data (Total, Date, Category, Description).
    """
    # 1. Validate File Type
    if file.content_type not in ["image/jpeg", "image/png", "image/heic", "image/jpg"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPG/PNG allowed.")

    # 2. Read file content
    try:
        content = await file.read()
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to read file.")

    # 3. Call AI Service
    result = ai_service.analyze_receipt(content)

    if not result:
         raise HTTPException(status_code=500, detail="AI Analysis failed.")
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])

    return result