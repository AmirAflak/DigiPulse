from pydantic import BaseModel
from uuid import UUID

class ProductSchema(BaseModel):
    dkp: str
    title: str
    
    
class ProductScrapeEventSchema(BaseModel):
    uuid: UUID
    dkp: str
    title: str
    
