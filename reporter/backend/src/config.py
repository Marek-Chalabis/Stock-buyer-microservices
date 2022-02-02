from environs import Env

env: Env = Env()
Env.read_env()


class FlaskConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CSRF_ENABLED = True
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


class FlaskConfigTesting(FlaskConfig):
    TESTING = True
    BCRYPT_LOG_ROUNDS = 4
    SQLALCHEMY_DATABASE_URI = f'postgresql://db_test:db_test@db_test:5432/db_test'
