from sqlalchemy.orm import Session
from fastapi import Depends, Header
from authentication.security import token_verification, extract_token
from database.models import Cart
from database.schemas import CartitemDelete, CartItemUser
from fastapi import APIRouter
from database.database import get_db
router = APIRouter()



@router.post('/add', summary='CreateCart', response_model=dict)
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





@router.delete('/delete', summary="DeleteItemCart", response_model=dict)
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