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


class FlaskConfigTesting(FlaskConfig):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = (
        f'postgresql://db_test:'
        + f'db_test@'
        + f'db_test:'
        + f'5432/'
        + f'db_test'
    )
