from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.domain.value_objects.user_id import UserId
from app.infrastructure.database import get_db
from app.infrastructure.models.user import UserModel

# パスワードハッシュ化のコンテキスト
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2スキーム
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/token"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """パスワードを検証する

    Args:
        plain_password: 平文パスワード
        hashed_password: ハッシュ化されたパスワード

    Returns:
        検証結果
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """パスワードをハッシュ化する

    Args:
        password: 平文パスワード

    Returns:
        ハッシュ化されたパスワード
    """
    return pwd_context.hash(password)


def create_access_token(
    data: Dict[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """アクセストークンを作成する

    Args:
        data: トークンにエンコードするデータ
        expires_delta: 有効期限

    Returns:
        JWT形式のアクセストークン
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
) -> UserModel:
    """現在のユーザーを取得する

    Args:
        token: アクセストークン
        db: データベースセッション

    Returns:
        ユーザーモデル

    Raises:
        HTTPException: 認証情報が無効な場合
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="認証情報を検証できませんでした",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception

    try:
        user_id_vo = UserId(user_id)
    except ValueError:
        raise credentials_exception

    user = db.query(UserModel).filter(UserModel.id == str(user_id_vo)).first()
    if user is None:
        raise credentials_exception
    if user.delete_flag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無効なユーザーです",
        )
    return user


def get_current_active_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """アクティブな現在のユーザーを取得する

    Args:
        current_user: 現在のユーザー

    Returns:
        ユーザーモデル

    Raises:
        HTTPException: ユーザーが無効な場合
    """
    if current_user.delete_flag:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="無効なユーザーです",
        )
    return current_user
