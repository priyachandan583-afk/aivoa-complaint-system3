from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:postgres@localhost:5432/aivoa_complaints"
    groq_api_key: str = ""
    groq_extraction_model: str = "gemma2-9b-it"
    groq_context_model: str = "llama-3.3-70b-versatile"
    frontend_origin: str = "http://localhost:5173"

    class Config:
        env_file = ".env"


settings = Settings()
