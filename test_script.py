#!/usr/bin/env python3
"""
Test script for housing monitor functionality.
This script tests the core functions without sending actual emails.
"""

import requests
from bs4 import BeautifulSoup
import logging

# Configure logging for testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Test URL
URL = ("https://www.stwdo.de/en/living-houses-application/"
       "current-housing-offers")


def test_website_access():
    """Test if we can access the housing website."""
    logging.info("🔍 Testing website access...")
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(URL, headers=headers, timeout=30)
        response.raise_for_status()
        
        logging.info(f"✅ Website accessible. Status code: {response.status_code}")
        logging.info(f"✅ Response size: {len(response.text)} characters")
        
        return True, response.text
        
    except requests.exceptions.RequestException as e:
        logging.error(f"❌ Website access failed: {e}")
        return False, None


def test_parsing_logic(html_content):
    """Test the HTML parsing logic."""
    logging.info("🔍 Testing HTML parsing...")
    
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Check if the "no results" notice exists
        no_results = soup.find("div", class_="notification__header")
        
        if no_results and "No results" in no_results.text:
            logging.info("✅ Parsing logic works: No results detected")
            return True, "no_results"
        else:
            logging.info("✅ Parsing logic works: Results detected")
            return True, "has_results"
            
    except Exception as e:
        logging.error(f"❌ Parsing failed: {e}")
        return False, None


def test_email_credentials():
    """Test email credentials without sending."""
    logging.info("🔍 Testing email credentials...")
    
    try:
        import smtplib
        
        # Test credentials (don't send actual email)
        EMAIL_SENDER = "fasihmuhammad.virk@gmail.com"
        EMAIL_PASSWORD = "ykqagdafqstnkcel"
        
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465, timeout=10)
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.quit()
        
        logging.info("✅ Email credentials are valid")
        return True
        
    except smtplib.SMTPAuthenticationError:
        logging.error("❌ Email authentication failed. Check credentials.")
        return False
    except Exception as e:
        logging.error(f"❌ Email test failed: {e}")
        return False


def main():
    """Run all tests."""
    logging.info("🚀 Starting housing monitor tests...")
    
    # Test 1: Website access
    success, html_content = test_website_access()
    if not success:
        logging.error("❌ Website access test failed. Cannot proceed.")
        return
    
    # Test 2: HTML parsing
    success, result_type = test_parsing_logic(html_content)
    if not success:
        logging.error("❌ HTML parsing test failed.")
        return
    
    # Test 3: Email credentials
    success = test_email_credentials()
    if not success:
        logging.error("❌ Email credentials test failed.")
        return
    
    logging.info("🎉 All tests passed! The script should work correctly.")
    logging.info(f"Current housing status: {result_type}")


if __name__ == "__main__":
    main() 