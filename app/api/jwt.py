from fastapi import Depends, Header, HTTPException
from authentication.security import hash_password, generate_token, token_verification, extract_token

from database.schemas import CreateItem, SearchItem, UpdateItem, DeleteItem, UserJWT
from fastapi import APIRouter
import jwt

router = APIRouter()

SECRET_KEY = "testsecretkey"


def create_jwt_token(user_data: dict, secret_key: str):
    token = jwt.encode(user_data, secret_key, algorithm="HS256")
    return token


@router.post('/create', summary='CreateUserJWT', response_model=dict)
def create_user_jwt(user: UserJWT):
    user_data = user.dict()
    token = create_jwt_token(user_data, SECRET_KEY)
    print(user_data)
    return {"token": token}


# payload = {"some": "payload", "iss": "urn:foo"}
#
# token = jwt.encode(payload, "secret")
# decoded = jwt.decode(token, "secret", issuer="urn:foo", algorithms=["HS256"])


@router.get('/profile', summary="ProfileWithJWT", response_model=dict)
def profile_user_jwt(authorization: str = Header(...)):
    decoded_token = jwt.decode(extract_token(authorization), SECRET_KEY, algorithms=["HS256"])
    return decoded_token
