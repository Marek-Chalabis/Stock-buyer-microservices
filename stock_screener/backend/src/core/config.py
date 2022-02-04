from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_STATUS: str
    CELERY_BROKER_URL: str
    REPORTER_API_ROOT: str
    REPORTER_TOKEN: str
    API_V1_STR: str = '/api/v1'
    PROJECT_NAME: str = 'Stock Screener'

    class Config:
        case_sensitive = True
        allow_mutation = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
