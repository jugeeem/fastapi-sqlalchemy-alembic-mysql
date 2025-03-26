# FastAPI DDD Example

このプロジェクトは、FastAPI、SQLAlchemy、Alembic、MySQLを使用した、厳密なドメイン駆動開発（DDD）パターンに従ったRESTful APIのサンプル実装です。

## プロジェクト構造

```
backend/
├── .python-version      # Python 3.13を指定
├── app/                 # アプリケーションコード
│   ├── main.py          # アプリケーションエントリーポイント
│   ├── domain/          # ドメイン層（エンティティ、バリューオブジェクト、リポジトリインターフェース）
│   ├── application/     # アプリケーション層（ユースケース、DTOs）
│   ├── infrastructure/  # インフラストラクチャ層（DBモデル、リポジトリ実装）
│   └── interfaces/      # インターフェース層（API、スキーマ）
├── alembic/             # マイグレーション設定
└── requirements.txt     # 依存関係
```

## セットアップ

1. 依存関係のインストール:
```bash
uv pip install -r backend/requirements.txt
```

2. データベースの作成:
```sql
CREATE DATABASE fastapi_db;
```

3. 環境変数の設定:
```bash
# .envファイルを作成
MYSQL_USER=root
MYSQL_PASSWORD=password
MYSQL_SERVER=localhost
MYSQL_PORT=3306
MYSQL_DB=fastapi_db
```

4. マイグレーションの実行:
```bash
cd backend
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 実行方法

```bash
cd backend
uv run fastapi run app/main.py
```

サーバーは `http://localhost:8000` で実行されます。
APIドキュメント: `http://localhost:8000/docs`

## APIエンドポイント

### ユーザーAPI
- `GET /api/v1/users` - すべてのユーザーを取得
- `POST /api/v1/users` - 新しいユーザーを作成
- `GET /api/v1/users/{user_id}` - 特定のユーザーを取得
- `PUT /api/v1/users/{user_id}` - ユーザー情報を更新
- `DELETE /api/v1/users/{user_id}` - ユーザーを削除

### 勤怠情報API
- `GET /api/v1/attendances` - 勤怠情報を取得 (クエリパラメータで絞り込み可能)
- `POST /api/v1/attendances` - 新しい勤怠情報を作成
- `GET /api/v1/attendances/{attendance_id}` - 特定の勤怠情報を取得
- `PUT /api/v1/attendances/{attendance_id}` - 勤怠情報を更新
- `DELETE /api/v1/attendances/{attendance_id}` - 勤怠情報を削除