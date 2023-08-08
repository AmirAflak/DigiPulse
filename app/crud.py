from cassandra.cqlengine.management import sync_table
from .db import get_session
from .models import Product, ProductScrapeEvent
import uuid 

session = get_session()
sync_table(Product)
sync_table(ProductScrapeEvent)


def create_entry(data: dict):
    return Product.create(**data)

def create_scrape_entry(data: dict):
    data['uuid'] = uuid.uuid1()
    return ProductScrapeEvent.create(**data)