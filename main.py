import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('housing_monitor.log'),
        logging.StreamHandler()
    ]
)

# Email credentials
EMAIL_SENDER = "fasihmuhammad.virk@gmail.com"
EMAIL_PASSWORD = "ykqagdafqstnkcel"  # For Gmail, generate an App Password
EMAIL_RECEIVER = "fasihmuhammad.virk@gmail.com"

# STWDO housing page
URL = ("https://www.stwdo.de/en/living-houses-application/"
       "current-housing-offers")

# Only send once per new offer appearance
notified = False


def check_housing_offers():
    """Check for new housing offers and send email alert if found."""
    global notified
    logging.info("🔍 Checking housing offers...")

    try:
        # Add timeout and headers to prevent hanging
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()  # Raise exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the "no results" notice exists
        no_results = soup.find("div", class_="notification__header")

        if no_results and "No results" in no_results.text:
            logging.info("❌ No offers available.")
            notified = False  # Reset so the next listing triggers alert
        else:
            if not notified:
                subject = "📢 New Housing Offer Found"
                body = f"Visit the housing portal: {URL}"
                send_email_alert(subject, body)
                logging.info("✅ Email alert sent.")
                notified = True
            else:
                logging.info("ℹ️ Offer exists, already notified.")

    except requests.exceptions.RequestException as e:
        logging.error(f"⚠️ Network error: {e}")
    except Exception as e:
        logging.error(f"⚠️ Unexpected error: {e}")


def send_email_alert(subject, body):
    """Send email alert with error handling."""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_SENDER
    msg['To'] = EMAIL_RECEIVER
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=30)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        logging.info("📧 Email sent successfully")
    except smtplib.SMTPAuthenticationError:
        logging.error("⚠️ Email authentication failed. Check credentials.")
    except smtplib.SMTPException as e:
        logging.error(f"⚠️ SMTP error: {e}")
    except Exception as e:
        logging.error(f"⚠️ Failed to send email: {e}")


def main():
    """Main function to run the monitoring loop."""
    logging.info("🚀 Housing monitor started...")
    logging.info(f"Monitoring URL: {URL}")
    logging.info("Running every 30 seconds...")
    
    # Schedule the job to run every 30 seconds
    schedule.every(30).seconds.do(check_housing_offers)
    
    # Run initial check
    check_housing_offers()
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("🛑 Monitoring stopped by user.")
    except Exception as e:
        logging.error(f"🛑 Unexpected error in main loop: {e}")


if __name__ == "__main__":
    main()
