from functools import lru_cache
from types import MappingProxyType

from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = '/api/v1'
    REDIS_HOST: str
    X_API_KEY_SECRET: str
    REPORTER_SERVER_API_V1_URL: str
    REPORTER_SERVER_KEY_SECRET: str

    class Config:
        case_sensitive = True
        allow_mutation = False
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @property
    def reporter_server_client(self):
        return MappingProxyType(
            {
                'stocks-purchase-orders': f'{self.REPORTER_SERVER_API_V1_URL}/stocks-purchase-orders/',
            },
        )


@lru_cache
def get_settings() -> BaseSettings:
    return Settings()


settings = Settings()
