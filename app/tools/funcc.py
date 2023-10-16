from database.models import Item


def calculate_total_cart_price(user, db):
    cart_items = []
    item_quantities = {}
    total_price = 0

    for cart in user.cart:
        item_id = cart.item_id

        if item_id in item_quantities:
            item_quantities[item_id] += cart.quantity
        else:
            item_quantities[item_id] = cart.quantity

    for item_id, quantity in item_quantities.items():
        item = db.query(Item).filter(Item.id == item_id).first()
        if item:
            item_info = {
                "item_id": item_id,
                "quantity": quantity,
                "name": item.name,
                "price": item.price
            }
            cart_items.append(item_info)
            total_price += item.price * quantity

    return cart_items, total_price
