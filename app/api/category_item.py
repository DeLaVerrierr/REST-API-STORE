from fastapi import Depends, Header
from sqlalchemy import func
from sqlalchemy.orm import Session
from authentication.security import check_admin_authorization
from logger.logger import logger
from database.models import Category
from database.schemas import CreateCategory, ChangeNameCategory, DeleteCategory
from fastapi import APIRouter
from database.database import get_db

router = APIRouter()


@router.post('/create', summary='CreateCategory', response_model=dict)
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


@router.put('/change-name', summary='ChangeNameCategory', response_model=dict)
def change_name_category(new_name_category: ChangeNameCategory, authorization: str = Header(...),
                         db: Session = Depends(get_db)):
    """
    PUT
    Изменение имени категории
    """
    check_admin_authorization(authorization, db)
    category_object = db.query(Category).filter(Category.id == new_name_category.category_id).first()
    if category_object:
        category_object.name = new_name_category.new_name
        db.commit()
        return {"message": "Имя категории успешно изменено"}
    else:
        return {"message": "Категория не найдена"}


@router.delete("/delete", summary="DeleteCategory", response_model=dict)
def delete_category(category_del: DeleteCategory, authorization: str = Header(...),
                    db: Session = Depends(get_db)):
    """
    DELETE
    Удаление категории по ID и name (регистрозависимый для точности удаления)
    """
    check_admin_authorization(authorization, db)

    category_for_delete = db.query(Category).filter(
        Category.id == category_del.category_id, Category.name == category_del.name
    ).first()

    if category_for_delete:
        db.delete(category_for_delete)
        db.commit()

        logger.info(
            f'DELETE /api/v1/store/category/delete Category delete: Category ID:{category_del.category_id}, Name:{category_del.name}'
        )

        return {'message': 'Категория удалена успешно'}
    else:
        return {'message': 'Категория не найдена'}
