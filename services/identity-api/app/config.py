from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "APEX Identity API"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://apex:apex@db:5432/apex"
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    access_token_minutes: int = 15
    refresh_token_days: int = 30
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
