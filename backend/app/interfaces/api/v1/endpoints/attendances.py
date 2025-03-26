from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.exc import OperationalError, ProgrammingError
from sqlalchemy.orm import Session

from app.application.dtos.attendance_dto import (
    AttendanceCreateDTO,
    AttendanceQueryDTO,
    AttendanceResponseDTO,
    AttendanceUpdateDTO,
)
from app.application.services.attendance_service import AttendanceService
from app.domain.repositories.attendance_repository import AttendanceRepository
from app.infrastructure.database import get_db
from app.infrastructure.repositories.attendance_repository import (
    SQLAlchemyAttendanceRepository,
)

router = APIRouter()


def get_attendance_repository(
    db: Session = Depends(get_db),
) -> AttendanceRepository:
    return SQLAlchemyAttendanceRepository(db)


def get_attendance_service(
    repo: AttendanceRepository = Depends(get_attendance_repository),
) -> AttendanceService:
    return AttendanceService(repo)


@router.get("", response_model=List[AttendanceResponseDTO])
def read_attendances(
    query: AttendanceQueryDTO = Depends(),
    service: AttendanceService = Depends(get_attendance_service),
):
    """勤怠情報一覧を取得"""
    try:
        return service.get_attendances(
            user_id=query.user_id,
            start_date=query.start_date,
            end_date=query.end_date,
            limit=query.limit,
            offset=query.offset,
            order_by=query.order_by,
            asc=query.asc,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.post(
    "",
    response_model=AttendanceResponseDTO,
    status_code=status.HTTP_201_CREATED,
)
def create_attendance(
    attendance_create: AttendanceCreateDTO,
    service: AttendanceService = Depends(get_attendance_service),
):
    """新しい勤怠情報を作成"""
    try:
        return service.create_attendance(attendance_create)
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


@router.get("/{attendance_id}", response_model=AttendanceResponseDTO)
def read_attendance(
    attendance_id: str,
    service: AttendanceService = Depends(get_attendance_service),
):
    """勤怠情報を取得"""
    try:
        attendance = service.get_attendance(attendance_id)
        if attendance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance with ID {attendance_id} not found",
            )
        return attendance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.put("/{attendance_id}", response_model=AttendanceResponseDTO)
def update_attendance(
    attendance_id: str,
    attendance_update: AttendanceUpdateDTO,
    service: AttendanceService = Depends(get_attendance_service),
):
    """勤怠情報を更新"""
    try:
        attendance = service.update_attendance(
            attendance_id, attendance_update
        )
        if attendance is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance with ID {attendance_id} not found",
            )
        return attendance
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e


@router.delete("/{attendance_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_attendance(
    attendance_id: str,
    updated_by: str = Body(..., embed=True),
    service: AttendanceService = Depends(get_attendance_service),
):
    """勤怠情報を削除（論理削除）"""
    try:
        if not service.delete_attendance(attendance_id, updated_by):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Attendance with ID {attendance_id} not found",
            )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
        ) from e
