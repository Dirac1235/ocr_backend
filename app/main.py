from typing import Union
from fastapi import FastAPI
from app.api.routes import router as ocr_router

app = FastAPI(title="ID OCR Service", version="1.0.0")
app.include_router(ocr_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return { "message": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}