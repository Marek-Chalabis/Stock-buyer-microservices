from pydantic import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    REDIS_HOST: str
    X_API_KEY_SECRET: str

    class Config:
        case_sensitive = True
        allow_mutation = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
