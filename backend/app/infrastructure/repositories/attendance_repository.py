from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app.domain.entities.attendance import Attendance
from app.domain.repositories.attendance_repository import AttendanceRepository
from app.domain.value_objects.attendance_id import AttendanceId
from app.domain.value_objects.user_id import UserId
from app.infrastructure.models.attendance import AttendanceModel


class SQLAlchemyAttendanceRepository(AttendanceRepository):
    def __init__(self, db: Session):
        self.db = db

    def find_by_id(self, attendance_id: AttendanceId) -> Optional[Attendance]:
        """IDで勤怠情報を検索"""
        attendance = (
            self.db.query(AttendanceModel)
            .filter(
                AttendanceModel.id == str(attendance_id),
                AttendanceModel.delete_flag == False,  # noqa: E712
            )
            .first()
        )
        if not attendance:
            return None
        return self._to_entity(attendance)

    def find_by_user_id_and_date(
        self,
        user_id: UserId,
        work_date: date,  # dateからwork_dateに変更
    ) -> Optional[Attendance]:
        """ユーザーIDと日付で勤怠情報を検索"""
        attendance = (
            self.db.query(AttendanceModel)
            .filter(
                AttendanceModel.user_id == str(user_id),
                AttendanceModel.work_date
                == work_date,  # dateからwork_dateに変更
                AttendanceModel.delete_flag == False,  # noqa: E712
            )
            .first()
        )
        if not attendance:
            return None
        return self._to_entity(attendance)

    def find_by_user_id(
        self,
        user_id: UserId,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Attendance]:
        """ユーザーIDで勤怠情報を検索"""
        query = self.db.query(AttendanceModel).filter(
            AttendanceModel.user_id == str(user_id),
            AttendanceModel.delete_flag == False,  # noqa: E712
        )

        # 日付の降順でソート
        query = query.order_by(desc(AttendanceModel.work_date))  # 変更

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        attendances = query.all()
        return [self._to_entity(attendance) for attendance in attendances]

    def find_by_date_range(
        self,
        start_date: date,
        end_date: date,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Attendance]:
        """日付範囲で勤怠情報を検索"""
        query = self.db.query(AttendanceModel).filter(
            AttendanceModel.work_date.between(start_date, end_date),  # 変更
            AttendanceModel.delete_flag == False,  # noqa: E712
        )

        # 日付の昇順でソート
        query = query.order_by(asc(AttendanceModel.work_date))  # 変更

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        attendances = query.all()
        return [self._to_entity(attendance) for attendance in attendances]

    def find_by_user_id_and_date_range(
        self,
        user_id: UserId,
        start_date: date,
        end_date: date,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[Attendance]:
        """ユーザーIDと日付範囲で勤怠情報を検索"""
        query = self.db.query(AttendanceModel).filter(
            AttendanceModel.user_id == str(user_id),
            AttendanceModel.work_date.between(start_date, end_date),  # 変更
            AttendanceModel.delete_flag == False,  # noqa: E712
        )

        # 日付の昇順でソート
        query = query.order_by(asc(AttendanceModel.work_date))  # 変更

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        attendances = query.all()
        return [self._to_entity(attendance) for attendance in attendances]

    def find_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        asc: bool = True,
    ) -> List[Attendance]:
        """全ての勤怠情報を検索"""
        query = self.db.query(AttendanceModel).filter(
            AttendanceModel.delete_flag == False  # noqa: E712
        )

        if order_by:
            column = getattr(AttendanceModel, order_by, None)
            if column is not None:
                query = query.order_by(column.asc() if asc else column.desc())
        else:
            # デフォルトは日付の降順
            query = query.order_by(desc(AttendanceModel.work_date))  # 変更

        if offset:
            query = query.offset(offset)
        if limit:
            query = query.limit(limit)

        attendances = query.all()
        return [self._to_entity(attendance) for attendance in attendances]

    def save(self, attendance: Attendance) -> Attendance:
        """勤怠情報を保存"""
        try:
            db_attendance = (
                self.db.query(AttendanceModel)
                .filter(AttendanceModel.id == str(attendance.id))
                .first()
            )

            if not db_attendance:
                # 新規作成
                db_attendance = AttendanceModel(
                    id=str(attendance.id),
                    work_date=attendance.work_date,  # 変更
                    clock_in=attendance.clock_in,
                    clock_out=attendance.clock_out,
                    rest_in=attendance.rest_in,
                    rest_out=attendance.rest_out,
                    user_id=str(attendance.user_id),
                    work_place=attendance.work_place,
                    transportation_expenses=attendance.transportation_expenses,
                    remarks=attendance.remarks,
                    delete_flag=attendance.delete_flag,
                    created_at=attendance.created_at,
                    created_by=attendance.created_by,
                    updated_at=attendance.updated_at,
                    updated_by=attendance.updated_by,
                )
                self.db.add(db_attendance)
            else:
                # 更新
                db_attendance.work_date = attendance.work_date  # 変更
                db_attendance.clock_in = attendance.clock_in
                db_attendance.clock_out = attendance.clock_out
                db_attendance.rest_in = attendance.rest_in
                db_attendance.rest_out = attendance.rest_out
                db_attendance.work_place = attendance.work_place
                db_attendance.transportation_expenses = (
                    attendance.transportation_expenses
                )
                db_attendance.remarks = attendance.remarks
                db_attendance.delete_flag = attendance.delete_flag
                db_attendance.updated_at = datetime.now()
                db_attendance.updated_by = attendance.updated_by

            self.db.commit()
            self.db.refresh(db_attendance)
            return self._to_entity(db_attendance)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, attendance_id: AttendanceId) -> None:
        """勤怠情報を削除（論理削除）"""
        try:
            db_attendance = (
                self.db.query(AttendanceModel)
                .filter(AttendanceModel.id == str(attendance_id))
                .first()
            )
            if db_attendance:
                db_attendance.delete_flag = True
                db_attendance.updated_at = datetime.now()
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def _to_entity(self, model: AttendanceModel) -> Attendance:
        """モデルからエンティティへの変換"""
        return Attendance(
            id=AttendanceId(model.id),
            work_date=model.work_date,  # 変更
            clock_in=model.clock_in,
            clock_out=model.clock_out,
            rest_in=model.rest_in,
            rest_out=model.rest_out,
            user_id=UserId(model.user_id),
            work_place=model.work_place,
            transportation_expenses=model.transportation_expenses,
            remarks=model.remarks,
            delete_flag=model.delete_flag,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
        )
