import re
from authentication.security import generate_token, hash_password, extract_token, token_verification
from models import Base, User, Token
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, desc, asc, func
from sqlalchemy.orm import sessionmaker, Session
from fastapi import FastAPI, HTTPException, Query, Depends, Body, Header
import logging
import json

from schemas import RegisterUserRequest, UpdateUserProfileRequest

logger = logging.getLogger(__name__)

logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

file_handler = logging.FileHandler('app.log')

file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
# Подключение к базе
SQLALCHEMY_DATABASE_URI = "postgresql://postgres:Lilpeep228@localhost:5432/store"
engine = create_engine(SQLALCHEMY_DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/api/v1/store/user', summary='CreateUser', response_model=dict, tags=['User'])
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

    # Создаем объект пользователя и токена
    user_object = User(name=user.name, surname=user.surname, phone_number=user.phone_number, password=hashed_password)
    token_object = Token(token=token, user=user_object)

    # Добавляем объекты в сессию
    db.add_all([user_object, token_object])

    # Один раз вызываем commit для сохранения изменений
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

@app.get('/api/v1/store/user/profile', summary='ProfileUser', response_model=dict, tags=['User'])
def get_user_profile(authorization: str = Header(...), db: Session = Depends(get_db)):
    user = token_verification(extract_token(authorization), db)
    response_message = {
        "id": user.id,
        "name": user.name,
        "surname": user.surname,
        "phone_number": user.phone_number
    }
    return response_message


@app.put('/api/v1/store/user/update-profile', summary='UpdateProfileUser', response_model=dict, tags=['User'])
def update_user_profile(update_data: UpdateUserProfileRequest, authorization: str = Header(...),
                        db: Session = Depends(get_db)):
    user = token_verification(extract_token(authorization), db)

    # Обновляем данные пользователя
    user.name = update_data.name
    user.surname = update_data.surname
    user.phone_number = update_data.phone_number

    # Сохраняем изменения в базе данных
    db.commit()

    return {'message': 'Profile updated successfully'}
