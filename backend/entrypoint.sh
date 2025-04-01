#!/bin/bash
set -e

echo "Waiting for database to be ready..."
# データベースが利用可能になるまで待機
max_retries=30
retry_interval=2
retry_count=0

# MySQLへの接続確認
check_mysql_connection() {
    if command -v mysql >/dev/null 2>&1; then
        mysql -h db -u user -ppassword -e "SELECT 1" >/dev/null 2>&1
        return $?
    fi
}

while ! check_mysql_connection && [ $retry_count -lt $max_retries ]; do
    echo "Database not ready yet. Waiting... (Attempt $((retry_count+1))/$max_retries)"
    sleep $retry_interval
    retry_count=$((retry_count+1))
done

if [ $retry_count -eq $max_retries ]; then
    echo "Failed to connect to database after $max_retries attempts. Exiting."
    exit 1
fi

echo "Database is ready!"

echo "Running database migrations..."
# マイグレーションディレクトリの権限確認
if [ ! -w /app/migrations/versions ]; then
    echo "No write permission to migrations directory. Trying to fix..."
    # Dockerfileでアクセス権を設定していない場合は、ここで試みる
    mkdir -p /app/migrations/versions
    chmod -R 777 /app/migrations
fi

# マイグレーションファイルの自動生成
alembic revision --autogenerate -m "Auto migration"

# マイグレーションの実行
alembic upgrade head

echo "Migrations completed successfully!"

# FastAPIアプリケーションの起動
echo "Starting FastAPI application..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
