import enum


class Gender(enum.Enum):
    """性別の選択肢を定義する列挙型"""
    MALE = "male"
    FEMALE = "female"


class Role(enum.Enum):
    """ユーザー権限レベルを定義する列挙型"""
    ADMIN = "admin"  # システム管理者
    MANAGER = "manager"  # 管理者
    USER = "user"  # 一般ユーザ
    GUEST = "guest"  # 閲覧のみ
