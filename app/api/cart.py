from sqlalchemy.orm import Session
from fastapi import Depends, Header, HTTPException
from authentication.security import hash_password, generate_token, token_verification, extract_token, \
    check_admin_authorization
from logger.logger import logger
from database.models import Cart
from database.schemas import CreateItem, CartitemDelete, CartItemUser
from fastapi import APIRouter
from database.database import get_db
from fastapi.responses import JSONResponse
router = APIRouter()



@router.post('/add', summary='CreateCart', response_model=dict, tags=['Cart'])
def create_cart_item(item_for_cart: CartItemUser, authorization: str = Header(...), db: Session = Depends(get_db)):
    """
    POST
    Добалвение в корзину
    """

    user = token_verification(extract_token(authorization), db)

    if user.cart is None:
        new_cart = Cart(item_id=item_for_cart.item_id, quantity=item_for_cart.quantity)
        user.cart = [new_cart]
    else:
        user.cart.append(Cart(item_id=item_for_cart.item_id, quantity=item_for_cart.quantity))

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
            # Если находим совпадение, удаляем элемент из корзины
            db.delete(cart_item)
            db.commit()
            return {'message': 'Товар успешно удален из корзины'}

    # Если совпадения не найдено
    return {'message': 'Товар не найден в корзине'}