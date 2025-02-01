from datetime import datetime, timedelta
import jwt
from jwt.exceptions import InvalidTokenError

EXPIRE_ACCESS = 30 * 10
EXPIRE_REFRESH = 60 * 10
SECRET_KEY = "b9bb0e47de50fe904431c0237e8442efc61f484407a1922c4611226b79e822e1"


async def access_token_generate(user_id: int) -> str:
    """ data = {'user_id': 1}"""
    data = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=EXPIRE_ACCESS),
        'iat': datetime.utcnow(),
        'type': 'access'
    }
    payload = jwt.encode(payload=data, key=SECRET_KEY, algorithm="HS256")
    return payload


async def refresh_token_generate(user_id: int) -> str:
    """ data = {'user_id': 1}"""
    data = {
        'sub': str(user_id),
        'exp': datetime.utcnow() + timedelta(minutes=EXPIRE_REFRESH),
        'iat': datetime.utcnow(),
        'type': 'refresh'
    }
    payload = jwt.encode(payload=data, key=SECRET_KEY, algorithm="HS256")
    return payload


async def token_decode(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except InvalidTokenError as e:
        raise e
