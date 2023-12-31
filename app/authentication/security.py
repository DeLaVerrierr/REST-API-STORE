import secrets

import bcrypt
from sqlalchemy.orm import Session
from fastapi import HTTPException
from database.models import Token, User


def generate_token():
    """
    Генерация токена
    """
    token = secrets.token_urlsafe(32)
    return token


def hash_password(password: str) -> bytes:
    """
    Хэширование пароля
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def token_verification(token: str, db: Session) -> User | dict[str, str]:
    """
    Проверка токена в базе
    """
    match_token_user = db.query(Token).filter(Token.token == token).first()
    if not match_token_user:
        return {'error': 'Invalid token'}
    user = match_token_user.user
    return user

def extract_token(authorization: str) -> str:
    """
    Убираем Bearer если есть
    """
    if authorization.startswith('Bearer '):
        return authorization[7:]
    return authorization

def check_admin_authorization(authorization: str, db: Session) -> None:
    user = token_verification(extract_token(authorization), db)
    if isinstance(user, User):
        if user.status != 'admin':
            raise HTTPException(status_code=403, detail="Access denied. User is not an admin")
    else:
        raise HTTPException(status_code=403, detail=user['error'])