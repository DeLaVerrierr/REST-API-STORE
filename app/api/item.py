import re

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import update
from authentication.security import hash_password, generate_token, token_verification, extract_token, \
    check_admin_authorization
from logger.logger import logger
from database.models import Item, User, Category
from database.schemas import CreateItem, SearchItem, UpdateItem
from fastapi import APIRouter
from database.database import get_db
from fastapi.responses import JSONResponse


router = APIRouter()


@router.post('/create', summary='CreateItem', response_model=dict, tags=['Item'])
def create_item(item: CreateItem, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    POST
    Создание нового товара
    """

    check_admin_authorization(authorization, db)

    if len(item.description) <= 10:
        return JSONResponse(content={"error": "Description length must be more than 10 characters"})

    item_object = Item(name=item.name, price=item.price, description=item.description, category_id=item.category_id)

    db.add(item_object)
    db.commit()
    category_name = db.query(Category).filter(Category.id == item.category_id).first().name
    response_data = {
        "message": "Item successfully created",
        'id': item_object.id,
        'name': item.name,
        'price': item.price,
        'description': item.description,
        "quantity": item.quantity,
        'category_id': item.category_id,
        'category_name': category_name
    }

    logger.info(
        f'POST /api/v1/store/item/create Item created id:{item_object.id},name:{item.name},price:{item.price},description:{item.description}, category_id:{item.category_id},category_name:{category_name}')
    return response_data

@router.put('/update', summary='UpdateItem', response_model=dict, tags=['Item'])
def update_user_profile(update_data: UpdateItem, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    PUT
    изменение Item
    """
    check_admin_authorization(authorization, db)

    # Получаем обновленный объект
    updated_item = db.query(Item).filter(Item.id == update_data.id).first()

    if updated_item:
        if update_data.description and len(update_data.description) <= 10:
            return JSONResponse(content={"error": "Description length must be more than 10 characters"})

        update_dict = {field: value for field, value in update_data.dict().items() if value is not None}

        # Обновляем атрибуты объекта
        for field, value in update_dict.items():
            setattr(updated_item, field, value)

        db.commit()
        db.refresh(updated_item)  # Обновляем состояние объекта

        return {
            "id": updated_item.id,
            "name": updated_item.name,
            "price": updated_item.price,
            "description": updated_item.description
        }
    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router.post('/search', summary='SearchItem', response_model=dict, tags=['Item'])
def search_item(item: SearchItem, db: Session = Depends(get_db)):
    """
    POST
    Показывает товары в зависимости от фильтра
    """
    query = db.query(Item)

    if item.id is not None:
        query = query.filter(Item.id == item.id)

    if item.name is not None:
        query = query.filter(Item.name.ilike(f"%{item.name}%"))

    if item.price is not None:
        query = query.filter(Item.price == item.price)

    if item.description is not None:
        query = query.filter(Item.description.ilike(f"%{item.description}%"))

    results = query.all()

    if results:
        results = [
            {
                "id": item.id,
                "name": item.name,
                "price": item.price,
                "description": item.description
            }
            for item in results
        ]
        filter_used = {attr: getattr(item, attr) for attr in ["id", "name", "price", "description"] if
                       getattr(item, attr) is not None}
        return JSONResponse(content={"filter": filter_used, "results": results})

    return JSONResponse(content={"message": "Item not found"})
