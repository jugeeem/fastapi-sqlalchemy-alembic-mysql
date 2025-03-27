from datetime import timedelta
from typing import Annotated, Dict, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import settings
from app.infrastructure.database import get_db
from app.infrastructure.models.user import UserModel
from app.infrastructure.security.token import (
    create_access_token,
    get_current_active_user,
    get_current_user,
    verify_password,
)

router = APIRouter()


class Token(BaseModel):
    """トークンレスポンスモデル"""
    access_token: str
    token_type: str


class UserInfo(BaseModel):
    """ユーザー情報レスポンスモデル"""
    id: str
    username: str
    email: str
    role: Optional[str] = None


def authenticate_user(db: Session, username: str, password: str) -> Optional[UserModel]:
    """ユーザーを認証する

    Args:
        db: データベースセッション
        username: ユーザー名
        password: パスワード

    Returns:
        認証成功時、ユーザーモデル。失敗時、None。
    """
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    if user.delete_flag:
        return None
    return user


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
) -> Token:
    """アクセストークンを取得する

    Args:
        form_data: フォームデータ
        db: データベースセッション

    Returns:
        トークン情報

    Raises:
        HTTPException: 認証に失敗した場合
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="ユーザー名またはパスワードが正しくありません",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=UserInfo)
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_active_user)],
) -> Dict[str, str]:
    """現在のユーザー情報を取得する

    Args:
        current_user: 現在のユーザー

    Returns:
        ユーザー情報
    """
    # ユーザーのロールを取得
    role = current_user.roles[0].role_name if current_user.roles else None
    
    return {
        "id": str(current_user.id),
        "username": current_user.username,
        "email": current_user.email,
        "role": role,
    }
