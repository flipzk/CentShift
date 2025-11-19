from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    BRL = "BRL"
    CHF = "CHF"

class TransactionCreate(BaseModel):
    type: str
    amount: float
    currency: Currency = Currency.EUR
    date: date
    category: Optional[str] = None
    description: Optional[str] = None

class TransactionRead(TransactionCreate):
    id: int
