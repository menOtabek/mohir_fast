from auth_token import access_token_generate, refresh_token_generate, token_decode
from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordBearer
from schemas import Login, Register
from database import session, engine
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

session = session(bind=engine)
auth_router = APIRouter(prefix="/auth")

oauth2 = OAuth2PasswordBearer(tokenUrl="/token")


@auth_router.get("/me")
async def auth(token: str = Depends(oauth2)):
    payload = await token_decode(token)
    user_id = payload.get("sub")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    data = {
        "id": user.id,
        "username": user.username,
        "email": user.email
    }
    return {"success": True,
            'message': 'Data about User',
            "data": data}


@auth_router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user: Register):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with this Email already registered')

    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='User with this Username already registered')

    new_user = User(email=user.email,
                    username=user.username,
                    password=generate_password_hash(user.password),
                    is_active=user.is_active,
                    is_staff=user.is_staff)
    session.add(new_user)
    session.commit()
    data = {'user_id': new_user.id,
            'email': new_user.email,
            'username': new_user.username,
            'is_active': new_user.is_active,
            'is_staff': new_user.is_staff}
    return {
        'success': True,
        'message': 'User created successfully',
        'data': data,
    }


@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login(user: Login):
    db_user = session.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    if not check_password_hash(db_user.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Incorrect password')
    access_token = await access_token_generate(db_user.id)
    refresh_token = await refresh_token_generate(db_user.id)
    data = {
        'success': True,
        'message': 'User successfully logged in',
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return data


@auth_router.get("/refresh", status_code=status.HTTP_200_OK)
async def refresh(token: str = Depends(oauth2)):
    payload = await token_decode(token)
    user_id = payload.get("sub")
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    access_token = await access_token_generate(user_id)
    refresh_token = await refresh_token_generate(user_id)
    data = {
        'success': True,
        'message': 'User successfully refreshed',
        'access_token': access_token,
        'refresh_token': refresh_token
    }
    return data
