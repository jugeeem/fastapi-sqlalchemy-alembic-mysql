import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.infrastructure.models.user import UserModel
from app.infrastructure.models.user_info import UserInfoModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        """SQLAlchemyUserRepositoryを初期化する。

        Args:
            db: SQLAlchemyデータベースセッション。
        """
        self.db = db

    def find_by_id(self, user_id: UserId) -> Optional[User]:
        """IDでユーザーを検索する。

        Args:
            user_id: ユーザーの一意識別子。

        Returns:
            見つかった場合はUserエンティティ、見つからない場合はNone。
        """
        user = (
            self.db.query(UserModel)
            .filter(
                UserModel.id == str(user_id),
                UserModel.delete_flag == False,  # noqa: E712
            )
            .first()
        )
        if not user:
            return None
        user_info = (
            self.db.query(UserInfoModel)
            .filter(
                UserInfoModel.user_id == str(user_id),
                UserInfoModel.delete_flag == False,  # noqa: E712
            )
            .first()
        )

        return self._to_entity(user, user_info)

    def find_by_email(self, email: Email) -> Optional[User]:
        """メールアドレスでユーザーを検索する。

        Args:
            email: ユーザーのメールアドレス。

        Returns:
            見つかった場合はUserエンティティ、見つからない場合はNone。
        """
        user = (
            self.db.query(UserModel)
            .filter(
                UserModel.email == str(email),
                UserModel.delete_flag == False,  # noqa: E712
            )
            .first()
        )
        if not user:
            return None
        user_info = (
            self.db.query(UserInfoModel)
            .filter(
                UserInfoModel.user_id == user.id,
                UserInfoModel.delete_flag == False,  # noqa: E712
            )
            .first()
        )

        return self._to_entity(user, user_info)

    def find_all(
        self,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        order_by: Optional[str] = None,
        asc: bool = True,
    ) -> List[User]:
        """削除されていないすべてのユーザーをページング付きでソートして検索する。

        Args:
            limit: 返すユーザーの最大数。
            offset: スキップするユーザーの数。
            order_by: ソートするカラム名。
            asc: Trueの場合は昇順、Falseの場合は降順でソート。

        Returns:
            Userエンティティのリスト。
        """
        query = self.db.query(UserModel).filter(UserModel.delete_flag == False)  # noqa: E712
        if order_by:
            column = getattr(UserModel, order_by, None)
            if column is not None:
                query = query.order_by(column.asc() if asc else column.desc())
        if offset is not None:
            query = query.offset(offset)
        if limit is not None:
            query = query.limit(limit)
        users = query.all()
        result = []
        for user in users:
            user_info = (
                self.db.query(UserInfoModel)
                .filter(
                    UserInfoModel.user_id == user.id,
                    UserInfoModel.delete_flag == False,  # noqa: E712
                )
                .first()
            )
            result.append(self._to_entity(user, user_info))

        return result

    def save(self, user: User) -> User:
        """ユーザーを保存または更新する。

        ユーザーが存在しない場合は新しいユーザーレコードを作成し、
        存在する場合は既存のユーザーレコードを更新する。

        Args:
            user: 保存するUserエンティティ。

        Returns:
            保存されたUserエンティティ。

        Raises:
            Exception: データベース操作が失敗した場合。
        """
        try:
            db_user = (
                self.db.query(UserModel)
                .filter(UserModel.id == str(user.id))
                .first()
            )
            if not db_user:
                db_user = UserModel(
                    id=str(user.id),
                    email=str(user.email),
                    username=user.username,
                    password=user.password,
                    manager_id=user.manager_id,
                    remarks=user.remarks,
                    delete_flag=user.delete_flag,
                    created_at=user.created_at,
                    created_by=user.created_by,
                    updated_at=user.updated_at,
                    updated_by=user.updated_by,
                )
                self.db.add(db_user)
                db_user_info = UserInfoModel(
                    id=str(uuid.uuid4()),
                    user_id=str(user.id),
                    first_name=user.first_name,
                    first_name_ruby=user.first_name_ruby,
                    last_name=user.last_name,
                    last_name_ruby=user.last_name_ruby,
                    phone_number=user.phone_number,
                    zip_code=user.zip_code,
                    address=user.address,
                    delete_flag=False,
                    created_at=user.created_at,
                    created_by=user.created_by,
                    updated_at=user.updated_at,
                    updated_by=user.updated_by,
                )
                self.db.add(db_user_info)
            else:
                db_user.email = str(user.email)
                db_user.username = user.username
                db_user.password = user.password
                db_user.manager_id = user.manager_id
                db_user.remarks = user.remarks
                db_user.delete_flag = user.delete_flag
                db_user.updated_at = datetime.now()
                db_user.updated_by = user.updated_by
                db_user_info = (
                    self.db.query(UserInfoModel)
                    .filter(
                        UserInfoModel.user_id == str(user.id),
                        UserInfoModel.delete_flag == False,  # noqa: E712
                    )
                    .first()
                )

                if not db_user_info:
                    db_user_info = UserInfoModel(
                        id=str(uuid.uuid4()),
                        user_id=str(user.id),
                        first_name=user.first_name,
                        first_name_ruby=user.first_name_ruby,
                        last_name=user.last_name,
                        last_name_ruby=user.last_name_ruby,
                        phone_number=user.phone_number,
                        zip_code=user.zip_code,
                        address=user.address,
                        delete_flag=False,
                        created_at=user.created_at,
                        created_by=user.created_by,
                        updated_at=user.updated_at,
                        updated_by=user.updated_by,
                    )
                    self.db.add(db_user_info)
                else:
                    db_user_info.first_name = user.first_name
                    db_user_info.first_name_ruby = user.first_name_ruby
                    db_user_info.last_name = user.last_name
                    db_user_info.last_name_ruby = user.last_name_ruby
                    db_user_info.phone_number = user.phone_number
                    db_user_info.zip_code = user.zip_code
                    db_user_info.address = user.address
                    db_user_info.updated_at = datetime.now()
                    db_user_info.updated_by = user.updated_by
            self.db.commit()
            self.db.refresh(db_user)
            db_user_info = (
                self.db.query(UserInfoModel)
                .filter(
                    UserInfoModel.user_id == str(user.id),
                    UserInfoModel.delete_flag == False,  # noqa: E712
                )
                .first()
            )

            return self._to_entity(db_user, db_user_info)
        except Exception as e:
            self.db.rollback()
            raise e

    def delete(self, user_id: UserId) -> None:
        """ユーザーを削除済みとしてマークする。

        Args:
            user_id: 削除するユーザーの一意識別子。

        Raises:
            Exception: データベース操作が失敗した場合。
        """
        try:
            db_user = (
                self.db.query(UserModel)
                .filter(UserModel.id == str(user_id))
                .first()
            )
            if db_user:
                db_user.delete_flag = True
                db_user.updated_at = datetime.now()
                db_user_info = (
                    self.db.query(UserInfoModel)
                    .filter(UserInfoModel.user_id == str(user_id))
                    .first()
                )
                if db_user_info:
                    db_user_info.delete_flag = True
                    db_user_info.updated_at = datetime.now()
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e

    def _to_entity(
        self, model: UserModel, info_model: Optional[UserInfoModel] = None
    ) -> User:
        """データベースモデルをUserエンティティに変換する。

        Args:
            model: ユーザーデータベースモデル。
            info_model: 利用可能な場合、ユーザー情報データベースモデル。

        Returns:
            提供されたモデルからのデータを持つUserエンティティ。
        """
        first_name = None
        first_name_ruby = None
        last_name = None
        last_name_ruby = None
        phone_number = None
        zip_code = None
        address = None
        if info_model:
            first_name = info_model.first_name
            first_name_ruby = info_model.first_name_ruby
            last_name = info_model.last_name
            last_name_ruby = info_model.last_name_ruby
            phone_number = info_model.phone_number
            zip_code = info_model.zip_code
            address = info_model.address

        return User(
            id=UserId(model.id),
            email=Email(model.email),
            username=model.username,
            password=model.password,
            manager_id=model.manager_id,
            remarks=model.remarks,
            delete_flag=model.delete_flag,
            created_at=model.created_at,
            created_by=model.created_by,
            updated_at=model.updated_at,
            updated_by=model.updated_by,
            first_name=first_name,
            first_name_ruby=first_name_ruby,
            last_name=last_name,
            last_name_ruby=last_name_ruby,
            phone_number=phone_number,
            zip_code=zip_code,
            address=address,
        )
