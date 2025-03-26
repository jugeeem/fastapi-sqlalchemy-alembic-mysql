from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserCreateDTO(BaseModel):
    email: str
    username: str
    password: str
    manager_id: str
    remarks: Optional[str] = None
    created_by: str
    updated_by: str
    first_name: Optional[str] = None
    first_name_ruby: Optional[str] = None
    last_name: Optional[str] = None
    last_name_ruby: Optional[str] = None
    phone_number: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None


class UserUpdateDTO(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    manager_id: Optional[str] = None
    remarks: Optional[str] = None
    delete_flag: Optional[bool] = None
    updated_by: str
    first_name: Optional[str] = None
    first_name_ruby: Optional[str] = None
    last_name: Optional[str] = None
    last_name_ruby: Optional[str] = None
    phone_number: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None


class UserQueryDTO(BaseModel):
    limit: Optional[int] = None
    offset: Optional[int] = None
    order_by: Optional[str] = None
    asc: bool = True


class UserResponseDTO(BaseModel):
    id: str
    email: str
    username: str
    manager_id: str
    remarks: Optional[str] = None
    delete_flag: bool
    created_at: datetime
    created_by: str
    updated_at: datetime
    updated_by: str
    first_name: Optional[str] = None
    first_name_ruby: Optional[str] = None
    last_name: Optional[str] = None
    last_name_ruby: Optional[str] = None
    phone_number: Optional[str] = None
    zip_code: Optional[str] = None
    address: Optional[str] = None
