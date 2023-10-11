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

class Token(Base):
    __tablename__ = 'Tokens'

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey('Users.id'))

    user = relationship("User", back_populates="tokens")
