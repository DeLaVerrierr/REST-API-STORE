from fastapi import FastAPI
from api import user, item, category_item, cart, order, jwt

app = FastAPI()

app.include_router(user.router, prefix="/api/v1/store/user", tags=["User"])
app.include_router(item.router, prefix="/api/v1/store/item", tags=["Item"])
app.include_router(category_item.router, prefix="/api/v1/store/category", tags=["Category"])
app.include_router(cart.router, prefix="/api/v1/store/user/cart", tags=["Cart"])
app.include_router(order.router, prefix="/api/v1/store/user/cart/order", tags=["Order"])
app.include_router(jwt.router, prefix="/api/v1/store/user/jwt", tags=["JWT"])
