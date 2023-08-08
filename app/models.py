from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model


class Product(Model):
    __keyspace__ = "scraper_app"
    dkp = columns.Text(primary_key=True, required=True)
    title = columns.Text()