import requests
from bs4 import BeautifulSoup
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime
from flask import Flask, jsonify
import threading
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('housing_monitor.log'),
        logging.StreamHandler()
    ]
)

# Flask app setup
app = Flask(__name__)

# Global variables for monitoring
monitoring_stats = {
    'last_check': None,
    'total_checks': 0,
    'offers_found': 0,
    'emails_sent': 0,
    'last_error': None,
    'is_running': True
}

# Email credentials
EMAIL_SENDER = "fasihmuhammad.virk@gmail.com"
EMAIL_PASSWORD = "ykqagdafqstnkcel"  # For Gmail, generate an App Password
EMAIL_RECEIVER = "fasihmuhammad.virk@gmail.com"

# STWDO housing page
URL = ("https://www.stwdo.de/en/living-houses-application/"
       "current-housing-offers")

# Only send once per new offer appearance
notified = False


@app.route('/')
def home():
    """Home page for UptimeRobot monitoring."""
    return jsonify({
        'status': 'online',
        'service': 'Housing Monitor',
        'timestamp': datetime.now().isoformat(),
        'message': ('Housing monitor is running and checking for offers '
                    'every 30 seconds')
    })


@app.route('/health')
def health():
    """Health check endpoint for monitoring."""
    return jsonify({
        'status': 'healthy',
        'last_check': monitoring_stats['last_check'],
        'total_checks': monitoring_stats['total_checks'],
        'offers_found': monitoring_stats['offers_found'],
        'emails_sent': monitoring_stats['emails_sent'],
        'last_error': monitoring_stats['last_error'],
        'is_running': monitoring_stats['is_running']
    })


@app.route('/status')
def status():
    """Detailed status endpoint."""
    return jsonify({
        'service': 'STWDO Housing Monitor',
        'status': 'running' if monitoring_stats['is_running'] else 'stopped',
        'monitoring_url': URL,
        'check_interval': '30 seconds',
        'last_check': monitoring_stats['last_check'],
        'total_checks': monitoring_stats['total_checks'],
        'offers_found': monitoring_stats['offers_found'],
        'emails_sent': monitoring_stats['emails_sent'],
        'last_error': monitoring_stats['last_error'],
        'uptime': '24/7 monitoring active'
    })


def check_housing_offers():
    """Check for new housing offers and send email alert if found."""
    global notified
    logging.info("🔍 Checking housing offers...")
    
    # Update monitoring stats
    monitoring_stats['last_check'] = datetime.now().isoformat()
    monitoring_stats['total_checks'] += 1

    try:
        # Add timeout and headers to prevent hanging
        headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/91.0.4472.124 Safari/537.36'),
            'Accept': ('text/html,application/xhtml+xml,application/xml;'
                      'q=0.9,*/*;q=0.8'),
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Try different connection methods to handle proxy issues
        session = requests.Session()
        
        # Disable proxy if it's causing issues
        session.trust_env = False
        
        # Try with different timeout and retry settings
        response = session.get(
            URL, 
            headers=headers, 
            timeout=30,
            allow_redirects=True,
            verify=True
        )
        response.raise_for_status()  # Raise exception for bad status codes
        
        soup = BeautifulSoup(response.text, 'html.parser')

        # Check if the "no results" notice exists
        # Look for the notification with "No results" in the header
        no_results_notification = soup.find(
            "div", class_="notification notification-info"
        )
        
        if no_results_notification:
            # Check if it contains "No results" in the header
            header = no_results_notification.find(
                "header", class_="notification__header"
            )
            if header and "No results" in header.text.strip():
                logging.info("❌ No offers available.")
                notified = False  # Reset so the next listing triggers alert
                monitoring_stats['last_error'] = None
            else:
                # Notification exists but doesn't say "No results" - offers available
                monitoring_stats['offers_found'] += 1
                if not notified:
                    subject = "📢 New Housing Offer Found"
                    body = f"Visit the housing portal: {URL}"
                    send_email_alert(subject, body)
                    logging.info("✅ Email alert sent.")
                    notified = True
                    monitoring_stats['emails_sent'] += 1
                else:
                    logging.info("ℹ️ Offer exists, already notified.")
                monitoring_stats['last_error'] = None
        else:
            # No notification div found - offers available
            monitoring_stats['offers_found'] += 1
            if not notified:
                subject = "📢 New Housing Offer Found"
                body = f"Visit the housing portal: {URL}"
                send_email_alert(subject, body)
                logging.info("✅ Email alert sent.")
                notified = True
                monitoring_stats['emails_sent'] += 1
            else:
                logging.info("ℹ️ Offer exists, already notified.")
            monitoring_stats['last_error'] = None

    except requests.exceptions.RequestException as e:
        error_msg = f"Network error: {e}"
        logging.error(f"⚠️ {error_msg}")
        monitoring_stats['last_error'] = error_msg
    except Exception as e:
        error_msg = f"Unexpected error: {e}"
        logging.error(f"⚠️ {error_msg}")
        monitoring_stats['last_error'] = error_msg


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


def run_flask_server():
    """Run Flask server in a separate thread."""
    port = int(os.environ.get('PORT', 8080))
    logging.info(f"🌐 Starting Flask server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)


def run_monitoring():
    """Run the monitoring loop."""
    logging.info("🚀 Housing monitor started...")
    logging.info(f"Monitoring URL: {URL}")
    logging.info("Running every 30 seconds...")
    
    # Schedule the job to run every 30 seconds
    schedule.every(30).seconds.do(check_housing_offers)
    
    # Run initial check
    check_housing_offers()
    
    try:
        while monitoring_stats['is_running']:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("🛑 Monitoring stopped by user.")
        monitoring_stats['is_running'] = False
    except Exception as e:
        logging.error(f"🛑 Unexpected error in main loop: {e}")
        monitoring_stats['is_running'] = False


def main():
    """Main function to start both Flask server and monitoring."""
    # Start Flask server in a separate thread
    flask_thread = threading.Thread(target=run_flask_server, daemon=True)
    flask_thread.start()
    
    # Give Flask server a moment to start
    time.sleep(2)
    
    # Start monitoring in the main thread
    run_monitoring()


if __name__ == "__main__":
    main()
