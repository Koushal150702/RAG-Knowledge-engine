from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from .database import Base, engine
from .models import Document

app = FastAPI(title= 'RAG knowledge engine')


@app.get('/health')
def health():
    return {'status' : 'ok'}

Base.metadata.create_all(bind = engine)