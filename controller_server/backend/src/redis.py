import redis

from src.core.config import settings

r = redis.Redis(host=settings.REDIS_HOST)
