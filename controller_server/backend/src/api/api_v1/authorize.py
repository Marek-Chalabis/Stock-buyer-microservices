import typing

from fastapi import Header, HTTPException
from src.core.config import settings


class AuthorizerDependencyByXApiKey:
    """Authorize endpoints by X_API_KEY."""

    def __call__(self, x_api_key: typing.Optional[str] = Header(...)) -> None:
        print(settings.X_API_KEY_SECRET)
        if settings.X_API_KEY_SECRET != x_api_key:
            raise HTTPException(status_code=401, detail="unauthorized")
