from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.testing import db
from sqlalchemy.orm import relationship
from sqlalchemy import BigInteger
from sqlalchemy.sql import func

Base = declarative_base()


class User(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    phone_number = Column(String, index=True)
    password = Column(String, index=True)
    status = Column(String, default='client')

    tokens = relationship("Token", back_populates="user")
    cart = relationship("Cart", back_populates="user")

class Token(Base):
    __tablename__ = 'Tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.id'))

    user = relationship("User", back_populates="tokens")


class Item(Base):
    __tablename__ = 'Items'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Integer, index=True)
    description = Column(String, unique=True, index=True)
    quantity = Column(Integer,index=True)
    category_id = Column(Integer, ForeignKey('Categories.id'))

    category = relationship("Category", back_populates="items")

class Category(Base):
    __tablename__ = 'Categories'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    items = relationship("Item", back_populates="category")


class Cart(Base):
    __tablename__ = "Carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    item_id = Column(Integer, index=True)
    quantity = Column(Integer, index=True, default=1)

    user = relationship("User", back_populates="cart")
