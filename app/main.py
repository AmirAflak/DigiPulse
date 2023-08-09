from fastapi import FastAPI
from typing import List
from cassandra.cqlengine.management import sync_table
from .schema import ProductSchema
from .config import get_settings
from .db import get_session
from .models import Product, ProductScrapeEvent

settings = get_settings()

app = FastAPI()

session = None

@app.on_event("startup")
def on_startup():
    global session
    session = get_session()
    sync_table(Product)
    sync_table(ProductScrapeEvent)

@app.get("/")
def read_index():
    return {"hello": "world", "name": settings.name}

@app.get("/products", response_model=List[ProductSchema])
def products_list_view():
    return list(Product.objects().all())

@app.get("/products/{dkp}")
def products_detail_view(dkp):
    res = dict(Product.objects().get(dkp=dkp))
    events_list = list(ProductScrapeEvent.objects().filter(dkp=dkp))
    res['events'] = [ProductScrapeEventDetailSchema(**x )for x in events_list]
    return res