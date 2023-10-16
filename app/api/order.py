import json

from fastapi import Depends, Header, Query
from sqlalchemy.orm import Session

from authentication.security import token_verification, extract_token, check_admin_authorization
from database.models import Order, Item
from fastapi import APIRouter
from database.database import get_db
from tools.funcc import calculate_total_cart_price
from database.schemas import ChangeStatus
from logger.logger import logger
router = APIRouter()


@router.get('/create', summary='CreateOrder', response_model=dict)
def create_order_for_cart(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    GET
    Создать ордер по корзине + в дальнейшем можно поставить POST и просить в теле адрес например
    """
    user = token_verification(extract_token(authorization), db)

    cart_items, total_price = calculate_total_cart_price(user, db)

    new_order = Order(user_id=user.id)
    new_order.cart_items = json.dumps(cart_items)
    new_order.total_price = total_price

    db.add(new_order)
    db.commit()

    response_message = {
        "message": "Заказ успешно создан",
        "Order ID": new_order.id,
        "cart": cart_items,
        "total_price": total_price
    }
    logger.info(
        f'GET /api/v1/store/user/cart/order/create Order created:Order ID:{new_order.id}, Items:{cart_items},Total price:{total_price}')
    return response_message



@router.post('/change-status', summary='ChangeStatusOrder', response_model=dict)
def change_status(change_status: ChangeStatus, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    POST
    Поменять статус заказа
    """
    check_admin_authorization(authorization, db)

    order_object = db.query(Order).filter(Order.id == change_status.order_id).first()

    if order_object:
        old_status = order_object.status

        order_object.status = change_status.new_status
        db.commit()
        db.refresh(order_object)

        response_message = {
            "message": "Статус заказа успешно изменен.",
            "Order ID": order_object.id,
            "Старый статус": old_status,
            "Новый статус": order_object.status,
            "User ID": order_object.user_id,
            "Created_at": order_object.created_at,
            "cart_items": order_object.cart_items,
            "Total price": order_object.total_price
        }

        logger.info(
            f'POST /api/v1/store/user/cart/order/change-status Order change status:Order ID:{order_object.id}, Old status:{old_status},New status:{order_object.status}')

        return response_message
    else:
        return {"message": "Заказ не найден."}

#http://127.0.0.1:8000/api/v1/store/user/cart/order/search?q={status}
@router.get("/search", summary='SearchOrder', response_model=dict)
def search_order(q: str = Query(..., description="Статус заказа для поиска"), authorization: str = Header(...),
                 db: Session = Depends(get_db)):
    """
    GET
    Ищем статус заказа через q аргумент
    """
    check_admin_authorization(authorization, db)

    orders = db.query(Order).filter(Order.status == q).all()

    if not orders:
        return {"message": "Заказы с указанным статусом не найдены."}

    order_list = []
    for order in orders:
        order_dict = {
            "Order ID": order.id,
            "Status": order.status,
            "User ID": order.user_id,
            "Created_at": order.created_at,
            "cart_items": order.cart_items,
            "Total price": order.total_price
        }
        order_list.append(order_dict)

    return {"message": "Заказы с указанным статусом найдены:", "orders": order_list}



@router.get('/my-order', summary='ViewOrder', response_model=dict)
def view_order(authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    GET
    Просмотр заказов пользователя
    """

    user = token_verification(extract_token(authorization), db)

    order_objects = db.query(Order).filter(Order.user_id == user.id).all()

    if order_objects:
        response_message = []
        for order_object in order_objects:
            items_info = []

            for cart_item in order_object.cart_items.split(','):

                item_id = None

                for item_info in cart_item.split(','):
                    if "item_id" in item_info:
                        item_id = item_info.split(":")[1].strip()

                if item_id:
                    item = db.query(Item).filter(Item.id == item_id).first()
                    if item:
                        item_info = {
                            "Item ID": item.id,
                            "Name": item.name,
                            "Price": item.price,
                            "Description": item.description
                        }
                        items_info.append(item_info)

            order_info = {
                "Order ID": order_object.id,
                "Status": order_object.status,
                "Created_at": order_object.created_at,
                "Items": items_info,
                "Total price": order_object.total_price
            }
            response_message.append(order_info)

        return {"message": "Ваши заказы", "orders": response_message}
    else:
        return {"message": "У вас нет заказов"}
