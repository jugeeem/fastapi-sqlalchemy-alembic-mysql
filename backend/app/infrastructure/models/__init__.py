# SQLAlchemyがモデル間のリレーションシップを解決できるように
# すべてのモデルをここでインポートします

from app.infrastructure.models.permission import PermissionModel  # noqa: F401
from app.infrastructure.models.role import RoleModel  # noqa: F401
from app.infrastructure.models.role_permission import (
    RolePermissionModel,  # noqa: F401
)
from app.infrastructure.models.user import UserModel  # noqa: F401
from app.infrastructure.models.user_role import UserRoleModel  # noqa: F401

# 他のモデルがある場合は、ここにインポートを追加してください
