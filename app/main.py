from fastapi import FastAPI
from .config import get_settings

settings = get_settings()

app = FastAPI()

@app.get("/")

def read_index():
    return {"hello": "world", "name": settings.name}