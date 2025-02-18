from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import Product, PriceHistory
from app.scraper import scrape_price
from app.logging_config import setup_logging
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="PriceGuard API")

# Add CORS middleware to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to PriceGuard API"}

# Endpoint to retrieve all products
@app.get("/products")
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [{"id": product.id, "title": product.title, "current_price": product.current_price, "last_checked": product.last_checked} for product in products]

# Endpoint to retrieve a specific product by ID
@app.get("/product/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {
        "id": product.id,
        "title": product.title,
        "current_price": product.current_price,
        "url": product.url,
        "last_checked": product.last_checked,
    }

# Endpoint to scrape products from URLs
class ProductURLs(BaseModel):
    urls: List[str]

@app.post("/scrape-products")
async def scrape_multiple_products(data: ProductURLs, db: Session = Depends(get_db)):
    all_products = []
    for url in data.urls:
        try:
            title, price = scrape_price(url)
            if title and price:
                existing_product = db.query(Product).filter(Product.url == url).first()
                if existing_product:
                    existing_product.current_price = price
                    existing_product.last_checked = datetime.utcnow()  # Update last_checked field
                    logger.info(f"Updated product: {title} with new price: £{price}")
                    product_data = {"id": existing_product.id, "title": existing_product.title, "current_price": existing_product.current_price, "last_checked": existing_product.last_checked}
                else:
                    product = Product(title=title, url=url, current_price=price, last_checked=datetime.utcnow())  # Set last_checked when adding a new product
                    db.add(product)
                    logger.info(f"Added new product: {title} with price: £{price}")
                    db.commit()
                    product_data = {"id": product.id, "title": product.title, "current_price": product.current_price, "last_checked": product.last_checked}
                all_products.append(product_data)
        except Exception as e:
            logger.error(f"Error scraping {url}: {e}")
    return {"message": "Products scraped successfully", "products": all_products}

# Endpoint to retrieve price history for a product
@app.get("/product/{product_id}/price-history")
def get_price_history(product_id: int, db: Session = Depends(get_db)):
    price_history = db.query(PriceHistory).filter(PriceHistory.product_id == product_id).all()
    if not price_history:
        raise HTTPException(status_code=404, detail="Price history not found")
    return [{"timestamp": ph.timestamp, "price": ph.price} for ph in price_history]
