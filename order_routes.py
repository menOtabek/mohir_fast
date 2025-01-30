from fastapi import APIRouter

order_router = APIRouter(prefix="/order")


@order_router.get("/")
async def order_route():
    return {"message": "This is the order route"}
