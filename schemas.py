from pydantic import BaseModel
from datetime import datetime, date


class Items_in_store(BaseModel):
    id: int
    name: str


class Stores_list(BaseModel):
    id: int
    address: str


class SalesIn(BaseModel):
    stores_id: int
    items_id: int


class SalesOut(BaseModel):
    stores_id: int
    items_id: int
    create_date = date


class Top_stores(Stores_list):
    id: int
    address: str
    tottal_rev: float


class Top_items(BaseModel):
    id: int
    name: str
    count: int