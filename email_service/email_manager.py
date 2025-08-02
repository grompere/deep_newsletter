import os
from typing import Optional
from jinja2 import Template
from .base import EmailService, EmailContent, EmailConfig
from .resend_service import ResendEmailService
from config.settings import get_settings
from config.email_config import print_email_setup_instructions
from pydantic import ValidationError


class EmailManager:
    """Manages email sending with template rendering"""
    
    def __init__(self):
        self.email_service: Optional[EmailService] = None
        self.recipient_email: Optional[str] = None
        self._initialize_email_service()
    
    def _initialize_email_service(self):
        """Initialize the email service if configuration is available"""
        try:
            settings = get_settings()
            email_settings = settings.email
            
            # Check if email is properly configured
            if email_settings.is_configured():
                # Create EmailConfig from pydantic settings
                config = EmailConfig(
                    api_key=email_settings.resend_api_key,
                    from_email=email_settings.from_email,
                    from_name=email_settings.from_name
                )
                
                self.email_service = ResendEmailService(config)
                self.recipient_email = email_settings.to_email
                
        except ValidationError as e:
            # If validation fails, email service remains None
            print(f"📧 Email configuration validation failed: {e}")
        except Exception as e:
            # Handle any other configuration errors
            print(f"📧 Error initializing email service: {e}")
    
    def is_available(self) -> bool:
        """Check if email service is available"""
        return self.email_service is not None and self.recipient_email is not None
    
    def test_connection(self) -> bool:
        """Test the email service connection"""
        if not self.email_service:
            return False
        return self.email_service.test_connection()
    
    def _load_template(self) -> Template:
        """Load the HTML email template"""
        template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', 'email_template.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        return Template(template_content)
    
    def send_research_report(self, topic: str, date: str, content: str) -> bool:
        """
        Send a research report via email
        
        Args:
            topic: The research topic
            date: The research date
            content: The research content (HTML formatted)
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        if not self.is_available():
            print("Email service not configured. Skipping email notification.")
            return False
        
        try:
            # Load and render template
            template = self._load_template()
            html_content = template.render(
                topic=topic,
                date=date,
                content=content,
                subject=f"Deep Research Report: {topic}"
            )
            
            # Create email content
            email_content = EmailContent(
                subject=f"🔍 Deep Research Report: {topic}",
                html_content=html_content,
                text_content=self._html_to_text(content)
            )
            
            # Send email
            success = self.email_service.send_email(self.recipient_email, email_content)
            
            if success:
                print(f"✅ Research report sent to {self.recipient_email}")
            else:
                print("❌ Failed to send email notification")
            
            return success
            
        except Exception as e:
            print(f"❌ Error sending email: {e}")
            return False
    
    def _html_to_text(self, html_content: str) -> str:
        """
        Convert HTML content to plain text for email fallback
        
        Args:
            html_content: HTML formatted content
            
        Returns:
            str: Plain text version of the content
        """
        # Simple HTML to text conversion
        import re
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', html_content)
        
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text)
        text = text.strip()
        
        return text 