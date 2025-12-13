#!/usr/bin/env python3
"""
Email Agent - Automated email handling with Gmail, Webshop, and ChatGPT integration
"""

import os
import re
import imaplib
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from email_config import (
    EMAIL_USER,
    EMAIL_PASS,
    IMAP_SERVER,
    IMAP_PORT,
    SMTP_SERVER,
    SMTP_PORT
)

# Create logs directory if it doesn't exist
os.makedirs('logs', exist_ok=True)

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
        mail = None
        try:
            mail = self.connect_imap()
            mail.select('inbox')
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                logger.error(f"IMAP search failed with status: {status}")
                return []
            
            if not messages[0]:
                logger.info("No unread emails found")
                return []
            
            email_ids = messages[0].split()
            logger.info(f"Found {len(email_ids)} unread emails")
            
            emails = []
            for email_id in email_ids:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status != 'OK' or not msg_data or not msg_data[0]:
                    logger.warning(f"Failed to fetch email {email_id}, skipping")
                    continue
                msg = email.message_from_bytes(msg_data[0][1])
                emails.append(msg)
            
            return emails
        except Exception as e:
            logger.error(f"Failed to fetch unread emails: {e}")
            raise
        finally:
            if mail:
                try:
                    mail.close()
                    mail.logout()
                except Exception as e:
                    logger.warning(f"Error closing IMAP connection: {e}")
    
    def send_email(self, to_address, subject, body, html=False):
        """Send an email
        
        Args:
            to_address: Recipient email address
            subject: Email subject
            body: Email body (can be plain text or HTML)
            html: If True, sends both plain text and HTML versions
        """
        server = None
        try:
            if html:
                # For HTML emails, send both plain text and HTML for better compatibility
                msg = MIMEMultipart('alternative')
                # Create plain text version (strip HTML tags for simple conversion)
                plain_text = re.sub('<[^<]+?>', '', body)
                msg.attach(MIMEText(plain_text, 'plain'))
                msg.attach(MIMEText(body, 'html'))
            else:
                # For plain text emails, use simple MIMEText
                msg = MIMEText(body, 'plain')
            
            msg['From'] = self.email_user
            msg['To'] = to_address
            msg['Subject'] = subject
            
            server = self.connect_smtp()
            server.send_message(msg)
            
            logger.info(f"Successfully sent email to {to_address}")
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            raise
        finally:
            if server:
                try:
                    server.quit()
                except Exception as e:
                    logger.warning(f"Error closing SMTP connection: {e}")
    
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
    try:
        agent = EmailAgent()
        agent.run()
    except Exception as e:
        logger.error(f"Email Agent failed to start: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
