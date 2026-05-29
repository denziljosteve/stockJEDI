import json
from typing import Optional, Any
import redis.asyncio as redis
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        if not self.redis:
            self.redis = await redis.from_url(
                settings.REDIS_URL, 
                encoding="utf-8", 
                decode_responses=True
            )

    async def get(self, key: str) -> Optional[Any]:
        await self.connect()
        data = await self.redis.get(key)
        if data:
            return json.loads(data)
        return None

    async def set(self, key: str, value: Any, expire: int = 3600):
        await self.connect()
        await self.redis.set(key, json.dumps(value), ex=expire)

    async def delete(self, key: str):
        await self.connect()
        await self.redis.delete(key)

cache_service = CacheService()
