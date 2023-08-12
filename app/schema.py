from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class ProductSchema(BaseModel):
    dkp: str
    title: Optional[str]
    
    
class ProductScrapeEventSchema(BaseModel):
    uuid: UUID
    dkp: str
    title: Optional[str]
    price_str: Optional[str]
    
class ProductScrapeEventDetailSchema(BaseModel):
    dkp: str
    title: Optional[str]
    price_str: Optional[str]
    

    
