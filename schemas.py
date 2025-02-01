from pydantic import BaseModel, Field
from typing import Optional

class Register(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, examples=["JohnDoe"])
    password: str = Field(..., min_length=6, examples=["strong_password"])
    email: str = Field(..., examples=["johndoe@example.com"])
    is_active: Optional[bool] = Field(default=True, examples=[True])
    is_staff: Optional[bool] = Field(default=False, examples=[False])



class Login(BaseModel):
    username: str = Field(..., min_length=3, max_length=25, examples=['johndoe'])
    password: str = Field(..., min_length=6, examples=['strong_password'])
