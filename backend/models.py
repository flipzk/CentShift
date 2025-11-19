from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date
from enum import Enum

class Currency(str, Enum):
    EUR = "EUR"
    USD = "USD"
    BRL = "BRL"
    CHF = "CHF"

class Transaction(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    type: str                 # "expense", "income", "investment", "saving"
    amount: float
    currency: Currency = Currency.EUR
    date: date
    category: Optional[str] = None
    description: Optional[str] = None
