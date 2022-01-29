from environs import Env

env: Env = Env()
Env.read_env()


class FlaskConfig:
    CSRF_ENABLED: bool = env('CSRF_ENABLED')
    SECRET_KEY: str = env('SECRET_KEY')
    FLASK_ENV: str = env('FLASK_ENV')
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{env("POSTGRES_USER")}:'
        + f'{env("POSTGRES_PASSWORD")}@'
        + f'{env("POSTGRES_HOST")}:'
        + f'{env("POSTGRES_PORT")}/'
        + f'{env("POSTGRES_DB")}'
    )
