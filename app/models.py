from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model

class Product(Model):
    __keyspace__ = "scraper_app"
    dkp = columns.Text(primary_key=True, required=True)
    title = columns.Text()
    price_str = columns.Text(default=("-1"))
    
class ProductScrapeEvent(Model):
    __keyspace__ = "scraper_app"
    uuid = columns.UUID(primary_key=True)
    dkp = columns.Text(index=True)
    title = columns.Text()
    price_str = columns.Text(default=("-100"))