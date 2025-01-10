import json
import os
from datetime import datetime
from typing import Dict, Any

class Logger:
    def __init__(self, log_file: str = "backend/logs/app_logs.json"):
        self.log_dir = os.path.dirname(log_file)
        self.log_file = log_file
        self._ensure_log_directory()
        self._ensure_log_file()

    def _ensure_log_directory(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _ensure_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump({"logs": []}, f, ensure_ascii=False)

    def _read_logs(self) -> Dict:
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {"logs": []}

    def _write_logs(self, logs: Dict):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)

    def _create_log_entry(self, level: str, message: str, data: Any = None) -> Dict:
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        if data:
            entry["data"] = data
        return entry

    def info(self, message: str, data: Any = None):
        self._log("INFO", message, data)

    def error(self, message: str, error: Exception = None, data: Any = None):
        error_message = f"{message}: {str(error)}" if error else message
        self._log("ERROR", error_message, data)

    def warning(self, message: str, data: Any = None):
        self._log("WARNING", message, data)

    def _log(self, level: str, message: str, data: Any = None):
        logs = self._read_logs()
        logs["logs"].append(self._create_log_entry(level, message, data))
        self._write_logs(logs)

# Create singleton instance
logger = Logger()
