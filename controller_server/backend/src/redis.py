import redis  # type: ignore

from src.core.config import settings

redis = redis.Redis(host=settings.REDIS_HOST)
