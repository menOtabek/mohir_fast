from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from product_routes import product_router
from database import engine, Base

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(auth_router)
app.include_router(order_router)
app.include_router(product_router)


@app.get("/")
async def root():
    return {"message": "This is the root route"}
