'''# app/routes.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product
import logging

logger = logging.getLogger(__name__)

@app.get("/products")
def read_products(db: Session = Depends(get_db)):
    logger.info("Fetching all products")
    products = db.query(Product).all()
    return products

@app.post("/products")
def create_product(product: Product, db: Session = Depends(get_db)):
    logger.info(f"Creating product: {product.title}")
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
'''