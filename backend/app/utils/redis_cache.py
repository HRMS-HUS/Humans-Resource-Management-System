# from ..configs.redis import redis_client
# import json
# from typing import Optional, Any
# import pickle

# class RedisCache:
#     def __init__(self, prefix: str, ttl: int = 3600):
#         self.prefix = prefix
#         self.ttl = ttl

#     def _get_key(self, key: str) -> str:
#         return f"{self.prefix}:{key}"

#     async def get(self, key: str) -> Optional[Any]:
#         full_key = self._get_key(key)
#         data = await redis_client.get(full_key)
#         if data:
#             return pickle.loads(data.encode())
#         return None

#     async def set(self, key: str, value: Any) -> bool:
#         full_key = self._get_key(key)
#         try:
#             serialized_value = pickle.dumps(value)
#             await redis_client.set(full_key, serialized_value, ex=self.ttl)
#             return True
#         except Exception:
#             return False

#     async def delete(self, key: str) -> bool:
#         full_key = self._get_key(key)
#         return bool(await redis_client.delete(full_key))

#     async def delete_pattern(self, pattern: str) -> bool:
#         full_pattern = self._get_key(pattern)
#         keys = await redis_client.keys(f"{full_pattern}*")
#         if keys:
#             await redis_client.delete(*keys)
#         return True
