from fastapi.exceptions import HTTPException
from fastapi import APIRouter, status
from schemas import SignUp
from database import session
from models import User

auth_router = APIRouter(prefix="/auth")


@auth_router.get("/")
async def sign_in():
    return {"message": "Welcome to Auth API!"}


@auth_router.post("/sign-up")
async def sign_up(user: SignUp):
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
                    password=user.password,
                    is_active=user.is_active,
                    is_staff=user.is_staff)
    session.add(new_user)
    session.commit()
