from typing import Optional
from app.models.product_model import ProductModel
from app.db.database import db
from app.schemas.product_schema import product_helper

async def create_product_controller(product: ProductModel):
    result = await db.products.insert_one(product.dict())
    return {"id": str(result.inserted_id)}

async def list_products_controller(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = 10,
    offset: int = 0
):
    query = {}

    if name:
        query["name"] = {"$regex": name, "$options": "i"}

    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}

    cursor = db.products.find(query).skip(offset).limit(limit).sort("_id")
    products = [product_helper(p) async for p in cursor]

    return {
        "data": products,
        "page": {
            "next": offset + limit,
            "limit": len(products),
            "previous": max(0, offset - limit)
        }
    }
