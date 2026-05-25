from pydantic import BaseModel, Field
from typing import Optional


class Item(BaseModel):
    id: int
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    available: bool = True


class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    available: bool = True


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
