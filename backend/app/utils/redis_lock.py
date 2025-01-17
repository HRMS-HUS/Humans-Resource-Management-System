from redis.asyncio import Redis
import asyncio
import uuid
from fastapi import HTTPException, status
from ..configs.redis import redis_client


class DistributedLock:
    def __init__(self, lock_key: str, expire_time: int = 10):
        self.lock_key = f"lock:{lock_key}"
        self.expire_time = expire_time
        self.lock_value = str(uuid.uuid4())
        self.renew_task = None
        self.redis_client = None

    async def renew_lock(self):
        while True:
            await asyncio.sleep(self.expire_time * 0.5)
            await self.redis_client.expire(self.lock_key, self.expire_time)

    async def __aenter__(self):
        self.redis_client = await redis_client
        attempts = 3
        while attempts > 0:
            if await self.redis_client.set(self.lock_key, self.lock_value, ex=self.expire_time, nx=True):
                self.renew_task = asyncio.create_task(self.renew_lock())
                return self
            attempts -= 1
            await asyncio.sleep(1)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource is locked. Please try again later."
        )

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.renew_task:
            self.renew_task.cancel()
        lua_script = """
        if redis.call("get", KEYS[1]) == ARGV[1] then
            return redis.call("del", KEYS[1])
        else
            return 0
        end
        """
        await self.redis_client.eval(lua_script, 1, self.lock_key, self.lock_value)
        await self.redis_client.close()

