from fastapi import Depends, Header
from sqlalchemy.orm import Session
from authentication.security import token_verification, extract_token
from database.schemas import CartItemUser, CartitemDelete
from logger.logger import logger
from database.models import User, Token, Cart, Item
from fastapi import APIRouter
from database.database import get_db

router = APIRouter()

#Работает
#
# {
#     "name":"TEST2",
#     "surname":"TEST",
#     "phone_number":"+79178974996",
#     "password":"li2222"
# }

# {
#     "message": "User successfully created",
#     "id": 5,
#     "name": "Олег",
#     "surname": "Дубков",
#     "phone_number": "+79178878767",
#     "token": "oc6fH5iMlk2affuja-fOU_sEHqSKXW8mAupY6jSgd64"
# }

@router.post('/add', summary='CreateCart', response_model=dict, tags=['Cart'])
def create_cart_item(item_for_cart: CartItemUser, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    POST
    Добавление товара в корзину
    """

    user = token_verification(extract_token(authorization), db)

    if user.cart is None:
        new_cart = Cart(user=user, item_id=item_for_cart.item_id, quantity=item_for_cart.quantity)
        db.add(new_cart)
    else:
        user.cart.append(Cart(user=user, item_id=item_for_cart.item_id, quantity=item_for_cart.quantity))

    db.commit()

    response_message = {"message": "Item successfully added to the cart"}
    return response_message



@router.delete('/delete', summary="DeleteItemCart", response_model=dict, tags=['Cart'])
def delete_cart_item(item: CartitemDelete, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    Delete
    Удаление товара из корзины
    """
    user = token_verification(extract_token(authorization), db)

    if user.cart is None:
        return {'message': 'У вас нет товаров в корзине'}

    # Итерируемся по элементам корзины пользователя
    for cart_item in user.cart:
        if cart_item.item_id == item.item_id and cart_item.quantity == item.quantity:
            db.delete(cart_item)
            db.commit()
            return {'message': 'Товар успешно удален из корзины'}

    return {'message': 'Товар не найден в корзине'}