"""
Configuracion centralizada de la app, cargada desde variables de entorno.
Todo lo que necesite un secreto o algo configurable por ambiente vive aqui,
no hardcodeado en el resto del codigo.
"""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    supabase_url: str
    supabase_key: str

    anthropic_api_key: str
    llm_model: str = "claude-sonnet-5"

    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000"

    class Config:
        env_file = ".env"


settings = Settings()
