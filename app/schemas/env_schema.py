from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    POSTGRES_USER: str 
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str 
    POSTGRES_HOST: str 
    POSTGRES_PORT: int
    CRYPTO_API_KEY: str 
    GEMINI_API_KEY: str
    API_BASE_URL: str
    LANGFUSE_SECRET_KEY: str 
    LANGFUSE_PUBLIC_KEY: str 
    LANGFUSE_BASE_URL: str

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()




