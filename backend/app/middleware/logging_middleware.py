import datetime
import time
import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from ..utils.logger import YAMLLogger


class AccessLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.logger = YAMLLogger()

    async def dispatch(self, request: Request, call_next):
        # リクエスト開始時間
        start_time = time.time()

        # リクエストID生成
        request_id = str(uuid.uuid4())

        # レスポンス処理
        response = await call_next(request)

        # 処理時間計算
        process_time = time.time() - start_time

        # ログデータ作成
        log_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "request_id": request_id,
            "method": request.method,
            "path": request.url.path,
            "query_params": str(request.query_params),
            "client_ip": request.client.host,
            "status_code": response.status_code,
            "process_time_ms": round(process_time * 1000, 2),
        }

        # アクセスログを記録
        self.logger.log_access(log_data)

        return response
