import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging

logger = logging.getLogger(__name__)

def send_alert_email(product_name: str, old_price: float, new_price: float):
    msg = MIMEMultipart()
    msg['From'] = "youremail@example.com"
    msg['To'] = "user@example.com"
    msg['Subject'] = f"Price Drop Alert for {product_name}"
    
    body = f"The price of {product_name} has dropped from £{old_price} to £{new_price}."
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        with smtplib.SMTP('smtp.example.com', 587) as server:
            server.starttls()
            server.login("youremail@example.com", "yourpassword")
            text = msg.as_string()
            server.sendmail(msg['From'], msg['To'], text)
        logger.info(f"Alert email sent for {product_name}")
    except Exception as e:
        logger.error(f"Failed to send alert email for {product_name}: {e}")
