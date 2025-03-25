from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    email: str
    name: str


class UserUpdateDTO(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponseDTO(BaseModel):
    id: str
    email: str
    name: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
