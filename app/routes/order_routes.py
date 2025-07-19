from fastapi import APIRouter
from app.models.order_model import OrderModel
from app.controllers.order_controller import create_order_controller, list_orders_controller

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(order: OrderModel):
    return await create_order_controller(order)

@router.get("/orders/{user_id}")
async def list_orders(user_id: str, limit: int = 10, offset: int = 0):
    return await list_orders_controller(user_id, limit, offset)
