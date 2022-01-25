import logging

from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server."""

    LOGGER_NAME: str = 'mycoolapp'
    LOG_FORMAT: str = '%(levelprefix)s - %(asctime)s - %(message)s'
    LOG_LEVEL: str = 'INFO'

    version = 1
    formatters = {
        'default': {
            '()': 'uvicorn.logging.DefaultFormatter',
            'fmt': LOG_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    }
    handlers = {
        'default': {
            'formatter': 'default',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
        },
    }
    loggers = {
        'controller_server': {'handlers': ['default'], 'level': LOG_LEVEL},
    }


dictConfig(LogConfig().dict())
logger = logging.getLogger('controller_server')
