from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
app = FastAPI()

class Item(BaseModel):
    text: str 
    is_done: bool = False

items: list[Item] = []

@app.get('/')
def root():
    return {'Hello' : 'World'}


@app.post('/items')
def create_item(item: Item):
    items.append(item)
    return items

@app.get('/items/{id}', response_model=Item)
def get_item(id: int):
    if id < len(items):
        return items[id]
    raise HTTPException(status_code=404, detail=f'Item {id} not found') 