from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from typing import List
from .models import (
    Product, ProductCreate, ProductOut,MostSoldItem,
    Sale, SaleCreate, SaleOut,
    engine, create_db_and_tables,
    MessageInput,
)
from .agent.ai_agent import AIAgent
from fastapi.middleware.cors import CORSMiddleware

    
app = FastAPI(title="Soda AI API", version="1.0.0")
agent = AIAgent()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_session():
    with Session(engine) as session:
        yield session

@app.on_event("startup")
async def startup_event():
    create_db_and_tables()


@app.post("/ask")
def ask(message_input: MessageInput):
    try:
        response = agent.handle_message(message_input.message)
        return {"response": response}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Sorry, i cant answer your question right now, please try again")

@app.post("/products/", response_model=ProductOut)
def create_product(product: ProductCreate, session: Session = Depends(get_session)):
    product_name_lower = product.name.lower()
    existing_product = session.exec(select(Product).where(Product.name == product_name_lower)).first()
    if existing_product:
        existing_product.stock += product.stock
        existing_product.price = product.price
        session.add(existing_product)
        session.commit()
        session.refresh(existing_product)
        return existing_product
    else:
        db_product = Product.from_orm(product)
        db_product.name = product_name_lower
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


@app.post("/sales/", response_model=List[SaleOut])
def create_sale(sale: SaleCreate, session: Session = Depends(get_session)):
    product = session.exec(select(Product).where(Product.name == sale.product_name)).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if sale.quantity <= 0:
        raise HTTPException(status_code=400, detail="Quantity must be greater than zero")
    if product.stock < sale.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock to fulfill the sale")
    sales = []
    for _ in range(sale.quantity):
        db_sale = Sale(product_id=product.id)
        session.add(db_sale)
        sales.append(db_sale)
    product.stock -= sale.quantity
    session.commit()
    for db_sale in sales:
        session.refresh(db_sale)
    return [
        SaleOut(id=db_sale.id, product_name=product.name, timestamp=db_sale.timestamp)
        for db_sale in sales
    ]

@app.get("/sales/", response_model=List[SaleOut])
def read_sales(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    sales = session.exec(select(Sale).offset(skip).limit(limit)).all()
    product_map = {p.id: p.name for p in session.exec(select(Product)).all()}
    return [
        SaleOut(id=sale.id, product_name=product_map.get(sale.product_id, "Unknown"), timestamp=sale.timestamp)
        for sale in sales
    ]

@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, session: Session = Depends(get_session)):
    sale = session.get(Sale, sale_id)
    if sale is None:
        raise HTTPException(status_code=404, detail="Sale not found")  
    product = session.get(Product, sale.product_id)
    if product:
        product.stock += 1
    session.delete(sale)
    session.commit()
    return {"message": "Sale deleted successfully"}

@app.get("/sales/history/", response_model=List[SaleOut])
def sale_history(session: Session = Depends(get_session)):
    sales = session.exec(select(Sale)).all()
    product_map = {p.id: p.name for p in session.exec(select(Product)).all()}
    return [
        SaleOut(id=sale.id, product_name=product_map.get(sale.product_id, "Unknown"), timestamp=sale.timestamp)
        for sale in sales
    ]
@app.get("/sales/most_sold/", response_model=List[MostSoldItem])
def most_sold_items(session: Session = Depends(get_session)):
    from collections import Counter
    sales = session.exec(select(Sale)).all()
    product_map = {p.id: p.name for p in session.exec(select(Product)).all()}
    counter = Counter(sale.product_id for sale in sales)
    most_sold = [
        MostSoldItem(product_name=product_map.get(pid, "Unknown"), total_sold=count)
        for pid, count in counter.most_common()
    ]
    return most_sold