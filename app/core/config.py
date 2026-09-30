from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ollama_model: str = "gemma4:e4b"
    ollama_base_url: str = "http://localhost:11434"
    database_url: str = "sqlite:///chat.db"
    max_history_tokens: int = 2000

    class Config:
        env_file = ".env"

settings = Settings()