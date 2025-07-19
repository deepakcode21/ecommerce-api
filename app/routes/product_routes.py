from fastapi import APIRouter
from typing import Optional
from app.models.product_model import ProductModel
from app.controllers.product_controller import (
    create_product_controller,
    list_products_controller,
)

router = APIRouter()

@router.post("/products", status_code=201)
async def create_product(product: ProductModel):
    return await create_product_controller(product)

@router.get("/products")
async def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    return await list_products_controller(name, size, limit, offset)
