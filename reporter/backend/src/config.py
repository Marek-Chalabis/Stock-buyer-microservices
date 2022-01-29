from environs import Env

env: Env = Env()
Env.read_env()


class FlaskConfig:
    SECRET_KEY: str = env('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://{env("POSTGRES_USER")}:'
        + f'{env("POSTGRES_PASSWORD")}@'
        + f'{env("POSTGRES_HOST")}:'
        + f'{env("POSTGRES_PORT")}/'
        + f'{env("POSTGRES_DB")}'
    )
    # prod/dev settings
    FLASK_ENV: str = env('FLASK_ENV')
    CSRF_ENABLED: bool = env('CSRF_ENABLED')
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = env('SQLALCHEMY_TRACK_MODIFICATIONS')
