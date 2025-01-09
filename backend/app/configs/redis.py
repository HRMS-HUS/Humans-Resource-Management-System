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

# redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

