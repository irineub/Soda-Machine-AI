from sqlmodel import SQLModel, Field, create_engine, Session, select
from datetime import datetime
from typing import Optional, List

engine = create_engine("sqlite:///./soda_ai.db", echo=True)

class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
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
    product_id: int

class SaleOut(SQLModel):
    id: int
    product_id: int
    timestamp: datetime


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
