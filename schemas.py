from pydantic import BaseModel, Field
from typing import Optional

class SignUp(BaseModel):
    id: Optional[int] = None
    username: str = Field(..., min_length=3, max_length=25, example="John")
    password: str = Field(..., min_length=6, max_length=25, example="password123")
    email: str = Field(..., min_length=3, max_length=254, example="John@gmail.com")
    is_active: Optional[bool] = Field(default=True, example=True)
    is_staff: Optional[bool] = Field(default=False, example=True)
