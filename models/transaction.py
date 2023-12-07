

from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlmodel import JSON, SQLModel, Field, Column, DateTime, func
from fastapi import Form
from datetime import datetime

class TransactionForm(SQLModel, table=True):
    __tablename__ = "contacts"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str 
    email: str
    amount: str
    currency: str
    description: str
    transaction_date: Optional[datetime] = Field(default=None, sa_column=Column(DateTime(timezone=True), default=func.now()))
    ip: Optional[str] = Field(default=None)
    
    class Config:
    	from_attributes = True
    
    @classmethod
    def as_form(cls, name: str, email: str, amount: str, currency: str, description: str, ip: str ):
        return cls(name=name, email=email, amount=amount, currency=currency, description=description, ip=ip)
