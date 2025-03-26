from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.infrastructure.database import get_db
from app.infrastructure.models.role import RoleModel

router = APIRouter()


@router.post("/roles", status_code=status.HTTP_201_CREATED)
def initialize_roles(db: Annotated[Session, Depends(get_db)]):
    """RoleModelに初期データを投入するエンドポイント"""
    initial_roles = [
        {"role_name": "admin", "description": "システム管理者権限"},
        {"role_name": "manager", "description": "管理者権限"},
        {"role_name": "user", "description": "一般ユーザー権限"},
        {"role_name": "guest", "description": "閲覧のみ可能な権限"},
    ]
    created_roles = []
    existing_roles = []
    for role_data in initial_roles:
        existing_role = (
            db.query(RoleModel)
            .filter(RoleModel.role_name == role_data["role_name"])
            .first()
        )
        if existing_role:
            existing_roles.append(role_data["role_name"])
            continue
        new_role = RoleModel(**role_data)
        db.add(new_role)
        created_roles.append(role_data["role_name"])
    try:
        db.commit()
        return {
            "status": "success",
            "message": "ロールの初期化が完了しました",
            "created": created_roles,
            "already_exists": existing_roles,
        }
    except IntegrityError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ロールの初期化中にエラーが発生しました。重複したデータがある可能性があります。",
        ) from err
