import os
from typing import Optional
from email_service.base import EmailConfig


def get_email_config() -> Optional[EmailConfig]:
    """
    Get email configuration from environment variables
    
    Returns:
        EmailConfig if all required variables are set, None otherwise
    """
    api_key = os.getenv("RESEND_API_KEY")
    from_email = os.getenv("EMAIL_FROM")
    from_name = os.getenv("EMAIL_FROM_NAME")
    
    if not api_key or not from_email:
        return None
    
    return EmailConfig(
        api_key=api_key,
        from_email=from_email,
        from_name=from_name
    )


def get_recipient_email() -> Optional[str]:
    """
    Get recipient email from environment variables
    
    Returns:
        str: Recipient email address if set, None otherwise
    """
    return os.getenv("EMAIL_TO")


def is_email_enabled() -> bool:
    """
    Check if email functionality is enabled
    
    Returns:
        bool: True if email configuration is complete, False otherwise
    """
    config = get_email_config()
    recipient = get_recipient_email()
    return config is not None and recipient is not None


def print_email_setup_instructions():
    """Print instructions for setting up email functionality"""
    print("\n" + "="*60)
    print("EMAIL SETUP INSTRUCTIONS")
    print("="*60)
    print("To enable email notifications, add the following to your .env file:")
    print()
    print("RESEND_API_KEY=your_resend_api_key_here")
    print("EMAIL_FROM=your-verified-email@domain.com")
    print("EMAIL_FROM_NAME=Deep Research Bot (optional)")
    print("EMAIL_TO=recipient@example.com")
    print()
    print("Steps to get your Resend API key:")
    print("1. Sign up at https://resend.com")
    print("2. Verify your domain or use the sandbox domain")
    print("3. Go to API Keys section and create a new key")
    print("4. Add the key to your .env file")
    print("="*60)
    print() 