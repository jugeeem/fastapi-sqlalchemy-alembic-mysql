from datetime import date, datetime, time
from typing import List, Optional

from app.application.dtos.attendance_dto import (
    AttendanceCreateDTO,
    AttendanceResponseDTO,
    AttendanceUpdateDTO,
)
from app.domain.entities.attendance import Attendance
from app.domain.repositories.attendance_repository import AttendanceRepository
from app.domain.value_objects.attendance_id import AttendanceId
from app.domain.value_objects.user_id import UserId


class AttendanceService:
    def __init__(self, attendance_repository: AttendanceRepository):
        self.attendance_repository = attendance_repository

    def get_attendance(
        self, attendance_id: str
    ) -> Optional[AttendanceResponseDTO]:
        """指定されたIDの勤怠情報を取得する"""
        try:
            attendance_id_vo = AttendanceId(attendance_id)
        except ValueError as err:
            raise ValueError(
                f"Invalid attendance ID: {attendance_id}"
            ) from err

        attendance = self.attendance_repository.find_by_id(attendance_id_vo)
        if not attendance:
            return None

        return self._to_response_dto(attendance)

    def get_attendances(
        self,
        user_id: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        asc: bool = True,
    ) -> List[AttendanceResponseDTO]:
        """勤怠情報のリストを取得する"""
        attendances = []

        if user_id and start_date and end_date:
            # ユーザーIDと日付範囲で検索
            try:
                user_id_vo = UserId(user_id)
                attendances = (
                    self.attendance_repository.find_by_user_id_and_date_range(
                        user_id_vo, start_date, end_date, limit, offset
                    )
                )
            except ValueError as err:
                raise ValueError(f"Invalid user ID: {user_id}") from err
        elif user_id:
            # ユーザーIDで検索
            try:
                user_id_vo = UserId(user_id)
                attendances = self.attendance_repository.find_by_user_id(
                    user_id_vo, limit, offset
                )
            except ValueError as err:
                raise ValueError(f"Invalid user ID: {user_id}") from err
        elif start_date and end_date:
            # 日付範囲で検索
            attendances = self.attendance_repository.find_by_date_range(
                start_date, end_date, limit, offset
            )
        else:
            # 全件検索
            attendances = self.attendance_repository.find_all(
                limit, offset, order_by, asc
            )

        return [
            self._to_response_dto(attendance) for attendance in attendances
        ]

    def create_attendance(
        self, data: AttendanceCreateDTO
    ) -> AttendanceResponseDTO:
        """新しい勤怠情報を作成する"""
        try:
            user_id_vo = UserId(data.user_id)
        except ValueError as err:
            raise ValueError(f"Invalid user ID: {data.user_id}") from err

        # 同じユーザーの同じ日付の勤怠が既に存在するかチェック
        existing_attendance = (
            self.attendance_repository.find_by_user_id_and_date(
                user_id_vo,
                data.work_date,  # dateからwork_dateに変更
            )
        )
        if existing_attendance:
            raise ValueError(
                f"Attendance record for user {data.user_id} on {data.work_date} already exists"  # 変更
            )

        # 打刻時間の検証
        self._validate_clock_times(
            data.clock_in, data.clock_out, data.rest_in, data.rest_out
        )

        attendance = Attendance(
            id=AttendanceId.generate(),
            work_date=data.work_date,  # 変更
            clock_in=data.clock_in,
            clock_out=data.clock_out,
            rest_in=data.rest_in,
            rest_out=data.rest_out,
            user_id=user_id_vo,
            work_place=data.work_place,
            transportation_expenses=data.transportation_expenses,
            remarks=data.remarks,
            delete_flag=False,
            created_at=datetime.now(),
            created_by=data.created_by,
            updated_at=datetime.now(),
            updated_by=data.updated_by,
        )

        created_attendance = self.attendance_repository.save(attendance)
        return self._to_response_dto(created_attendance)

    def update_attendance(
        self, attendance_id: str, data: AttendanceUpdateDTO
    ) -> Optional[AttendanceResponseDTO]:
        """勤怠情報を更新する"""
        try:
            attendance_id_vo = AttendanceId(attendance_id)
        except ValueError as err:
            raise ValueError(
                f"Invalid attendance ID: {attendance_id}"
            ) from err

        attendance = self.attendance_repository.find_by_id(attendance_id_vo)
        if not attendance:
            return None

        # 打刻時間のバリデーション（更新される場合のみ）
        if (
            data.clock_in is not None
            or data.clock_out is not None
            or data.rest_in is not None
            or data.rest_out is not None
        ):
            self._validate_clock_times(
                data.clock_in or attendance.clock_in,
                data.clock_out or attendance.clock_out,
                data.rest_in or attendance.rest_in,
                data.rest_out or attendance.rest_out,
            )

        updated_attendance = attendance.update(
            date=data.date,
            clock_in=data.clock_in,
            clock_out=data.clock_out,
            rest_in=data.rest_in,
            rest_out=data.rest_out,
            work_place=data.work_place,
            transportation_expenses=data.transportation_expenses,
            remarks=data.remarks,
            updated_by=data.updated_by,
        )

        saved_attendance = self.attendance_repository.save(updated_attendance)
        return self._to_response_dto(saved_attendance)

    def delete_attendance(self, attendance_id: str, updated_by: str) -> bool:
        """勤怠情報を削除する（論理削除）"""
        try:
            attendance_id_vo = AttendanceId(attendance_id)
        except ValueError as err:
            raise ValueError(
                f"Invalid attendance ID: {attendance_id}"
            ) from err

        attendance = self.attendance_repository.find_by_id(attendance_id_vo)
        if not attendance:
            return False

        # 論理削除状態に更新
        updated_attendance = attendance.deactivate()
        # updated_byの更新
        updated_attendance = updated_attendance.update(updated_by=updated_by)
        self.attendance_repository.save(updated_attendance)
        return True

    def _to_response_dto(
        self, attendance: Attendance
    ) -> AttendanceResponseDTO:
        """エンティティからDTOへの変換"""
        return AttendanceResponseDTO(
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
            working_hours=attendance.calculate_working_hours(),
            rest_hours=attendance.calculate_rest_hours(),
            delete_flag=attendance.delete_flag,
            created_at=attendance.created_at,
            created_by=attendance.created_by,
            updated_at=attendance.updated_at,
            updated_by=attendance.updated_by,
        )

    def _validate_clock_times(
        self, clock_in: time, clock_out: time, rest_in: time, rest_out: time
    ):
        """打刻時間の検証"""
        # 出勤時刻 < 休憩開始時刻 < 休憩終了時刻 < 退勤時刻の順序を検証
        if clock_in >= rest_in:
            raise ValueError("Clock-in time must be before rest-in time")
        if rest_in >= rest_out:
            raise ValueError("Rest-in time must be before rest-out time")
        if rest_out >= clock_out:
            raise ValueError("Rest-out time must be before clock-out time")
