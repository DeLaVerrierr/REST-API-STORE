from typing import List

from pydantic import BaseModel




class RegisterUserRequest(BaseModel):
    name: str
    surname: str
    phone_number: str
    password: str


class UserModel(BaseModel):
    id: int
    surname: str
    phone_number: str
    password: str

    class Config:
        from_attributes = True


class UpdateUserProfileRequest(BaseModel):
    name: str = None
    surname: str = None
    phone_number: str = None


class CreateItem(BaseModel):
    name: str
    price: int
    description: str
    quantity: int
    category_id: int


class SearchItem(BaseModel):
    id: int = None
    name: str = None
    price: int = None
    description: str = None
    category_id: int = None


class UpdateItem(BaseModel):
    id: int
    name: str = None
    price: int = None
    description: str = None
    quantity: int = None
    category_id: int = None


class CreateCategory(BaseModel):
    name: str


class CartItemUser(BaseModel):
    item_id: int
    quantity: int = 1

class CartitemDelete(BaseModel):
    item_id: int
    quantity: int = 1