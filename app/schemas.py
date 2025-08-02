from typing import List, Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

# Customer


class CustomerBase(BaseModel):
    name: str
    email: EmailStr


class CustomerCreate(CustomerBase):
    pass


class CustomerRead(CustomerBase):
    id: int

    class Config:
        from_attributes = True


# Product


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock: int


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int

    class Config:
        from_attributes = True


# OrderItem


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int


class OrderItemCreate(OrderItemBase):
    pass


class OrderItemRead(OrderItemBase):
    id: int
    unit_price: float
    total_price: float

    class Config:
        from_attributes = True


# Order


class OrderBase(BaseModel):
    customer_id: int


class OrderCreate(OrderBase):
    items: List[OrderItemCreate]


class OrderRead(OrderBase):
    id: int
    created_at: datetime
    status: str
    total_amount: float
    items: List[OrderItemRead]

    class Config:
        from_attributes = True


# User


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    pass


class UserRead(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True


# ApiKey


class ApiKeyBase(BaseModel):
    key: str
    description: Optional[str]


class ApiKeyRead(ApiKeyBase):
    id: int
    active: bool

    class Config:
        from_attributes = True


# Authentication


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str
