from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from dataclasses import dataclass


@dataclass
class EmailConfig:
    """Configuration for email service"""
    api_key: str
    from_email: str
    from_name: Optional[str] = None


@dataclass
class EmailContent:
    """Email content structure"""
    subject: str
    html_content: str
    text_content: Optional[str] = None


class EmailService(ABC):
    """Abstract base class for email services"""
    
    def __init__(self, config: EmailConfig):
        self.config = config
    
    @abstractmethod
    def send_email(self, to_email: str, content: EmailContent) -> bool:
        """
        Send an email using the configured service
        
        Args:
            to_email: Recipient email address
            content: Email content including subject and body
            
        Returns:
            bool: True if email sent successfully, False otherwise
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test the connection to the email service
        
        Returns:
            bool: True if connection successful, False otherwise
        """
        pass 