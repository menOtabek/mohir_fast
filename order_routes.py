from fastapi import APIRouter, Depends, status
from models import Order, User, Product
from database import session, engine
from fastapi.security import OAuth2PasswordBearer
from auth_token import token_decode

order_router = APIRouter(prefix="/order")

oauth2 = OAuth2PasswordBearer(tokenUrl="/token")
session = session(bind=engine)


@order_router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(token: str = Depends(oauth2)):
    payload = await token_decode(token)
    user_id = payload.get('sub')
    orders = session.query(Order).filter(Order.user_id == user_id).all()
    return {
        'success': True,
        'message': "User's orders",
        'data': orders
    }


