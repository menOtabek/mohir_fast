from fastapi.exceptions import HTTPException
from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer
from auth_token import token_decode
from models import User, Product
from schemas import ProductSchema
from auth_routes import session

product_router = APIRouter(prefix="/product")
oauth2 = OAuth2PasswordBearer(tokenUrl='/token')


@product_router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_product(product: ProductSchema, token: str = Depends(oauth2)):
    user_data = await token_decode(token)
    user_id = user_data.get('sub')
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    new_product = Product(
        name=product.name,
        price=product.price
    )
    session.add(new_product)
    session.commit()

    return {
        'status': True,
        'message': 'Product created',
        'data': {
            'id': new_product.id,
            'name': new_product.name,
            'price': new_product.price
        }
    }


@product_router.get("/list", status_code=status.HTTP_200_OK)
async def list_products():
    products = session.query(Product).all()
    return {
        'success': True,
        'message': 'Products list',
        'data': products
    }


@product_router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def product_details(product_id: int):
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return {
        'status': True,
        'message': 'Product details',
        'data': {
            'id': product.id,
            'name': product.name,
            'price': product.price
        }
    }


@product_router.delete("/{product_id}/delete", status_code=status.HTTP_200_OK)
async def delete_product(product_id: int, token: str = Depends(oauth2)):
    user_data = await token_decode(token)
    user_id = user_data.get('sub')
    user = session.query(User).filter_by(id=user_id).first()
    if not user or user.is_staff is False:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found or method not permitted")
    product = session.query(Product).filter_by(id=product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    session.delete(product)
    session.commit()
    return {
        'status': True,
        'message': 'Product deleted',
    }
