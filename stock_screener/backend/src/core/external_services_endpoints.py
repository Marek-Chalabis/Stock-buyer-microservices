from typing import Dict

from src.core.config import settings


class ExternalServicesAPI:
    @property
    def reporter(self) -> Dict[str, str]:
        root = settings.REPORTER_API_ROOT
        return {'stocks': f'{root}/stocks'}


external_endpoints = ExternalServicesAPI()
