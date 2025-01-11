import json
import os
import asyncio
from datetime import datetime, date
from typing import Dict, Any, List
from collections import deque
import logging.handlers

class AsyncLogger:
    def __init__(self, 
                 log_file: str = "backend/logs/app_logs.json",
                 buffer_size: int = 100,
                 max_file_size: int = 5 * 1024 * 1024,  # 5MB
                 backup_count: int = 3):
        self.log_dir = os.path.dirname(log_file)
        self.log_file = log_file
        self.buffer = deque(maxlen=buffer_size)
        self.buffer_lock = asyncio.Lock()
        self.max_file_size = max_file_size
        self.backup_count = backup_count
        self._ensure_log_directory()
        self._ensure_log_file()
        self._start_background_task()

    def _ensure_log_directory(self):
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

    def _ensure_log_file(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump({"logs": []}, f, ensure_ascii=False)

    def _start_background_task(self):
        asyncio.create_task(self._flush_buffer_periodically())

    async def _flush_buffer_periodically(self, interval: int = 5):
        while True:
            await asyncio.sleep(interval)
            await self._flush_buffer()

    async def _flush_buffer(self):
        if not self.buffer:
            return

        async with self.buffer_lock:
            logs = self._read_logs()
            while self.buffer:
                logs["logs"].append(self.buffer.popleft())
            
            # Check file size and rotate if needed
            if os.path.getsize(self.log_file) > self.max_file_size:
                self._rotate_logs()

            self._write_logs(logs)

    def _rotate_logs(self):
        for i in range(self.backup_count - 1, 0, -1):
            src = f"{self.log_file}.{i}"
            dst = f"{self.log_file}.{i + 1}"
            if os.path.exists(src):
                os.rename(src, dst)
        if os.path.exists(self.log_file):
            os.rename(self.log_file, f"{self.log_file}.1")

    def _read_logs(self) -> Dict:
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"logs": []}

    def _write_logs(self, logs: Dict):
        with open(self.log_file, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False, cls=DateTimeEncoder)

    async def log(self, level: str, message: str, data: Any = None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message
        }
        
        if data:
            if isinstance(data, dict):
                # Only log essential data
                essential_data = {k: v for k, v in data.items() if k in ['holiday_id', 'status_code', 'error']}
                if essential_data:
                    entry["data"] = essential_data
            else:
                entry["data"] = str(data)

        async with self.buffer_lock:
            self.buffer.append(entry)

    async def info(self, message: str, data: Any = None):
        await self.log("INFO", message, data)

    async def error(self, message: str, error: Exception = None, data: Any = None):
        error_message = f"{message}: {str(error)}" if error else message
        await self.log("ERROR", error_message, data)

    async def warning(self, message: str, data: Any = None):
        await self.log("WARNING", message, data)

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        return super().default(obj)

# Create singleton instance
logger = AsyncLogger()
