from pydantic import BaseModel, root_validator
from typing import Optional, Any
from .utils import uuid1_time_to_datetime
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
    created: Optional[Any] = None
    
    @root_validator(pre=True)
    def extra_create_time_from_uuid(cls, values):
        values['created'] = uuid1_time_to_datetime(values['uuid'].time)
        return values
    
    

    
