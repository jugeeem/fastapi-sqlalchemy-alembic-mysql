import uuid
from datetime import datetime
from typing import List, Optional

from sqlalchemy.orm import Session

from app.domain.entities.user import User
from app.domain.repositories.user_repository import UserRepository
from app.domain.value_objects.email import Email
from app.domain.value_objects.user_id import UserId
from app.infrastructure.models.role import RoleModel
from app.infrastructure.models.user import UserModel
from app.infrastructure.models.user_info import UserInfoModel
from app.infrastructure.models.user_role import UserRoleModel


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

    def create(self, user: User) -> User:
        """新しいユーザーを作成する。

        Args:
            user: 作成するUserエンティティ。

        Returns:
            作成されたUserエンティティ。

        Raises:
            Exception: データベース操作が失敗した場合。
        """
        try:
            # 既存のユーザーがないか確認
            existing_user = (
                self.db.query(UserModel)
                .filter(UserModel.id == str(user.id))
                .first()
            )
            if existing_user:
                raise ValueError(f"User with ID {user.id} already exists")

            # ユーザーモデルを作成
            db_user = UserModel(
                id=str(user.id),
                email=str(user.email),
                username=user.username,
                password=user.password,
                manager_id=user.manager_id if user.manager_id else None,  # manager_idがnullを許容するように
                remarks=user.remarks,
                delete_flag=user.delete_flag,
                created_at=user.created_at,
                created_by=user.created_by,
                updated_at=user.updated_at,
                updated_by=user.updated_by,
            )
            self.db.add(db_user)

            # ユーザー情報モデルを作成
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
            
            # デフォルトのユーザーロールを追加
            user_role = (
                self.db.query(RoleModel)
                .filter(
                    RoleModel.role_name == RoleModel.USER_ROLE,
                    RoleModel.delete_flag == False  # noqa: E712
                )
                .first()
            )
            
            if not user_role:
                raise ValueError(f"Role {RoleModel.USER_ROLE} not found")
            
            db_user_role = UserRoleModel(
                id=str(uuid.uuid4()),
                user_id=str(user.id),
                role_id=user_role.id,
                delete_flag=False,
                created_at=user.created_at,
                created_by=user.created_by,
                updated_at=user.updated_at,
                updated_by=user.updated_by,
            )
            self.db.add(db_user_role)
            
            self.db.commit()
            self.db.refresh(db_user)

            return self._to_entity(db_user, db_user_info)
        except Exception as e:
            self.db.rollback()
            raise e

    def update(self, user: User) -> User:
        """既存のユーザーを更新する。

        Args:
            user: 更新するUserエンティティ。

        Returns:
            更新されたUserエンティティ。

        Raises:
            Exception: データベース操作が失敗した場合。
            ValueError: manager_idに設定しようとしているユーザーが存在しない場合、
                      またはマネージャー権限がない場合。
        """
        try:
            db_user = (
                self.db.query(UserModel)
                .filter(UserModel.id == str(user.id))
                .first()
            )
            if not db_user:
                raise ValueError(f"User with ID {user.id} not found")

            # manager_idが変更された場合、そのユーザーが存在し、マネージャー権限を持っているか確認
            if user.manager_id != db_user.manager_id and user.manager_id is not None:
                try:
                    # manager_idとして設定されるユーザーが存在するか確認
                    manager_id_vo = UserId(user.manager_id)
                    manager = (
                        self.db.query(UserModel)
                        .filter(
                            UserModel.id == str(manager_id_vo),
                            UserModel.delete_flag == False,  # noqa: E712
                        )
                        .first()
                    )
                    if not manager:
                        raise ValueError(f"Manager with ID {user.manager_id} not found")
                    
                    if not self.has_manager_role(manager_id_vo):
                        raise ValueError(
                            f"User with ID {user.manager_id} does not have manager privileges"
                        )
                except ValueError as e:
                    raise ValueError(f"Invalid manager ID: {str(e)}") from e

            db_user.email = str(user.email)
            db_user.username = user.username
            db_user.password = user.password
            db_user.manager_id = user.manager_id
            db_user.remarks = user.remarks
            db_user.delete_flag = user.delete_flag
            db_user.updated_at = datetime.now()
            db_user.updated_by = user.updated_by

            # ユーザー情報モデルを取得または作成
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

    def promote_to_manager(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'user'から'manager'に昇格させる。

        Args:
            user_id: 昇格させるユーザーの一意識別子。

        Returns:
            昇格させたユーザー。見つからない場合はNone。
        """
        try:
            # ユーザーが存在するか確認
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
            
            # userロールを持っているかチェック
            user_role = (
                self.db.query(UserRoleModel, RoleModel)
                .join(RoleModel, UserRoleModel.role_id == RoleModel.id)
                .filter(
                    UserRoleModel.user_id == str(user_id),
                    UserRoleModel.delete_flag == False,  # noqa: E712
                    RoleModel.role_name == RoleModel.USER_ROLE
                )
                .first()
            )
            
            if not user_role:
                return None
                
            # managerロールを取得
            manager_role = (
                self.db.query(RoleModel)
                .filter(
                    RoleModel.role_name == RoleModel.MANAGER_ROLE,
                    RoleModel.delete_flag == False  # noqa: E712
                )
                .first()
            )
            
            if not manager_role:
                raise ValueError(f"Role {RoleModel.MANAGER_ROLE} not found")
            
            # userロールを削除（または非アクティブ化）
            user_role_model = user_role[0]
            user_role_model.delete_flag = True
            user_role_model.updated_at = datetime.now()
            
            # managerロールを追加
            new_role = UserRoleModel(
                id=str(uuid.uuid4()),
                user_id=str(user_id),
                role_id=manager_role.id,
                delete_flag=False,
                created_at=datetime.now(),
                created_by=user.updated_by,
                updated_at=datetime.now(),
                updated_by=user.updated_by
            )
            self.db.add(new_role)
            
            # ユーザー更新時間を更新
            user.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(user)
            
            # ユーザー情報を取得して返す
            user_info = (
                self.db.query(UserInfoModel)
                .filter(
                    UserInfoModel.user_id == str(user_id),
                    UserInfoModel.delete_flag == False,  # noqa: E712
                )
                .first()
            )
            
            return self._to_entity(user, user_info)
        except Exception as e:
            self.db.rollback()
            raise e

    def promote_to_admin(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'manager'から'admin'に昇格させる。

        Args:
            user_id: 昇格させるユーザーの一意識別子。

        Returns:
            昇格させたユーザー。見つからないか現在の役割が'manager'でない場合はNone。
        """
        try:
            # ユーザーが存在するか確認
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
            
            # managerロールを持っているかチェック
            manager_role = (
                self.db.query(UserRoleModel, RoleModel)
                .join(RoleModel, UserRoleModel.role_id == RoleModel.id)
                .filter(
                    UserRoleModel.user_id == str(user_id),
                    UserRoleModel.delete_flag == False,  # noqa: E712
                    RoleModel.role_name == RoleModel.MANAGER_ROLE
                )
                .first()
            )
            
            if not manager_role:
                return None
                
            # adminロールを取得
            admin_role = (
                self.db.query(RoleModel)
                .filter(
                    RoleModel.role_name == RoleModel.ADMIN_ROLE,
                    RoleModel.delete_flag == False  # noqa: E712
                )
                .first()
            )
            
            if not admin_role:
                raise ValueError(f"Role {RoleModel.ADMIN_ROLE} not found")
            
            # managerロールを削除（または非アクティブ化）
            manager_role_model = manager_role[0]
            manager_role_model.delete_flag = True
            manager_role_model.updated_at = datetime.now()
            
            # adminロールを追加
            new_role = UserRoleModel(
                id=str(uuid.uuid4()),
                user_id=str(user_id),
                role_id=admin_role.id,
                delete_flag=False,
                created_at=datetime.now(),
                created_by=user.updated_by,
                updated_at=datetime.now(),
                updated_by=user.updated_by
            )
            self.db.add(new_role)
            
            # ユーザー更新時間を更新
            user.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(user)
            
            # ユーザー情報を取得して返す
            user_info = (
                self.db.query(UserInfoModel)
                .filter(
                    UserInfoModel.user_id == str(user_id),
                    UserInfoModel.delete_flag == False,  # noqa: E712
                )
                .first()
            )
            
            return self._to_entity(user, user_info)
        except Exception as e:
            self.db.rollback()
            raise e

    def demote_from_admin_to_manager(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'admin'から'manager'に降格させる。

        Args:
            user_id: 降格させるユーザーの一意識別子。

        Returns:
            降格させたユーザー。見つからないか現在の役割が'admin'でない場合はNone。
        """
        try:
            # 同様のパターンでadminからmanagerへの降格処理を実装
            # ユーザーが存在するか確認
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
            
            # adminロールを持っているかチェック
            admin_role = (
                self.db.query(UserRoleModel, RoleModel)
                .join(RoleModel, UserRoleModel.role_id == RoleModel.id)
                .filter(
                    UserRoleModel.user_id == str(user_id),
                    UserRoleModel.delete_flag == False,  # noqa: E712
                    RoleModel.role_name == RoleModel.ADMIN_ROLE
                )
                .first()
            )
            
            if not admin_role:
                return None
                
            # managerロールを取得
            manager_role = (
                self.db.query(RoleModel)
                .filter(
                    RoleModel.role_name == RoleModel.MANAGER_ROLE,
                    RoleModel.delete_flag == False  # noqa: E712
                )
                .first()
            )
            
            if not manager_role:
                raise ValueError(f"Role {RoleModel.MANAGER_ROLE} not found")
            
            # adminロールを削除（または非アクティブ化）
            admin_role_model = admin_role[0]
            admin_role_model.delete_flag = True
            admin_role_model.updated_at = datetime.now()
            
            # managerロールを追加
            new_role = UserRoleModel(
                id=str(uuid.uuid4()),
                user_id=str(user_id),
                role_id=manager_role.id,
                delete_flag=False,
                created_at=datetime.now(),
                created_by=user.updated_by,
                updated_at=datetime.now(),
                updated_by=user.updated_by
            )
            self.db.add(new_role)
            
            # ユーザー更新時間を更新
            user.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(user)
            
            # ユーザー情報を取得して返す
            user_info = (
                self.db.query(UserInfoModel)
                .filter(
                    UserInfoModel.user_id == str(user_id),
                    UserInfoModel.delete_flag == False,  # noqa: E712
                )
                .first()
            )
            
            return self._to_entity(user, user_info)
        except Exception as e:
            self.db.rollback()
            raise e

    def demote_from_manager_to_user(self, user_id: UserId) -> Optional[User]:
        """ユーザーの権限を'manager'から'user'に降格させる。

        Args:
            user_id: 降格させるユーザーの一意識別子。

        Returns:
            降格させたユーザー。見つからないか現在の役割が'manager'でない場合はNone。
        """
        try:
            # 同様のパターンでmanagerからuserへの降格処理を実装
            # ユーザーが存在するか確認
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
            
            # managerロールを持っているかチェック
            manager_role = (
                self.db.query(UserRoleModel, RoleModel)
                .join(RoleModel, UserRoleModel.role_id == RoleModel.id)
                .filter(
                    UserRoleModel.user_id == str(user_id),
                    UserRoleModel.delete_flag == False,  # noqa: E712
                    RoleModel.role_name == RoleModel.MANAGER_ROLE
                )
                .first()
            )
            
            if not manager_role:
                return None
                
            # userロールを取得
            user_role = (
                self.db.query(RoleModel)
                .filter(
                    RoleModel.role_name == RoleModel.USER_ROLE,
                    RoleModel.delete_flag == False  # noqa: E712
                )
                .first()
            )
            
            if not user_role:
                raise ValueError(f"Role {RoleModel.USER_ROLE} not found")
            
            # managerロールを削除（または非アクティブ化）
            manager_role_model = manager_role[0]
            manager_role_model.delete_flag = True
            manager_role_model.updated_at = datetime.now()
            
            # userロールを追加
            new_role = UserRoleModel(
                id=str(uuid.uuid4()),
                user_id=str(user_id),
                role_id=user_role.id,
                delete_flag=False,
                created_at=datetime.now(),
                created_by=user.updated_by,
                updated_at=datetime.now(),
                updated_by=user.updated_by
            )
            self.db.add(new_role)
            
            # ユーザー更新時間を更新
            user.updated_at = datetime.now()
            
            self.db.commit()
            self.db.refresh(user)
            
            # ユーザー情報を取得して返す
            user_info = (
                self.db.query(UserInfoModel)
                .filter(
                    UserInfoModel.user_id == str(user_id),
                    UserInfoModel.delete_flag == False,  # noqa: E712
                )
                .first()
            )
            
            return self._to_entity(user, user_info)
        except Exception as e:
            self.db.rollback()
            raise e

    def has_manager_role(self, user_id: UserId) -> bool:
        """指定されたユーザーがマネージャー権限以上を持っているか確認する。

        Args:
            user_id: 確認するユーザーの一意識別子。

        Returns:
            マネージャー権限以上を持っている場合はTrue、そうでない場合はFalse。
        """
        # UserRoleModelとRoleModelを結合して、ユーザーのロールを取得
        user_roles = (
            self.db.query(UserRoleModel, RoleModel)
            .join(RoleModel, UserRoleModel.role_id == RoleModel.id)
            .filter(
                UserRoleModel.user_id == str(user_id),
                UserRoleModel.delete_flag == False,  # noqa: E712
                RoleModel.delete_flag == False,      # noqa: E712
            )
            .all()
        )
        
        # ユーザーのロール名を取得
        role_names = [role[1].role_name for role in user_roles]
        
        # マネージャー以上のロールを持っているか確認
        return any(
            RoleModel.get_role_level(role_name) >= RoleModel.get_role_level(RoleModel.MANAGER_ROLE)
            for role_name in role_names
        )

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
