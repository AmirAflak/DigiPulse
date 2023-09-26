from pydantic import BaseSettings, Field   
from functools import lru_cache
import os

if os.getenv("CQLENG_ALLOW_SCHEMA_MANAGEMENT") is None:
    os.environ["CQLENG_ALLOW_SCHEMA_MANAGEMENT"] = "1"
    
    
class Settings(BaseSettings):
    name: str = Field(..., env="PROJ_NAME") 
    db_client_id: str = Field(..., env="ASTRA_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRA_CLIENT_SECRET")
    redis_url: str = Field(..., env="REDIS_URL")
    driver_path: str = Field(..., env="DRIVER_PATH")
    products_page_url: str = Field(..., env="PRODUCTS_PAGE_URL")
    class Config:
        env_file = ".env"
      
@lru_cache  
def get_settings():
    return Settings()