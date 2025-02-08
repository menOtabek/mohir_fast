from pydantic import BaseModel, Field
from typing import Optional, List

class Register(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, examples=["JohnDoe"])
    password: str = Field(..., min_length=6, examples=["strong_password"])
    email: str = Field(..., examples=["johndoe@example.com"])
    is_active: Optional[bool] = Field(default=True, examples=[True])
    is_staff: Optional[bool] = Field(default=False, examples=[False])



class Login(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, examples=['johndoe'])
    password: str = Field(..., min_length=6, examples=['strong_password'])



class OrderSchema(BaseModel):
    quantity: int
    # product_id: Optional[int]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "quantity": 1,
                # "product_id": 1
            }
        }


class OrderStatusSchema(BaseModel):
    status: Optional[str]
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "status": "pending",
            }
        }


class ProductSchema(BaseModel):
    name: str
    price: float
    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Product name",
                "price": 1.0,
            }
        }
