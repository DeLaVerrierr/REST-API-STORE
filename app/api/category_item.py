from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from authentication.security import hash_password, generate_token, token_verification, extract_token, \
    check_admin_authorization
from logger.logger import logger
from database.models import Category, Item
from database.schemas import CreateCategory
from fastapi import APIRouter
from database.database import get_db
from fastapi.responses import JSONResponse
from fastapi import APIRouter, Depends, Path

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


@router.get('/all', summary='AllCategory', response_model=dict, tags=['Category'])
def all_categories(db: Session = Depends(get_db)):
    all_categories = db.query(Category).all()

    category_list = [{"category_id": category.id, "category_name": category.name} for category in all_categories]

    response_data = {
        "count_categories": len(all_categories),
        "categories": category_list
    }

    return response_data


@router.get('/{category_id}', summary='CategoryDetails', response_model=dict, tags=['Category'])
def category_details(category_id: int = Path(..., description='ID of the category'), db: Session = Depends(get_db)):
    """
    GET
    Вывод товаров в категории по id
    """
    category = db.query(Category).filter(Category.id == category_id).first()

    if category is None:
        return {"message": "Category not found"}

    items = db.query(Item).filter(Item.category_id == category_id).all()

    item_list = [{"item_id": item.id, "item_name": item.name, "item_description": item.description} for item in items]

    response_data = {
        "category_id": category_id,
        "category_name": category.name,
        "count_items": len(item_list),
        "category_items": item_list
    }

    return response_data

#
# {
#     "name": "мышка",
#     "price": 1500,
#     "description": "Мышка игравая вот или нет кто знает",
#     "category_id":1
# }


# {
#     "category_id": 2,
#     "category_name": "Электронника"
# },
# {
#     "category_id": 3,
#     "category_name": "Бытовые товары"
# },
# {
#     "category_id": 4,
#     "category_name": "Холодильники"
# }