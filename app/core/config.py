from pydantic import Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings,SettingsConfigDict
from typing import Literal
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"
    )
    
    
    
# --- Application -------------------------------------------------
    PROJECT_NAME: str = "Tailer Backend"
    ENVIRONMENT: Literal["development", "staging", "production", "test"] = "development"
    API_V1_PREFIX: str = "/api/v1"
    
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"
    LOG_FORMAT: Literal["console", "json"] = "console"
    
    CORS_ORIGINS: str = "http://localhost:3000"
    TRUSTED_HOSTS: str = "localhost,127.0.0.1"
    
# --- Database ------------------------------------------------------
    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    DATABASE_ECHO: bool = False
    
    
# --- Redis -----------------------------------------------------------
    REDIS_URL: RedisDsn
# --- JWT ---------------------------------------------------------------
    JWT_SECRET_KEY: str = Field(min_length=32)
    JWT_ALGORITHM:str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    JWT_ACCESS_TOKEN_EXPIRE_DAYS: int = 30
    
# --- Google OAuth ------------------------------------------------------
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_CLIENT_SECRET: str = ""
    GOOGLE_REDICRECT_URI: str = "http://localhost:8000/api/v1/auth/google/callback"
    
# --- Rate limiting -------------------------------------------------
    RATE_LIMIT_PER_MINUTE: int = 60
    LOGIN_RATE_LIMIT_PER_MINUTE: int = 5
    
    # @field_validator("JWT_SECRET_KEY")
    # @classmethod
    # def validate_secret_strength(cls, v:str) -> str:
    #     if v == "change-me-to-a-random-64-char-hex-string":
    #         raise ValueError(
    #             "JWT_SECRET_KEY is still the placeholder value. "
    #             "Generate one with `openssl rand -hex 32`."
    #         )
    #     return v
    
    @property
    def cors_origin_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    @property
    def trusted_hosts_list(self) -> list[str]:
        return [host.strip() for host in self.TRUSTED_HOSTS.split(",") if host.strip()]
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "production"

@lru_cache
def get_setting() -> Settings:
    """Return a cached Setting instance"""
    
    return Settings()
        
    