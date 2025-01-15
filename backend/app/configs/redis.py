from redis.asyncio import Redis
import time
from fastapi import HTTPException, status
import asyncio
import os
import uuid
from dotenv import load_dotenv
from typing import List
import redis

load_dotenv()

redis_client = Redis(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT', 6379)),
    db=int(os.getenv('REDIS_DB', 0)),
    password=os.getenv('REDIS_PASSWORD'),
    decode_responses=True
)

# async def init_redis():
#     # Set memory limit and policy after connection
#     await redis_client.config_set('maxmemory', '1073741824')  # 1 GB
#     await redis_client.config_set('maxmemory-policy', 'allkeys-lru')
