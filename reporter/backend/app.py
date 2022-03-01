from src import create_app
from src.celery import create_celery

app = create_app()
celery = create_celery(app=app)

if __name__ == '__main__':
    app.run(host='0.0.0.0')  # noqa: S104
