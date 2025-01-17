import os
import asyncio
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler

class AsyncLogger:
    def __init__(self, 
                 log_file: str = "logs/app.log",
                 max_file_size: int = 5 * 1024 * 1024,
                 backup_count: int = 3):
        self.logger = logging.getLogger('AsyncLogger')
        self.logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Ensure log directory exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
            
        # Setup RotatingFileHandler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    async def log(self, level: str, message: str, data: any = None):
        log_message = message
        if data:
            if isinstance(data, dict):
                essential_data = {k: v for k, v in data.items() if k in ['holiday_id', 'status_code', 'error']}
                if essential_data:
                    log_message = f"{message} - Data: {essential_data}"
            else:
                log_message = f"{message} - Data: {str(data)}"

        if level == "INFO":
            self.logger.info(log_message)
        elif level == "ERROR":
            self.logger.error(log_message)
        elif level == "WARNING":
            self.logger.warning(log_message)

    async def info(self, message: str, data: any = None):
        await self.log("INFO", message, data)

    async def error(self, message: str, error: Exception = None, data: any = None):
        error_message = f"{message}: {str(error)}" if error else message
        await self.log("ERROR", error_message, data)

    async def warning(self, message: str, data: any = None):
        await self.log("WARNING", message, data)

# Create singleton instance
logger = AsyncLogger()
