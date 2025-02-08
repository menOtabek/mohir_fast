from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from models import Order, User, Product
from database import session, engine
from fastapi.security import OAuth2PasswordBearer
from auth_token import token_decode
from schemas import OrderSchema, OrderUpdateSchema

order_router = APIRouter(prefix="/order")
oauth2 = OAuth2PasswordBearer(tokenUrl="/token")
session = session(bind=engine)


@order_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_order(order: OrderSchema, token: str = Depends(oauth2)):
    user_data = await token_decode(token)
    user_id = user_data.get('sub')
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized")
    product = session.query(Product).filter(Product.id == order.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    new_order = Order(
        quantity=order.quantity
    )
    new_order.user_id = user.id
    new_order.product_id = order.product_id
    session.add(new_order)
    session.commit()
    return {
        'success': True,
        'message': "Order created",
        'data': {
            'id': new_order.id,
            'quantity': new_order.quantity,
            'user_id': new_order.user.id,
            'product': {
                'id': new_order.product.id,
                'name': new_order.product.name,
                'price': new_order.product.price,
            }
        }
    }


@order_router.get("/list", status_code=status.HTTP_200_OK)
async def list_orders(token: str = Depends(oauth2)):
    user_data = await token_decode(token)
    user_id = user_data.get('sub')
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    orders = session.query(Order).filter(Order.user_id == user.id).all()

    return {
        'success': True,
        'message': "List orders",
        'data': orders
    }


@order_router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int, token: str = Depends(oauth2)):
    user_data = await token_decode(token)
    user_id = user_data.get('sub')
    user = session.query(User).filter(User.id == user_id).first()
    order = session.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return {
        'success': True,
        'message': "Order detail",
        'data': {
            'id': order.id,
            'quantity': order.quantity,
            'user_id': order.user.id,
            'status': order.status,
            'product': {
                'id': order.product.id,
                'name': order.product.name,
                'price': order.product.price,
            }
        }
    }


@order_router.patch("/{order_id}/update", status_code=status.HTTP_200_OK)
async def update_order(order_id: int, order_update: OrderUpdateSchema, token: str = Depends(oauth2)):
    order_data = await token_decode(token)
    user_id = order_data.get('sub')
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    exist_order = session.query(Order).filter(Order.id == order_id, Order.user_id == user.id).first()
    if not exist_order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    new_order = order_update.model_dump(exclude_unset=True)
    for key, value in new_order.items():
        setattr(exist_order, key, value)
    session.commit()
    session.refresh(exist_order)

    return {
        'success': True,
        'message': "Order updated",
        'data': {
            'id': exist_order.id,
            'quantity': exist_order.quantity,
            'user_id': exist_order.user.id,
            'status': exist_order.status,
            'product': {
                'id': exist_order.product.id,
                'name': exist_order.product.name,
                'price': exist_order.product.price,
            }
        }
    }
