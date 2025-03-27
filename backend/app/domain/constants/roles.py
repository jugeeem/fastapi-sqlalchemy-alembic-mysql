"""ロール関連の定数を定義するモジュール"""

# システム内のデフォルトロール
USER_ROLE = "user_role"
MANAGER_ROLE = "manager_role"
ADMIN_ROLE = "admin_role"

# ロールの階層 (低い値ほど低い権限)
ROLE_HIERARCHY = {
    USER_ROLE: 1,
    MANAGER_ROLE: 2,
    ADMIN_ROLE: 3
}

def get_role_level(role_name):
    """ロールの権限レベルを取得する

    Args:
        role_name: ロール名

    Returns:
        権限レベル（値が大きいほど高い権限）
    """
    return ROLE_HIERARCHY.get(role_name, 0)
