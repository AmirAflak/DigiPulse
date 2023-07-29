from .db import get_session
from .models import Product

session = get_session()

def create_entry(data: dict):
    return Product.create(**data)

