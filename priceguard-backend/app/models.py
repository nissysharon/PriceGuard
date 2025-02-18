from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement is set
    title = Column(String, unique=True, index=True)
    url = Column(String, unique=True)
    current_price = Column(Float)
    last_checked = Column(DateTime, default=datetime.utcnow)  # New column for last checked timestamp
    price_history = relationship("PriceHistory", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, title={self.title}, current_price={self.current_price}, last_checked={self.last_checked})>"

class PriceHistory(Base):
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)  # Ensure autoincrement is set
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    product = relationship("Product", back_populates="price_history")

    def __repr__(self):
        return f"<PriceHistory(product_id={self.product_id}, price={self.price}, timestamp={self.timestamp})>"
