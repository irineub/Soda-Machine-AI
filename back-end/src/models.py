from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

engine = create_engine("sqlite:///./soda_ai.db", echo=True)

class MessageInput(BaseModel):
    message: str

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True, unique=True)
    stock: int
    price: int

class ProductCreate(SQLModel):
    name: str
    stock: int
    price: int

class ProductOut(SQLModel):
    id: int
    name: str
    stock: int
    price: int

class Sale(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="product.id")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class SaleCreate(SQLModel):
    product_name: str
    quantity: int

class SaleOut(SQLModel):
    id: int
    product_name: str
    timestamp: datetime

class MostSoldItem(BaseModel):
    product_name: str
    total_sold: int

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
