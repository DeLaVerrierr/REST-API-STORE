from fastapi import Depends, Header
from sqlalchemy.orm import Session
from authentication.security import check_admin_authorization
from logger.logger import logger
from database.models import Category
from database.schemas import CreateCategory
from fastapi import APIRouter
from database.database import get_db



router = APIRouter()


@router.post('/create', summary='CreateCategory', response_model=dict, tags=['Category'])
def create_item(category: CreateCategory, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    POST
    Создание новой категории
    """

    check_admin_authorization(authorization, db)

    category_object = Category(name=category.name)

    db.add(category_object)
    db.commit()

    response_data = {
        "message": "Category successfully created",
        'id': category_object.id,
        'name': category.name
    }

    logger.info(
        f'POST /api/v1/store/category/create Category created id:{category_object.id},name:{category.name}')
    return response_data

