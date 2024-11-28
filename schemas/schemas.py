# app/schemas/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from models.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER

class User(UserBase):
    id: int
    is_active: bool
    role: UserRole

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class InventoryBase(BaseModel):
    name: str
    description: str
    quantity: int

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    created_by: int

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    username: str
    password: str