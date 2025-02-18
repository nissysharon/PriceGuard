import httpx
from bs4 import BeautifulSoup
from app.database import SessionLocal
from app.models import Product, PriceHistory
import logging
from app.alerts import send_alert_email  # Import from alerts.py

logger = logging.getLogger(__name__)

BASE_URL = "http://books.toscrape.com"

def scrape_price(url: str):
    """Scrape a product's price from a single URL."""
    response = httpx.get(url)
    if response.status_code != 200:
        logger.error(f"Failed to fetch {url}")
        return None, None

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.find("h1").text.strip()
    price = soup.find("p", class_="price_color").text.strip()
    price = float(price.replace("£", ""))  # Convert price to float

    return title, price

def scrape_multiple_products(urls: list[str]):
    """Scrape prices for a list of product URLs and add them to the database."""
    all_products = []  # List to store product details
    for url in urls:
        title, price = scrape_price(url)
        if title and price:
            db = SessionLocal()
            # Check if the product already exists in the database
            existing_product = db.query(Product).filter(Product.url == url).first()
            if existing_product:
                # Update price for existing product
                existing_product.current_price = price
                existing_product.last_checked = datetime.utcnow()  # Update last_checked timestamp
                db.commit()
                db.refresh(existing_product)
                logger.info(f"Updated product: {title} with new price: £{price}")
                all_products.append({"id": existing_product.id, "title": existing_product.title, "current_price": existing_product.current_price})
            else:
                # Create new product in the database
                product = Product(title=title, url=url, current_price=price, last_checked=datetime.utcnow())  # Set last_checked when adding a new product
                db.add(product)
                db.commit()
                db.refresh(product)
                logger.info(f"Added new product: {title} with price: £{price}")
                all_products.append({"id": product.id, "title": product.title, "current_price": product.current_price})
            db.close()

    return all_products  # Return the list of scraped product data
