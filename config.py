from pydantic import Field
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    # Database connection string, e.g. sqlite+aiosqlite:///./app.db or postgres+asyncpg://user:pass@host/db
    DATABASE_URL: str = Field(..., env="DATABASE_URL")

    # Telegram Bot API token
    TELEGRAM_TOKEN: str = Field(..., env="TELEGRAM_TOKEN")

    # OpenFoodFacts API key and settings
    OPENFOOD_API_KEY: str = Field(..., env="OPENFOOD_API_KEY")
    OPENFOOD_CLIENT_KEY: str = Field(..., env="OPENFOOD_CLIENT_KEY")

    OPENFOOD_BASE_URL: str = Field(
        "https://world.openfoodfacts.org", env="OPENFOOD_BASE_URL"
    )

    API_DAILY_LIMIT: int = Field(5000, env="API_DAILY_LIMIT")

    # Bot behavior settings
    MAX_SEARCH_RESULTS: int = Field(10, env="MAX_SEARCH_RESULTS")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate settings
settings = Settings()