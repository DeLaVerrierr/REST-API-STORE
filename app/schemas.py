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