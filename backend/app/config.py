from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # General settings
    PROJECT_NAME: str = "FastAPI DDD Example"
    API_V1_STR: str = "/api/v1"

    # Database settings
    DATABASE_URL: str

    # Security settings
    SECURITY_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


settings = Settings()
