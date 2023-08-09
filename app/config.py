from pydantic import BaseSetting, Field   
from functool import lru_cache

class Settings(BaseSetting):
    db_client_id: str = Field(..., env="ASTRA_CLIENT_ID")
    db_client_secret: str = Field(..., env="ASTRA_CLIENT_SECRET")
    
    class Config:
        env_file = ".env"
      
@lru_cache  
def get_settings():
    return Settings()