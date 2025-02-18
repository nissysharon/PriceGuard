
# app/prometheus.py
from prometheus_client import start_http_server, Gauge
import time
from app.database import SessionLocal
from app.models import Product
import logging

price_gauge = Gauge('product_price', 'Price of the product', ['product_name'])

logger = logging.getLogger(__name__)

def start_prometheus():
    start_http_server(8001)
    logger.info("Prometheus server started on port 8001")
    while True:
        try:
            db = SessionLocal()
            products = db.query(Product).all()
            for product in products:
                price_gauge.labels(product_name=product.title).set(product.current_price)
            time.sleep(60)  # sleep for a minute between updates
        except Exception as e:
            logger.error(f"Error in Prometheus data collection: {e}")
