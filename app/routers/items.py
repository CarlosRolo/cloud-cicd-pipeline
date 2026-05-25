from typing import List

from fastapi import APIRouter, HTTPException

from app.models.schemas import Item, ItemCreate

router = APIRouter(prefix="/items", tags=["items"])

_db: dict[int, Item] = {
    1: Item(id=1, name="Widget A", description="First item", price=9.99),
    2: Item(id=2, name="Widget B", price=19.99, available=False),
}
_next_id = 3


@router.get("/", response_model=List[Item])
async def list_items():
    return list(_db.values())


@router.get("/{item_id}", response_model=Item)
async def get_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item not found")
    return _db[item_id]


@router.post("/", response_model=Item, status_code=201)
async def create_item(payload: ItemCreate):
    global _next_id
    item = Item(id=_next_id, **payload.model_dump())
    _db[_next_id] = item
    _next_id += 1
    return item


@router.delete("/{item_id}", status_code=204)
async def delete_item(item_id: int):
    if item_id not in _db:
        raise HTTPException(status_code=404, detail="Item not found")
    del _db[item_id]
