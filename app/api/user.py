import re

from fastapi import Depends, Header
from sqlalchemy.orm import Session

from authentication.security import hash_password, generate_token, token_verification, extract_token
from logger.logger import logger
from database.models import User, Token
from database.schemas import RegisterUserRequest, UpdateUserProfileRequest
from fastapi import APIRouter
from database.database import get_db

router = APIRouter()

#Работает

# {
#     "name":"TEST2",
#     "surname":"TEST",
#     "phone_number":"+79178974996",
#     "password":"li2222"
# }


@router.post('/create', summary='CreateUser', response_model=dict, tags=['User'])
def create_user(user: RegisterUserRequest, db: Session = Depends(get_db)):
    """
    POST
    Регистрация пользователя
    """
    pattern_phone_number = r'\+7\d{10}'
    # Проверка на корректность телефона
    if not re.match(pattern_phone_number, user.phone_number):
        return "error phone_number: ru format +71234567890"

    # Хэшируем пароль
    hashed_password = hash_password(user.password)

    # Генерируем токен
    token = generate_token()

    user_object = User(name=user.name, surname=user.surname, phone_number=user.phone_number, password=hashed_password)
    token_object = Token(token=token, user=user_object)

    db.add_all([user_object, token_object])

    db.commit()

    user_id = user_object.id

    response_data = {
        "message": "User successfully created",
        "id": user_id,
        "name": user.name,
        "surname": user.surname,
        "phone_number": user.phone_number,
        "token": token
    }

    logger.info(
        f'POST /api/v1/store/user Users created id:{user_id},name:{user.name},surname:{user.surname},phone_number:{user.phone_number}')
    return response_data


# Токен UsKO7S4tYmQK6NZ3vuE_QFFHJIZk_xgbIZ0FtzRKYr0

@router.get('/profile', summary='ProfileUser', response_model=dict, tags=['User'])
def get_user_profile(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    GET
    Профиль пользователя
    """
    user = token_verification(extract_token(authorization), db)
    response_message = {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "phone_number": user.phone_number
    }
    return response_message


@router.put('/update-profile', summary='UpdateProfileUser', response_model=dict, tags=['User'])
def update_user_profile(update_data: UpdateUserProfileRequest, authorization: str = Header(...),
                        db: Session = Depends(get_db)):
    """
    PUT
    изменение name/surname/phone_number пользователя
    """
    user = token_verification(extract_token(authorization), db)

    if update_data.name:
        user.name = update_data.name
    if update_data.surname:
        user.surname = update_data.surname
    if update_data.phone_number:
        user.phone_number = update_data.phone_number

    db.commit()

    return {'message': 'Profile updated successfully'}
