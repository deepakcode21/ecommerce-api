from pydantic import BaseModel, Field
from typing import List

class SizeModel(BaseModel):
    size: str
    quantity: int = 0

class ProductModel(BaseModel):
    name: str
    price: float
    sizes: List[SizeModel]
