import resend
from typing import Optional
from .base import EmailService, EmailConfig, EmailContent


class ResendEmailService(EmailService):
    """Resend email service implementation"""
    
    def __init__(self, config: EmailConfig):
        super().__init__(config)
        resend.api_key = config.api_key
    
    def send_email(self, to_email: str, content: EmailContent) -> bool:
        """
        Send an email using Resend
        
        Args:
            to_email: Recipient email address
            content: Email content including subject and body
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        try:
            params = {
                "from": self.config.from_email,
                "to": [to_email],
                "subject": content.subject,
                "html": content.html_content,
            }
            
            # Add text content if provided
            if content.text_content:
                params["text"] = content.text_content
            
            # Add from name if provided
            if self.config.from_name:
                params["from"] = f"{self.config.from_name} <{self.config.from_email}>"
            
            response = resend.Emails.send(params)
            
            # Check if email was sent successfully
            # The response is a dictionary with an 'id' key
            if isinstance(response, dict) and response.get('id'):
                return True
            return False
            
        except Exception as e:
            print(f"Error sending email via Resend: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        Test the connection to Resend by checking if API key is set
        
        Returns:
            bool: True if API key is configured, False otherwise
        """
        try:
            # Check if API key is set
            if not resend.api_key:
                print("Resend API key not configured")
                return False
            
            # For now, just verify the API key is set
            # The actual email sending will be tested in the main test
            print("✅ Resend API key is configured")
            return True
            
        except Exception as e:
            print(f"Error testing Resend connection: {e}")
            return False 