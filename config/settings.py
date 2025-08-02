"""
Pydantic-based configuration management for the Deep Newsletter application.
Handles environment variables with validation and type safety.
"""

from typing import Optional
from functools import cached_property
from pydantic import Field, EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict

# Shared configuration to reduce repetition
_BASE_CONFIG = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
    case_sensitive=False,
    extra="ignore"
)


class OpenAISettings(BaseSettings):
    """OpenAI API configuration"""
    api_key: str = Field(..., description="OpenAI API key for deep research functionality")
    
    model_config = SettingsConfigDict(
        **_BASE_CONFIG,
        env_prefix="OPENAI_"
    )


class GoogleSettings(BaseSettings):
    """Google API configuration"""
    api_key: Optional[str] = Field(None, description="Google Gemini API key for search bot functionality")
    
    model_config = SettingsConfigDict(
        **_BASE_CONFIG,
        env_prefix="GOOGLE_"
    )


class NewsAPISettings(BaseSettings):
    """News API configuration"""
    api_key: Optional[str] = Field(None, description="News API key for search bot functionality")
    
    model_config = SettingsConfigDict(
        **_BASE_CONFIG,
        env_prefix="NEWS_API_"
    )


class EmailSettings(BaseSettings):
    """Email service configuration"""
    resend_api_key: Optional[str] = Field(
        None, 
        env="RESEND_API_KEY",
        description="Resend API key for email notifications"
    )
    from_email: str = Field(
        "onboarding@resend.dev",
        env="EMAIL_FROM", 
        description="From email address"
    )
    from_name: str = Field(
        "Deep Research Bot",
        env="EMAIL_FROM_NAME",
        description="From name for emails"
    )
    to_email: str = Field(
        "zsolt.mrtn@gmail.com",
        env="EMAIL_TO",
        description="Recipient email address"
    )
    
    model_config = _BASE_CONFIG
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return bool(self.resend_api_key and self.from_email and self.to_email)


class AppSettings(BaseSettings):
    """Main application settings that combines all configurations"""
    
    environment: str = Field("development", description="Application environment")
    debug: bool = Field(False, description="Enable debug mode")
    
    model_config = _BASE_CONFIG
    
    @cached_property
    def openai(self) -> OpenAISettings:
        """Lazy-loaded OpenAI settings"""
        return OpenAISettings()
    
    @cached_property
    def google(self) -> GoogleSettings:
        """Lazy-loaded Google settings"""
        return GoogleSettings()
    
    @cached_property
    def news_api(self) -> NewsAPISettings:
        """Lazy-loaded News API settings"""
        return NewsAPISettings()
    
    @cached_property
    def email(self) -> EmailSettings:
        """Lazy-loaded Email settings"""
        return EmailSettings()


# Singleton instance
_settings_instance: Optional[AppSettings] = None

def get_settings() -> AppSettings:
    """Get the global settings instance"""
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = AppSettings()
    return _settings_instance 