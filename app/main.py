from fastapi import FastAPI
from api import user, item, category_item, cart, order

app = FastAPI()

app.include_router(user.router, prefix="/api/v1/store/user", tags=["user"])
app.include_router(item.router, prefix="/api/v1/store/item", tags=["item"])
app.include_router(category_item.router, prefix="/api/v1/store/category", tags=["category"])
app.include_router(cart.router, prefix="/api/v1/store/user/cart", tags=["cart"])
app.include_router(order.router, prefix="/api/v1/store/user/cart/order", tags=["order"])
