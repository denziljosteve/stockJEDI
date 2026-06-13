import json
from typing import Optional, Any
import redis.asyncio as redis
from loguru import logger
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        if not self.redis:
            try:
                self.redis = await redis.from_url(
                    settings.REDIS_URL,
                    encoding="utf-8",
                    decode_responses=True
                )
                logger.info("Redis connection established")
            except redis.ConnectionError as e:
                logger.error(f"Redis connection failed: {e}")
                self.redis = None
                raise
            except Exception as e:
                logger.error(f"Unexpected Redis error during connection: {e}")
                self.redis = None
                raise

    async def close(self):
        if self.redis:
            try:
                await self.redis.close()
                logger.info("Redis connection closed")
            except Exception as e:
                logger.error(f"Error closing Redis connection: {e}")
            finally:
                self.redis = None

    async def get(self, key: str) -> Optional[Any]:
        try:
            await self.connect()
            if not self.redis:
                return None
            data = await self.redis.get(key)
            if data:
                return json.loads(data)
            return None
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection lost during GET {key}: {e}")
            self.redis = None
            return None
        except Exception as e:
            logger.error(f"Cache GET error for key {key}: {e}")
            return None

    async def set(self, key: str, value: Any, expire: int = 3600):
        try:
            await self.connect()
            if not self.redis:
                return
            await self.redis.set(key, json.dumps(value), ex=expire)
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection lost during SET {key}: {e}")
            self.redis = None
        except Exception as e:
            logger.error(f"Cache SET error for key {key}: {e}")

    async def delete(self, key: str):
        try:
            await self.connect()
            if not self.redis:
                return
            await self.redis.delete(key)
        except redis.ConnectionError as e:
            logger.warning(f"Redis connection lost during DELETE {key}: {e}")
            self.redis = None
        except Exception as e:
            logger.error(f"Cache DELETE error for key {key}: {e}")

cache_service = CacheService()
