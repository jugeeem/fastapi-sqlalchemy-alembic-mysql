import os
import yaml
import datetime
import logging
from typing import Dict, Any


class YAMLLogger:
    def __init__(self):
        # コンテナ内の一時ディレクトリを使用してパーミッション問題を解決
        log_dir = "/app/app/logs"
        os.makedirs(log_dir, exist_ok=True)
        self.log_dir = log_dir

        # 基本的なログ設定
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        self.logger = logging.getLogger("app")

    def _get_log_file_name(self) -> str:
        # 現在の日付を取得してファイル名を生成
        today = datetime.datetime.now().strftime("%Y%m%d")
        return f"access-{today}.yml"

    def _get_log_file_path(self) -> str:
        # ログファイルのフルパスを取得
        file_name = self._get_log_file_name()
        return os.path.join(self.log_dir, file_name)

    def log_access(self, log_data: Dict[str, Any]) -> None:
        """アクセスログを YAML 形式で記録する"""
        file_path = self._get_log_file_path()

        # 既存のログファイルを読み込む
        existing_logs = []
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                existing_logs = yaml.safe_load(file) or []

        # 新しいログをリストに追加
        existing_logs.append(log_data)

        # ファイルに書き込む
        with open(file_path, "w") as file:
            yaml.dump(existing_logs, file, default_flow_style=False)
