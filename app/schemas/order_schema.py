def order_helper(order) -> dict:
    return {
        "id": str(order["_id"]),
        "userId": order["userId"],
        "items": order["items"],
        "total": order["total"]
    }
