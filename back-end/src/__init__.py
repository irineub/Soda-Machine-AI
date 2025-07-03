from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List
from .models import (
    Product, ProductCreate, ProductOut,
    Sale, SaleCreate, SaleOut,
    engine, create_db_and_tables
)
from .agent.ai_agent import AIAgent

class MessageInput(BaseModel):
    message: str
    
app = FastAPI(title="Soda AI API", version="1.0.0")
agent = AIAgent()

# Dependency to get database session
def get_session():
    with Session(engine) as session:
        yield session

# Create database tables on startup
@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


@app.post("/ask")
def ask(message_input: MessageInput):
    try:
        response = agent.handle_message(message_input.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Sorry, i cant answer your question right now, please try again")

# Product CRUD endpoints
@app.post("/products/", response_model=ProductOut)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    db_product = Product.from_orm(product)
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.get("/products/", response_model=List[ProductOut])
def read_products(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    products = session.exec(select(Product).offset(skip).limit(limit)).all()
    return products

@app.get("/products/{product_id}", response_model=ProductOut)
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product: ProductCreate, session: Session = Depends(get_session)):
    db_product = session.get(Product, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product_data = product.dict(exclude_unset=True)
    for key, value in product_data.items():
        setattr(db_product, key, value)
    
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session)):
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    session.delete(product)
    session.commit()
    return {"message": "Product deleted successfully"}

# Sale CRUD endpoints
@app.post("/sales/", response_model=SaleOut)
def create_sale(sale: SaleCreate, session: Session = Depends(get_session)):
    # Check if product exists
    product = session.get(Product, sale.product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Check if stock is available
    if product.stock <= 0:
        raise HTTPException(status_code=400, detail="Product out of stock")
    
    # Create sale and update stock
    db_sale = Sale.from_orm(sale)
    session.add(db_sale)
    
    # Update product stock
    product.stock -= 1
    
    session.commit()
    session.refresh(db_sale)
    return db_sale

@app.get("/sales/", response_model=List[SaleOut])
def read_sales(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    sales = session.exec(select(Sale).offset(skip).limit(limit)).all()
    return sales

@app.get("/sales/{sale_id}", response_model=SaleOut)
def read_sale(sale_id: int, session: Session = Depends(get_session)):
    sale = session.get(Sale, sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    return sale

@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, session: Session = Depends(get_session)):
    sale = session.get(Sale, sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")
    
    # Restore stock when sale is deleted
    product = session.get(Product, sale.product_id)
    if product:
        product.stock += 1
    
    session.delete(sale)
    session.commit()
    return {"message": "Sale deleted successfully"}