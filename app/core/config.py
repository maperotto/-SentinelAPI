from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    monitor_interval: int = 60
    request_timeout: int = 10
    max_retries: int = 3
    
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    
    discord_webhook_url: str = ""
    
    smtp_host: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    alert_email: str = ""


settings = Settings()
