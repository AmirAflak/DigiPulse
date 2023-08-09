from fastapi import FastAPI
from cassandra.cqlengine.management import sync_table
from .config import get_settings
from .db import get_session
from .models import Product, ProductScrapeEvent

settings = get_settings()

app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    global session
    session = db.get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)

@app.get("/")
def read_index():
    return {"hello": "world", "name": settings.name}


