from functools import lru_cache
from pydantic import Field
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
   groq_api_key: str = Field(..., env="GROQ_API_KEY")
   model_id: str = Field("deepseek-r1-distill-llama-70b", env="MODEL_ID")
   max_tokens: int = Field(2048, env="MAX_TOKENS")
   temperature: float = Field(0.3, env="TEMPERATURE")
   ransomware_live_base: str = Field("https://api.ransomware.live/v2", env="RANSOMWARE_LIVE_BASE")
class Config:
    env_file = ".env"
@lru_cache
def get_settings() -> Settings:
   return Settings()
