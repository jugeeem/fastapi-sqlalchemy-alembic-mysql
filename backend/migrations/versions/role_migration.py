"""ロールベースの権限管理を実装するためのマイグレーション

Revision ID: role_migration
Revises: initial_migration
Create Date: 2023-XX-XX XX:XX:XX.XXXXXX

"""
from datetime import datetime
import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import table, column

# 修正: revisionとdownrevisionを適切な値に変更
revision = 'role_migration'
down_revision = 'initial_migration'  # 前のマイグレーションの識別子
branch_labels = None
depends_on = None


def upgrade():
    # UserModelのmanager_idをNULLABLEに変更
    op.alter_column('users', 'manager_id',
               existing_type=sa.CHAR(36),
               nullable=True)
    
    # デフォルトロールを作成
    now = datetime.now()
    roles = table('roles',
        column('id', sa.CHAR(36)),
        column('role_name', sa.String(50)),
        column('description', sa.String(255)),
        column('delete_flag', sa.Boolean),
        column('created_at', sa.DateTime),
        column('created_by', sa.String(255)),
        column('updated_at', sa.DateTime),
        column('updated_by', sa.String(255))
    )
    
    # システム定義のロールID（後で参照するために固定値を使用）
    user_role_id = str(uuid.uuid4())
    manager_role_id = str(uuid.uuid4())
    admin_role_id = str(uuid.uuid4())
    
    op.bulk_insert(roles, [
        {
            'id': user_role_id,
            'role_name': 'user_role',
            'description': '一般ユーザー権限',
            'delete_flag': False,
            'created_at': now,
            'created_by': 'system',
            'updated_at': now,
            'updated_by': 'system'
        },
        {
            'id': manager_role_id,
            'role_name': 'manager_role',
            'description': 'マネージャー権限',
            'delete_flag': False,
            'created_at': now,
            'created_by': 'system',
            'updated_at': now,
            'updated_by': 'system'
        },
        {
            'id': admin_role_id,
            'role_name': 'admin_role',
            'description': '管理者権限',
            'delete_flag': False,
            'created_at': now,
            'created_by': 'system',
            'updated_at': now,
            'updated_by': 'system'
        }
    ])
    
    # 既存のユーザーに対してロールを設定
    conn = op.get_bind()
    # すべてのアクティブユーザーを取得
    users = conn.execute("SELECT id, manager_id FROM users WHERE delete_flag = 0").fetchall()
    
    # 各ユーザーに適切なロールを設定
    for user in users:
        role_id = user_role_id  # デフォルトは一般ユーザー
        
        if user.manager_id == 'manager':
            role_id = manager_role_id
        elif user.manager_id == 'admin':
            role_id = admin_role_id
        
        # ユーザーロールテーブルに挿入
        op.execute(f"""
            INSERT INTO user_roles
            (id, user_id, role_id, delete_flag, created_at, created_by, updated_at, updated_by)
            VALUES
            ('{str(uuid.uuid4())}', '{user.id}', '{role_id}', 0, '{now}', 'system', '{now}', 'system')
        """)
        
        # manager_idが特殊値（'user','manager','admin'）の場合はNULLに設定
        if user.manager_id in ['user', 'manager', 'admin']:
            op.execute(f"""
                UPDATE users
                SET manager_id = NULL,
                    updated_at = '{now}',
                    updated_by = 'system'
                WHERE id = '{user.id}'
            """)


def downgrade():
    # マイグレーションを元に戻す場合の処理（一括移行なのでダウングレードは提供しない）
    pass
