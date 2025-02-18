from celery import Celery
from app.models import Product, PriceHistory
from app.database import SessionLocal
from celery.schedules import crontab
import logging
from app.alerts import send_alert_email  # Import from alerts.py
from app.scraper import scrape_price  # Import scrape_price from scraper

app = Celery('priceguard', broker='redis://priceguard-redis:6379/0')

logger = logging.getLogger(__name__)

@app.task
def scrape_and_store_price(url: str, product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()

        if product:
            title, price = scrape_price(url)
            if price:
                if price < product.current_price:
                    logger.info(f"Price drop detected for {title}: {product.current_price} -> {price}")
                    send_alert_email(title, product.current_price, price)

                product.current_price = price
                db.commit()

                price_history = PriceHistory(product_id=product.id, price=price)
                db.add(price_history)
                db.commit()

    except Exception as e:
        logger.error(f"Error in scrape_and_store_price: {e}")
    finally:
        db.close()


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=0),  # Update prices daily at midnight
        scrape_and_store_price.s()
    )
