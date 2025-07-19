from bson import ObjectId
from app.db.database import db
from app.models.order_model import OrderModel

async def create_order_controller(order: OrderModel):
    total = 0
    product_ids = [ObjectId(item.productId) for item in order.items]
    products = await db.products.find({"_id": {"$in": product_ids}}).to_list(None)
    product_price_map = {str(p["_id"]): p["price"] for p in products}

    for item in order.items:
        total += product_price_map.get(item.productId, 0) * item.qty

    order_data = order.dict()
    order_data["total"] = total

    result = await db.orders.insert_one(order_data)
    return {"id": str(result.inserted_id)}


async def list_orders_controller(user_id: str, limit: int = 10, offset: int = 0):
    pipeline = [
        {"$match": {"userId": user_id}},
        {"$sort": {"_id": 1}},
        {"$skip": offset},
        {"$limit": limit},
        {
            "$addFields": {
                "items": {
                    "$map": {
                        "input": "$items",
                        "as": "item",
                        "in": {
                            "qty": "$$item.qty",
                            "productId": {"$toObjectId": "$$item.productId"}
                        }
                    }
                }
            }
        },
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "productDetails"
            }
        }
    ]

    orders = await db.orders.aggregate(pipeline).to_list(None)

    for order in orders:
        for i, item in enumerate(order["items"]):
            matching = next(
                (p for p in order["productDetails"] if p["_id"] == item["productId"]),
                None
            )
            item["productDetails"] = {
                "id": str(item["productId"]),
                "name": matching["name"] if matching else "Unknown"
            }
            item.pop("productId", None)

        order["id"] = str(order["_id"])
        order.pop("_id", None)
        order.pop("productDetails", None)

    return {
        "data": orders,
        "page": {
            "next": offset + limit,
            "limit": len(orders),
            "previous": max(0, offset - limit)
        }
    }
