from typing import Annotated, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.application.dtos.user_dto import (
    UserCreateDTO,
    UserQueryDTO,
    UserResponseDTO,
    UserUpdateDTO,
)
from app.application.services.user_service import UserService
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.user_id import UserId
from app.infrastructure.database import get_db
from app.infrastructure.repositories.user_repository import (
    SQLAlchemyUserRepository,
)

router = APIRouter()


def get_user_repository(db: Annotated[Session, Depends(get_db)]) -> UserRepository:
    """ユーザーリポジトリのインスタンスを取得する。

    Args:
        db: データベースセッション。

    Returns:
        ユーザーリポジトリのインスタンス。
    """
    return SQLAlchemyUserRepository(db)


def get_user_service(
    repo: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    """ユーザーサービスのインスタンスを取得する。

    Args:
        repo: ユーザーリポジトリのインスタンス。

    Returns:
        ユーザーサービスのインスタンス。
    """
    return UserService(repo)


@router.get("", response_model=List[UserResponseDTO])
def read_users(
    query: Annotated[UserQueryDTO, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
):
    """ユーザーの一覧を取得する。

    Args:
        query: クエリパラメータ（制限、オフセット、並び順）。
        service: ユーザーサービスのインスタンス。

    Returns:
        ユーザーのリスト。
    """
    return service.get_users(
        limit=query.limit,
        offset=query.offset,
        order_by=query.order_by,
        asc=query.asc,
    )


@router.post(
    "", response_model=UserResponseDTO, status_code=status.HTTP_201_CREATED
)
def create_user(
    user_create: UserCreateDTO,
    service: Annotated[UserService, Depends(get_user_service)],
):
    """新しいユーザーを作成する。

    Args:
        user_create: 作成するユーザーの情報。
        service: ユーザーサービスのインスタンス。

    Returns:
        作成されたユーザー。

    Raises:
        HTTPException: 入力が無効な場合やデータベースエラーが発生した場合。
    """
    try:
        return service.create_user(user_create)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
    except (ProgrammingError, OperationalError) as e:
        if "Table" in str(e) and "doesn't exist" in str(e):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="データベーステーブルが存在しません。マイグレーションを実行してください: `alembic upgrade head`",
            ) from e
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"データベースエラー: {str(e)}",
        ) from e


@router.get("/{user_id}", response_model=UserResponseDTO)
def read_user(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    """指定されたIDのユーザーを取得する。

    Args:
        user_id: ユーザーの一意識別子。
        service: ユーザーサービスのインスタンス。

    Returns:
        ユーザー情報。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合。
    """
    try:
        user = service.get_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put("/{user_id}", response_model=UserResponseDTO)
def update_user(
    user_id: str,
    user_update: UserUpdateDTO,
    service: Annotated[UserService, Depends(get_user_service)],
    repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    """指定されたIDのユーザー情報を更新する。

    Args:
        user_id: 更新するユーザーの一意識別子。
        user_update: 更新するユーザー情報。
        service: ユーザーサービスのインスタンス。
        repo: ユーザーリポジトリのインスタンス。

    Returns:
        更新されたユーザー情報。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合、または権限が不足している場合。
    """
    try:
        # manager_idが指定されている場合、更新者がマネージャー権限を持っているか確認
        if user_update.manager_id is not None and user_update.updated_by:
            try:
                # 更新者IDがUUID形式で、かつ更新者がマネージャー権限を持っていない場合はエラー
                updated_by_id = UserId(user_update.updated_by)
                if not repo.has_manager_role(updated_by_id):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Insufficient privileges to update manager ID",
                    )
            except ValueError:
                # 更新者IDが無効なUUID形式の場合、検証をスキップ
                pass
                
        user = service.update_user(user_id, user_update)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: str,
    updated_by: Annotated[str, Body(..., embed=True)],
    service: Annotated[UserService, Depends(get_user_service)],
):
    """指定されたIDのユーザーを削除する。

    Args:
        user_id: 削除するユーザーの一意識別子。
        updated_by: 更新者の識別子。
        service: ユーザーサービスのインスタンス。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合。
    """
    try:
        if not service.delete_user(user_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post("/{user_id}/promote-to-manager", response_model=UserResponseDTO)
def promote_user_to_manager(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    """指定されたIDのユーザーの権限を'user'から'manager'に昇格させる。

    Args:
        user_id: 昇格させるユーザーの一意識別子。
        service: ユーザーサービスのインスタンス。

    Returns:
        昇格されたユーザー情報。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合。
    """
    try:
        user = service.promote_user_to_manager(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post("/{user_id}/promote-to-admin", response_model=UserResponseDTO)
def promote_user_to_admin(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    """指定されたIDのユーザーの権限を'manager'から'admin'に昇格させる。

    Args:
        user_id: 昇格させるユーザーの一意識別子。
        service: ユーザーサービスのインスタンス。

    Returns:
        昇格されたユーザー情報。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合、または現在の役割が'manager'でない場合。
    """
    try:
        user = service.promote_user_to_admin(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found or is not currently a manager",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "/{user_id}/demote-from-admin-to-manager", response_model=UserResponseDTO
)
def demote_user_from_admin_to_manager(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    """指定されたIDのユーザーの権限を'admin'から'manager'に降格させる。

    Args:
        user_id: 降格させるユーザーの一意識別子。
        service: ユーザーサービスのインスタンス。

    Returns:
        降格されたユーザー情報。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合、または現在の役割が'admin'でない場合。
    """
    try:
        user = service.demote_user_from_admin_to_manager(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found or is not currently an admin",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "/{user_id}/demote-from-manager-to-user", response_model=UserResponseDTO
)
def demote_user_from_manager_to_user(
    user_id: str,
    service: Annotated[UserService, Depends(get_user_service)],
):
    """指定されたIDのユーザーの権限を'manager'から'user'に降格させる。

    Args:
        user_id: 降格させるユーザーの一意識別子。
        service: ユーザーサービスのインスタンス。

    Returns:
        降格されたユーザー情報。

    Raises:
        HTTPException: ユーザーが見つからない場合や入力が無効な場合、または現在の役割が'manager'でない場合。
    """
    try:
        user = service.demote_user_from_manager_to_user(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found or is not currently a manager",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
