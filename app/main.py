from fastapi import FastAPI
from app.routes.product_routes import router as product_router
from app.routes.order_routes import router as order_router

app = FastAPI(title="E-commerce API")

@app.get("/")
async def root():
    return {"message": "Hello Buddy! Backend Working Fine!"}

app.include_router(product_router)
app.include_router(order_router)
