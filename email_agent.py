#!/usr/bin/env python3
"""
Email Agent - Automated email handling with Gmail, Webshop, and ChatGPT integration
"""

import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from datetime import datetime
from email_config import (
    EMAIL_USER,
    EMAIL_PASS,
    IMAP_SERVER,
    IMAP_PORT,
    SMTP_SERVER,
    SMTP_PORT
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/email_agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class EmailAgent:
    """Email Agent for automated email handling"""
    
    def __init__(self):
        """Initialize the Email Agent"""
        self.email_user = EMAIL_USER
        self.email_pass = EMAIL_PASS
        self.imap_server = IMAP_SERVER
        self.imap_port = IMAP_PORT
        self.smtp_server = SMTP_SERVER
        self.smtp_port = SMTP_PORT
        
        if not self.email_user or not self.email_pass:
            raise ValueError("EMAIL_USER and EMAIL_PASS must be set in .env file")
    
    def connect_imap(self):
        """Connect to IMAP server"""
        try:
            logger.info(f"Connecting to IMAP server: {self.imap_server}:{self.imap_port}")
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.email_user, self.email_pass)
            logger.info("Successfully connected to IMAP server")
            return mail
        except Exception as e:
            logger.error(f"Failed to connect to IMAP server: {e}")
            raise
    
    def connect_smtp(self):
        """Connect to SMTP server"""
        try:
            logger.info(f"Connecting to SMTP server: {self.smtp_server}:{self.smtp_port}")
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.email_user, self.email_pass)
            logger.info("Successfully connected to SMTP server")
            return server
        except Exception as e:
            logger.error(f"Failed to connect to SMTP server: {e}")
            raise
    
    def fetch_unread_emails(self):
        """Fetch unread emails from inbox"""
        try:
            mail = self.connect_imap()
            mail.select('inbox')
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            email_ids = messages[0].split()
            
            logger.info(f"Found {len(email_ids)} unread emails")
            
            emails = []
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append(msg)
            
            mail.close()
            mail.logout()
            
            return emails
        except Exception as e:
            logger.error(f"Failed to fetch unread emails: {e}")
            raise
    
    def send_email(self, to_address, subject, body, html=False):
        """Send an email"""
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_user
            msg['To'] = to_address
            msg['Subject'] = subject
            
            if html:
                msg.attach(MIMEText(body, 'html'))
            else:
                msg.attach(MIMEText(body, 'plain'))
            
            server = self.connect_smtp()
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Successfully sent email to {to_address}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
    
    def run(self):
        """Main run loop for the email agent"""
        logger.info("Email Agent started")
        
        try:
            # Fetch unread emails
            emails = self.fetch_unread_emails()
            
            for msg in emails:
                subject = msg.get('subject', 'No Subject')
                from_addr = msg.get('from', 'Unknown')
                logger.info(f"Processing email from {from_addr}: {subject}")
                
                # TODO: Add email processing logic here
                # - Analyze email content
                # - Integrate with ChatGPT for response generation
                # - Integrate with webshop API
                # - Send automated responses
        
        except Exception as e:
            logger.error(f"Error in email agent run loop: {e}")
            raise


def main():
    """Main entry point"""
    import os
    
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    try:
        agent = EmailAgent()
        agent.run()
    except Exception as e:
        logger.error(f"Email Agent failed to start: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
