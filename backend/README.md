`uv pip compile pyproject.toml > requirements.txt`

## about pytest  
### 基本的なテスト実行コマンド  
```bash
# backend ディレクトリに移動
cd c:\engineering\fastapi-sqlalchemy-alembic-mysql\backend

# すべてのテストを実行
pytest

# 詳細なテスト結果を表示
pytest -v

# さらに詳細なテスト結果を表示
pytest -vv
```

### テストカバレッジレポートを生成する  
```bash
# テストカバレッジレポートを生成
pytest --cov=app

# HTMLフォーマットでカバレッジレポートを生成
pytest --cov=app --cov-report=html
```

### 特定のテストだけを実行する  
```bash
# 特定のテストファイルを実行
pytest test/domain/test_value_objects.py

# 特定のテストクラスを実行
pytest test/domain/test_value_objects.py::TestEmail

# 特定のテスト関数を実行
pytest test/domain/test_value_objects.py::TestEmail::test_valid_email

# 特定のディレクトリのテストを実行
pytest test/domain/
```

### Docker を使用したテスト実行  
```bash
# Docker コンテナ内でテストを実行
docker-compose exec app pytest

# カバレッジレポート付きでテストを実行
docker-compose exec app pytest --cov=app
```
