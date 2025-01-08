import redis
import time
from fastapi import HTTPException, status
import asyncio
import os
import uuid
from dotenv import load_dotenv
from typing import List

load_dotenv()

def get_redis_client():
    return redis.Redis(
        host=os.getenv('REDIS_HOST'),
        port=int(os.getenv('REDIS_PORT')),
        db=int(os.getenv('REDIS_DB'))
    )