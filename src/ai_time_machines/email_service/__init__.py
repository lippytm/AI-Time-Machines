"""Email notification service for AI Time Machines."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from loguru import logger

from ..config import config


class EmailService:
    """Email notification service."""

    def __init__(self):
        """Initialize email service."""
        self.smtp_server = config.email.smtp_server
        self.smtp_port = config.email.smtp_port
        self.use_tls = config.email.use_tls
        self.email_address = config.email.email_address
        self.password = config.email.password

        if not self.password:
            logger.warning("Email password not configured - email notifications will be disabled")

    def send_email(self, to_addresses: List[str], subject: str, body: str, 
                   html_body: Optional[str] = None) -> bool:
        """Send an email notification."""
        if not self.password:
            logger.warning("Email not configured - skipping notification")
            return False

        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = self.email_address
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = subject

            # Add text part
            text_part = MIMEText(body, 'plain')
            msg.attach(text_part)

            # Add HTML part if provided
            if html_body:
                html_part = MIMEText(html_body, 'html')
                msg.attach(html_part)

            # Connect to server and send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.email_address, self.password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {', '.join(to_addresses)}")
            return True

        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            return False

    def send_github_event_notification(self, event_type: str, event_data: dict, 
                                     recipients: Optional[List[str]] = None) -> bool:
        """Send notification for GitHub events."""
        recipients = recipients or [self.email_address]
        
        subject = f"AI Time Machines - GitHub {event_type.title()} Event"
        
        # Create text body
        body = f"""
AI Time Machines GitHub Event Notification

Event Type: {event_type}
Repository: {event_data.get('repository', 'Unknown')}
Time: {event_data.get('timestamp', 'Unknown')}

Details:
{self._format_event_details(event_data)}

---
This is an automated notification from AI Time Machines.
        """.strip()

        # Create HTML body
        html_body = f"""
<html>
<body>
    <h2>AI Time Machines - GitHub Event Notification</h2>
    
    <p><strong>Event Type:</strong> {event_type}</p>
    <p><strong>Repository:</strong> {event_data.get('repository', 'Unknown')}</p>
    <p><strong>Time:</strong> {event_data.get('timestamp', 'Unknown')}</p>
    
    <h3>Details:</h3>
    <pre>{self._format_event_details(event_data)}</pre>
    
    <hr>
    <p><em>This is an automated notification from AI Time Machines.</em></p>
</body>
</html>
        """.strip()

        return self.send_email(recipients, subject, body, html_body)

    def send_error_notification(self, error_message: str, error_details: Optional[str] = None,
                               recipients: Optional[List[str]] = None) -> bool:
        """Send notification for errors."""
        recipients = recipients or [self.email_address]
        
        subject = "AI Time Machines - Error Alert"
        
        body = f"""
AI Time Machines Error Alert

Error Message: {error_message}

{f"Error Details: {error_details}" if error_details else ""}

Please check the application logs for more information.

---
This is an automated error notification from AI Time Machines.
        """.strip()

        html_body = f"""
<html>
<body>
    <h2 style="color: red;">AI Time Machines - Error Alert</h2>
    
    <p><strong>Error Message:</strong> {error_message}</p>
    
    {f"<p><strong>Error Details:</strong></p><pre>{error_details}</pre>" if error_details else ""}
    
    <p>Please check the application logs for more information.</p>
    
    <hr>
    <p><em>This is an automated error notification from AI Time Machines.</em></p>
</body>
</html>
        """.strip()

        return self.send_email(recipients, subject, body, html_body)

    def send_ai_response_notification(self, query: str, response: str, 
                                    github_action: Optional[str] = None,
                                    recipients: Optional[List[str]] = None) -> bool:
        """Send notification for AI responses and actions."""
        recipients = recipients or [self.email_address]
        
        subject = "AI Time Machines - AI Response"
        
        body = f"""
AI Time Machines - AI Response Notification

Query: {query}

AI Response: {response}

{f"GitHub Action Taken: {github_action}" if github_action else ""}

---
This is an automated notification from AI Time Machines.
        """.strip()

        html_body = f"""
<html>
<body>
    <h2>AI Time Machines - AI Response</h2>
    
    <p><strong>Query:</strong> {query}</p>
    
    <p><strong>AI Response:</strong></p>
    <blockquote>{response}</blockquote>
    
    {f"<p><strong>GitHub Action Taken:</strong> {github_action}</p>" if github_action else ""}
    
    <hr>
    <p><em>This is an automated notification from AI Time Machines.</em></p>
</body>
</html>
        """.strip()

        return self.send_email(recipients, subject, body, html_body)

    def _format_event_details(self, event_data: dict) -> str:
        """Format event details for display."""
        formatted_details = []
        for key, value in event_data.items():
            if key not in ['repository', 'timestamp']:
                formatted_details.append(f"{key}: {value}")
        return '\n'.join(formatted_details) if formatted_details else "No additional details"

    def test_connection(self) -> bool:
        """Test email service connection."""
        return self.send_email(
            to_addresses=[self.email_address],
            subject="AI Time Machines - Email Service Test",
            body="This is a test email to verify the email service is working correctly."
        )